import os
import requests
from dotenv import load_dotenv
import pandas as pd
from email.message import EmailMessage
import smtplib
from datetime import datetime, timedelta


load_dotenv()
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
STOCKS_API_KEY = os.environ.get("STOCKS_API_KEY")
RECIPIENT_ADDR = os.environ.get("RECIPIENT_ADDR")
FROM_ADDR = os.environ.get("FROM_ADDR")
LOGIN = os.environ.get("LOGIN")
PASSWORD = os.environ.get("PASSWORD")
MAILHOST = os.environ.get("MAILHOST")
PORT = os.environ.get("PORT")
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

URL_NEWS = "https://newsapi.org/v2/everything"
URL_STOCKS = "https://www.alphavantage.co/query"


def get_percentage_change(ticker):
    # STEP 1: Use https://www.alphavantage.co
    # When STOCK price increase/decreases by 5% between yesterday
    # and the day before yesterday then print("Get News").
    params_stocks = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "outputsize": "compact",
        "apikey": STOCKS_API_KEY
    }
    response = requests.get(URL_STOCKS, params_stocks)
    response.raise_for_status()
    data = response.json()
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
    return percentage_change


def fetch_news(ticker):
    # STEP 2: Use https://newsapi.org
    # Instead of printing ("Get News"), actually get the first
    # 3 news pieces for the COMPANY_NAME.

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
        connection.login(LOGIN, PASSWORD)

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


def get_symbol(percentage_change: float) -> str:
    if percentage_change > 0:
        symbol = "🔺"
    elif percentage_change < 0:
        symbol = "🔻"
    else:
        symbol = "▶"
    return symbol


percentage_change = get_percentage_change(STOCK)
if percentage_change >= 3:
    news = fetch_news(STOCK)
    if news:
        change_symbol = get_symbol(percentage_change)
        content = construct_msg_body(
            STOCK, percentage_change, change_symbol, news)
    print(RECIPIENT_ADDR, f"subject={STOCK} {
          change_symbol} {percentage_change}%", content)
    send_mail(RECIPIENT_ADDR, subject=f"{STOCK} {symbol}", content=content)
