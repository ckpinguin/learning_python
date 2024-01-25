import smtplib
import datetime as dt
import random
import json

try:
    with open(".secret.json", "r") as config_file:
        config_data = json.load(config_file)
except FileNotFoundError:
    print("ERROR: No config file found!")
    exit(0)

MY_EMAIL = config_data["email"]
MY_PASS = config_data["password"]

PORT = 1025
HOSTNAME = "127.0.0.1"


with open("quotes.txt", "r") as file:
    quotes = file.read()

quote = random.choice(quotes)
now = dt.datetime.now()
day_of_week = now.weekday()

if day_of_week == 0:
    with open("quotes.txt") as quote_file:
        all_quotes = quote_file.readlines()
        quote = random.choice(all_quotes)
    print(quote)
    print("Weekday matches, sending mail...")
    with smtplib.SMTP(host=HOSTNAME, port=PORT) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASS)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject: Monday Motivation!\n\n{quote}\n"
        )
else:
    print("No motivation mail today, sorry.")
