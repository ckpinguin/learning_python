from email.message import EmailMessage
import smtplib
import json
import pandas
import random
import datetime as dt
import socks
from billboard_timemachine import BillboardTimeMachine


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


def load_birthday_data(file) -> pandas.DataFrame:
    return pandas.read_csv(file)


def filter_active(df) -> pandas.DataFrame:
    return df[df['active'] == 1]


def filter_birthdays(df: pandas.DataFrame,
                     current_month, current_day) -> pandas.DataFrame:
    return df.dropna(subset=['year', 'month', 'day']).loc[
        (df['month'] == current_month) & (df['day'] == current_day)]


def extract_filtered_entries(df: pandas.DataFrame) -> list[dict]:
    return [{'firstname': row['firstname'],
             'gender': row['gender'], 'email': row['email'],
             'year': row['year'], 'month': row['month'],
             'day': row['day']}
            for _, row in df.iterrows()]


def find_persons_with_birthday_today(file) -> list[dict]:
    df_active = load_birthday_data(file)
    now = dt.datetime.now()
    current_month = now.month
    current_day = now.day
    df_birthday_exists = filter_birthdays(
        df_active, current_month, current_day)
    filtered_entries = extract_filtered_entries(df_birthday_exists)
    return filtered_entries


def read_random_template() -> str:
    rand_no = random.randint(1, 3)
    template = f"letter_templates/letter_{rand_no}.txt"
    with open(template) as file:
        content = file.read()
    return content


def replace_content(content: str, name_to_insert, gender) -> str:
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


def send_mail(email_addr, content, bcc=None) -> None:
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


def send_mail_for_all_bday_persons(
        persons_with_birthday: list[dict],
        top_three_songs_for_birthday: list[tuple]) -> None:
    for person in persons_with_birthday:
        template_content = read_random_template()
        content = replace_content(
            template_content, person['firstname'], person['gender'])
        content_special = "\n\nP.S. Die 3 Top-Songs der US-Charts an deinem Geburtstag waren:\n\n"
        for song, artist in top_three_songs_for_birthday:
            content_special += f"Song: {song}, Interpret: {artist}\n"
        print(
            f"Sending mail to{person['email']} with content:\n \
                {content}\n{content_special}")
        content += "\n" + content_special
        send_mail(person['email'], content, bcc=BCC_ADDR)


# ___ MAIN ____
persons_with_birthday = find_persons_with_birthday_today(BIRTHDAY_FILE)

for person in persons_with_birthday:
    year = person['year']
    month = str(person['month']).zfill(2)
    day = str(person['day']).zfill(2)
    bb = BillboardTimeMachine(
        f"{year}-{month}-{day}")
    top_three_songs_for_birthday = bb.get_top_three_artists_and_tracks()

send_mail_for_all_bday_persons(
    persons_with_birthday, top_three_songs_for_birthday)
