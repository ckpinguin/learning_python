import smtplib
from email.message import EmailMessage
import json


class NotificationManager:
    FROM_ADDR = ""
    MAILHOST = ""
    PORT = ""
    LOGIN = ""
    PASS = ""

    def __init__(self):
        self.config_data = {}
        with open('.secret.json') as env_file:
            self.config_data = json.load(env_file)
        self.FROM_ADDR = self.config_data['FROM_ADDR']
        self.MAILHOST = self.config_data['MAILHOST']
        self.PORT = self.config_data['PORT']
        self.LOGIN = self.config_data['LOGIN']
        self.PASS = self.config_data['PASSWORD']

    def send_price_notification(self, email_addr: str, old_price: int,
                                new_price: int, city: str, date: str,
                                via_cities: str = ""
                                ) -> None:
        content = f"""
        Hello
        The price for a flight to {city} has just dropped
        from CHF {old_price} to {new_price}!
        Flight date is {date}.
        """

        print(f"Sending mail to {email_addr} from {
              self.FROM_ADDR}")

        with smtplib.SMTP(host=self.MAILHOST, port=self.PORT) as connection:
            connection.starttls()
            connection.login(self.LOGIN, self.PASS)
            msg = EmailMessage()
            msg.set_content(content)
            msg["Subject"] = f"Price change for flight to {city}"
            msg["From"] = self.FROM_ADDR
            msg["To"] = email_addr
            connection.send_message(msg)

    def send_emails(self, addr_list: list[str], old_price: int,
                    new_price: int, city: str, via_cities: str, date: str):
        for addr in addr_list:
            self.send_price_notification(
                email_addr=addr, old_price=old_price,
                new_price=new_price, city=city,
                via_cities=via_cities, date=date)
