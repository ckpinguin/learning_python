import requests
import os
from dotenv import load_dotenv
import datetime as dt

load_dotenv()
USER_TOKEN = os.environ.get("USER_TOKEN")
USER_NAME = os.environ.get("USER_NAME")
RECIPIENT_ADDR = os.environ.get("RECIPIENT_ADDR")
FROM_ADDR = os.environ.get("FROM_ADDR")
LOGIN = os.environ.get("LOGIN")
PASSWORD = os.environ.get("PASSWORD")
MAILHOST = os.environ.get("MAILHOST")
PORT = os.environ.get("PORT")

URL_PIXELA = "https://pixe.la/v1/users"

headers = {
    "X-USER-TOKEN": USER_TOKEN
}

# One-timer „create user“:
# user_params = {
#    "token": USER_TOKEN,
#    "username": USER_NAME,
#    "agreeTermsOfService": "yes",
#    "notMinor": "yes"
# }
# response = requests.post(url=URL_PIXELA, json=user_params)
# print(response.text)

# One-timer „create graph“:
# graph_endpoint = f"{URL_PIXELA}/{USER_NAME}/graphs"
# graph_config = {
#   "id": "graph1",
#    "name": "Udemy graph",
#    "unit": "Vids",
#    "type": "int",
#    "color": "shibafu",
# }
# response = requests.post(
#    url=graph_endpoint, json=graph_config, headers=headers)
# print(response.text)

# Post a pixel (for today)


def post_pixel(graph, date, quantity):
    pixelpost_endpoint = f"{URL_PIXELA}/{USER_NAME}/graphs/{graph}"
    pixel_config = {
        "date": date,
        "quantity": f"{quantity}"
    }
    response = requests.post(url=pixelpost_endpoint,
                             json=pixel_config, headers=headers)
    print(response, response.text)


# Update a pixel (for a specific day)
def update_pixel(graph, date, quantity):
    pixelpost_endpoint = f"{URL_PIXELA}/{USER_NAME}/graphs/{graph}/{date}"
    pixel_update_config = {
        "quantity": f"{quantity}"
    }
    response = requests.put(url=pixelpost_endpoint,
                            json=pixel_update_config, headers=headers)
    print(response, response.text)


# Delete a pixel
def delete_pixel(graph, date):
    pixelpost_endpoint = f"{URL_PIXELA}/{USER_NAME}/graphs/{graph}/{date}"
    response = requests.delete(url=pixelpost_endpoint, headers=headers)
    print(response, response.text)


graph_id = "graph1"
today = dt.datetime.now()
today_formatted = today.strftime("%Y%m%d")
post_pixel(graph_id, today_formatted, quantity=4)
yesterday = today - dt.timedelta(days=1)
yesterday_formatted = yesterday.strftime("%Y%m%d")
update_pixel(graph_id, yesterday_formatted, quantity=7)
# delete_pixel(graph_id, today_formatted)
