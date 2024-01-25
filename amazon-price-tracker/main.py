from bs4 import BeautifulSoup
from email.message import EmailMessage
import requests
import json
import python_socks as socks
import smtplib

product_name = "Ninja Foodi"
product_url = "https://www.amazon.de/dp/B09DGBJN2C"
price_threshold = 220

try:
    with open(".secret.json", "r") as config_file:
        config_data: dict = json.load(config_file)
except FileNotFoundError:
    print("ERROR: No config file found!")
    exit(0)
LOGIN = config_data.get("LOGIN")
MY_PASS = config_data.get("PASSWORD")
FROM_ADDR = config_data.get("FROM_ADDR")
RECIPIENT_ADDR = config_data.get("RECIPIENT_ADDR")
PORT = config_data.get("PORT")
HOSTNAME = config_data.get("MAILHOST")
PROXY = config_data.get("PROXY_HOST", None)
PROXY_PORT = config_data.get("PROXY_PORT", None)
if PROXY is not None and PROXY_PORT is not None:
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, PROXY, PROXY_PORT)
    socks.wrapmodule(smtplib)


def send_mail(email_addr, content, product_name):
    print(f"Sending mail to {email_addr} from {FROM_ADDR}")

    with smtplib.SMTP(host=HOSTNAME, port=PORT) as connection:
        connection.starttls()
        connection.login(LOGIN, MY_PASS)

        msg = EmailMessage()
        msg.set_content(content)
        msg["Subject"] = f"Amazon price alert for {product_name}!"
        msg["From"] = FROM_ADDR
        msg["To"] = email_addr

        connection.send_message(msg)


response = requests.get(product_url, headers={
                        "User-Agent": "Defined"})
if response:
    html = response.text

soup = BeautifulSoup(html, "html.parser")
price_tag = soup.find(name="span", class_="a-price-whole")
price = int(price_tag.get_text().split(',')[0])
if price < price_threshold:
    send_mail(RECIPIENT_ADDR, f"Price of {
              product_name} is now: {price} => {product_url}", product_name)
