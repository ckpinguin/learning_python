from email.message import EmailMessage
import smtplib
import json
import pandas
import random
import datetime as dt
import socks


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
BCC_ADDR = config_data.get("BCC_ADDR")
PORT = config_data.get("PORT")
HOSTNAME = config_data.get("MAILHOST")
PROXY = config_data.get("PROXY_HOST", None)
PROXY_PORT = config_data.get("PROXY_PORT", None)
if PROXY is not None and PROXY_PORT is not None:
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, PROXY, PROXY_PORT)
    socks.wrapmodule(smtplib)


BIRTHDAY_FILE = "TEST_birthdays.csv"


def find_persons_with_birthday(file) -> list[dict]:
    now = dt.datetime.now()
    current_month = now.month
    current_day = now.day
    df = pandas.read_csv(file)

    df_with_birthdays = df.dropna(subset=['year', 'month', 'day'])

    df_hits = df_with_birthdays[(df_with_birthdays['month'] == current_month)
                                & (df['day'] == current_day)]
    filtered_entries = []
    if 'email' in df.columns:
        filtered_entries = [{'firstname': row['firstname'],
                             'gender': row['gender'], 'email': row['email']}
                            for _, row in df_hits.iterrows()]
    return filtered_entries


def read_random_template():
    rand_no = random.randint(1, 3)
    template = f"letter_templates/letter_{rand_no}.txt"
    with open(template) as file:
        content = file.read()
    return content


def replace_content(content: str, name_to_insert, gender):
    placeholder_name = '[NAME]'
    placeholder_title = '[TITLE]'
    placeholder_sender = '[SENDER]'
    if gender == 'f':
        title = "Liebe"
    else:
        title = "Lieber"

    content_new = content.replace(placeholder_name, name_to_insert)
    content_new = content_new.replace(placeholder_title, title)
    content_new = content_new.replace(placeholder_sender, SENDER)
    return content_new


def send_mail(email_addr, content, bcc=None):
    print(f"Sending mail to {email_addr} from {FROM_ADDR}")

    with smtplib.SMTP(host=HOSTNAME, port=PORT) as connection:
        connection.starttls()
        connection.login(LOGIN, MY_PASS)

        msg = EmailMessage()
        msg.set_content(content)
        msg["Subject"] = "Happy Birthday!"
        msg["From"] = FROM_ADDR
        msg["To"] = email_addr
        if bcc:
            msg["Bcc"] = bcc

        connection.send_message(msg)


persons_with_birthday = find_persons_with_birthday(BIRTHDAY_FILE)
for person in persons_with_birthday:
    template_content = read_random_template()
    content = replace_content(
        template_content, person['firstname'], person['gender'])
    print(f"Sending mail to{person['email']} with content:\n {content}")
    send_mail(person['email'], content, bcc=BCC_ADDR)
