import requests
import pandas as pd
from email.message import EmailMessage
import smtplib
from datetime import datetime, timedelta
import json
import python_socks as socks
from data_manager import DataManager
import time

try:
    with open(".secret.json", "r") as config_file:
        config_data: dict = json.load(config_file)
except FileNotFoundError:
    print("ERROR: No config file found!")
    exit(0)

SENDER = config_data.get("SENDER")
LOGIN = config_data.get("LOGIN")
MY_PASS = config_data.get("PASSWORD")
FROM_ADDR = config_data.get("FROM_ADDR")
RECIPIENT_ADDR = config_data.get("RECIPIENT_ADDR")
PORT = config_data.get("PORT")
MAILHOST = config_data.get("MAILHOST")
PROXY = config_data.get("PROXY_HOST", None)
PROXY_PORT = config_data.get("PROXY_PORT", None)
if PROXY is not None and PROXY_PORT is not None:
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, PROXY, PROXY_PORT)
    socks.wrapmodule(smtplib)
NEWS_API_KEY = config_data.get("NEWS_API_KEY")
STOCKS_API_KEY = config_data.get("STOCKS_API_KEY")
TWELVEDATA_API_KEY = config_data.get("TWELVEDATA_API_KEY")

URL_NEWS = "https://newsapi.org/v2/everything"
# Alpha Vantage API is restricted to 25 API requests per day
# URL_STOCKS = "https://www.alphavantage.co/query"
URL_STOCKS = "https://api.twelvedata.com/time_series"


def limiter(limit):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print("Limiting requests...")
            tickers = kwargs.get('tickers', [])
            print(tickers)
            if len(tickers) > limit:
                print("Too many requests for that API!")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator


@limiter(8)
def get_percentage_change_batch(tickers: list[str]) -> dict[str, float]:
    params_stocks = {
        "symbol": ",".join(tickers),
        "interval": "1day",
        "apikey": TWELVEDATA_API_KEY
    }
    response = requests.get(URL_STOCKS, params_stocks)
    response.raise_for_status()
    data = response.json()
    print(data)
    return data


# For limited API requests, this with a timeout of 1 minute is
# enough for daily data checks
def get_percentage_change(ticker: str) -> float:
    params_stocks = {
        "symbol": ticker,
        "interval": "1day",
        "apikey": TWELVEDATA_API_KEY
    }
    response = requests.get(URL_STOCKS, params_stocks)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data['values'])
    df['datetime'] = pd.to_datetime(df['datetime'])

    print("close today: ", df.iloc[0].close)
    print("close day before: ", df.iloc[1].close)


""" def get_percentage_change2(ticker):
    params_stocks = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "outputsize": "compact",
        "apikey": STOCKS_API_KEY
    }
    response = requests.get(URL_STOCKS, params_stocks)
    response.raise_for_status()
    data = response.json()
    print(data)
    series_daily = data['Time Series (Daily)']
    # dict keys as rows of the df:
    df = pd.DataFrame.from_dict(series_daily, orient='index')
    # now make the index sortable by converting it to datetime
    df.index = pd.to_datetime(df.index)
    df = df.sort_index(ascending=False)

    latest_close_prices = df.head(2)['4. close'].astype(float).tolist()
    last_close = latest_close_prices[0]
    day_before_close = latest_close_prices[1]
    percentage_change = (day_before_close - last_close) / last_close * 100
    return round(percentage_change, 2) """


def fetch_news(ticker):
    current_date = datetime.now()
    # Calculate one month back
    one_month_back = current_date - timedelta(days=30)
    # Format the result
    formatted_date = one_month_back.strftime('%Y-%m-%d')

    params_news = {
        "q": ticker,
        "from": formatted_date,
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(URL_NEWS, params_news)
    response.raise_for_status()
    data = response.json()
    articles_list = data['articles']
    # df = pd.DataFrame.from_dict(articles, orient='index')
    df = pd.DataFrame(articles_list)
    # Select the first 3 records and specific columns
    result_df = df.loc[:2, ["title", "description", "publishedAt"]]
    result_tuples = [tuple(row)
                     for row in result_df.itertuples(index=False, name=None)]

    # print(result_tuples)
    return result_tuples


def send_mail(email_addr, subject, content, bcc=None):
    # STEP 3:
    # Send a seperate message with the percentage change and
    # each article's title and description to your phone number.
    print(f"Sending mail to {email_addr} from {FROM_ADDR}")

    with smtplib.SMTP(host=MAILHOST, port=PORT) as connection:
        connection.starttls()
        connection.login(LOGIN, MY_PASS)

        msg = EmailMessage()
        msg.set_payload(content, "utf-8")
        # msg.set_content(content)
        msg["Subject"] = subject
        msg["From"] = FROM_ADDR
        msg["To"] = email_addr
        if bcc:
            msg["Bcc"] = bcc

        connection.send_message(msg)


def construct_msg_body(ticker, change, change_symbol, news):
    body = ""
    for text in news:
        headline, content, date = text
        body += f"""
            {ticker}: {change_symbol} {change}%
            Date: {date}
            Headline: {headline}
            Brief: {content}
        """
    return body


def get_up_down_symbol(percentage_change: float) -> str:
    if percentage_change > 0:
        symbol = "🔺"
    elif percentage_change < 0:
        symbol = "🔻"
    else:
        symbol = "▶"
    return symbol


dm = DataManager(sheet_name="Portfolio")
stocks = dm.get_data()

tickers = []
for stock in stocks:
    tickers.append(stock.get("Ticker"))


# print("Getting data for", tickers)
# get_percentage_change_batch(tickers=tickers)


for stock in stocks:
    ticker = stock.get("Ticker")
    print(f"Getting data for {ticker}")
    percentage_change = get_percentage_change(ticker)
    time.sleep(10)
"""    if percentage_change >= 3:
        news = fetch_news(ticker)
        if news:
            change_symbol = get_up_down_symbol(percentage_change)
            content = construct_msg_body(
                ticker, percentage_change, change_symbol, news)
        print(RECIPIENT_ADDR,
              f"subject={ticker} {change_symbol} {percentage_change}%",
              content)
        send_mail(RECIPIENT_ADDR,
                  subject=f"{ticker} {change_symbol} {percentage_change}%",
                  content=content)
 """
