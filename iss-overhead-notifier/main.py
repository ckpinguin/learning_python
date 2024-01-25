import requests
import datetime as dt
from tzlocal import get_localzone
import socks
import smtplib
import json
import time

MY_LAT = 47.258949
MY_LNG = 8.848430

URL_ISS = "http://api.open-notify.org/iss-now.json"
URL_SUN = "https://api.sunrise-sunset.org/json"
VISIBILITY_THRESHOLD = 10

try:
    with open(".secret.json", "r") as config_file:
        config_data: dict = json.load(config_file)
except FileNotFoundError:
    print("ERROR: No config file found!")
    exit(0)

LOGIN = config_data.get("LOGIN")
MY_PASS = config_data.get("PASSWORD")
TO_ADDR = config_data.get("TO_ADDR")
FROM_ADDR = config_data.get("FROM_ADDR")
PORT = config_data.get("PORT")
HOSTNAME = config_data.get("MAILHOST")
PROXY = config_data.get("PROXY_HOST", None)
PROXY_PORT = config_data.get("PROXY_PORT", None)
if PROXY is not None and PROXY_PORT is not None:
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, PROXY, PROXY_PORT)
    socks.wrapmodule(smtplib)


def is_night(sunrise_hour, sunset_hour, current_hour) -> bool:
    if sunset_hour < sunrise_hour:
        # Case where sunset is in the evening and sunrise is in the morning
        return not (sunset_hour <= current_hour <= sunrise_hour)
    else:
        # Case where sunset is in the morning and sunrise is in the evening
        return current_hour <= sunrise_hour or current_hour >= sunset_hour


def get_sunrise_sunset() -> tuple:
    sun_params = {"lat": MY_LAT,
                  "lng": MY_LNG,
                  "formatted": 0}
    response = requests.get(URL_SUN, params=sun_params)
    response.raise_for_status()
    data = response.json()
    sunrise_time: str = data["results"]["sunrise"]
    sunset_time: str = data["results"]["sunset"]
    return (sunrise_time, sunset_time)


def convert_utc_to_local(dt_to_convert: str) -> dt.datetime:
    utc_datetime = dt.datetime.fromisoformat(dt_to_convert)
    local_timezone = get_localzone()
    local_datetime = utc_datetime.astimezone(local_timezone)
    return local_datetime


def is_iss_in_sight(position: tuple) -> bool:
    iss_lat, iss_lng = get_iss_position()
    return is_object_within_threshold(MY_LAT, MY_LNG,
                                      iss_lat, iss_lng, VISIBILITY_THRESHOLD)


def get_iss_position() -> tuple:
    response = requests.get(URL_ISS)
    response.raise_for_status()
    data = response.json()
    longitude = float(data["iss_position"]["longitude"])
    latitude = float(data["iss_position"]["latitude"])
    iss_position = (longitude, latitude)
    print(f"ISS is at: {iss_position}")
    return iss_position


def is_object_within_threshold(lat_observer, lng_observer,
                               lat_obj, lng_obj, threshold) -> bool:
    lat_diff = abs(lat_observer - lat_obj)
    lng_diff = abs(lng_observer - lng_obj)
    return lat_diff <= threshold and lng_diff <= threshold


def send_mail(email_addr):
    print(f"Sending mail to {email_addr} from {FROM_ADDR}")
    with smtplib.SMTP(host=HOSTNAME, port=PORT) as connection:
        connection.starttls()
        connection.login(LOGIN, MY_PASS)
        connection.sendmail(
            from_addr=FROM_ADDR,
            to_addrs=TO_ADDR,
            msg="Subject: Look up!\nLook up"
                "outside! ISS is currently overhead!"
        )


while True:
    now = dt.datetime.now()
    current_hour = now.hour
    sunrise, sunset = get_sunrise_sunset()
    sunrise_local = convert_utc_to_local(sunrise)
    sunset_local = convert_utc_to_local(sunset)
    sunrise_hour = sunrise_local.hour
    sunset_hour = sunset_local.hour
    if is_iss_in_sight((MY_LAT, MY_LNG))\
            and is_night(sunrise_hour, sunset_hour, current_hour):
        print("ISS is currently in sight! Sending mail to look above!")
        send_mail()
    else:
        print("No ISS in sight now...")
    time.sleep(60)
