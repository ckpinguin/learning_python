import requests
import os
from dotenv import load_dotenv
import datetime as dt
import pandas as pd

# Set pandas options to display all rows and columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

load_dotenv()
APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
TOKEN_SHEETY = os.environ.get("TOKEN_SHEETY")
URL_SHEETY = os.environ.get("URL_SHEETY")
GOOGLE_SHEET_NAME = "workout"

URL_NUTRITIONIX = "https://trackapi.nutritionix.com/v2/natural/exercise"

headers = {
    "X-APP-ID": APP_ID,
    "X-APP-KEY": API_KEY
}

query = input("What did you do today?: ")
params = {
    "query": query,
    "gender": "male",
    "weight_kg": 85,
    "height_cm": 176,
    "age": 48
}

response = requests.post(url=URL_NUTRITIONIX,
                         json=params, headers=headers)
data = response.json()
# df = pd.DataFrame.from_dict(data, orient='index')
df = pd.json_normalize(data['exercises'])
# print(df.to_string(index=False))
exercises: list[dict] = df[['name', 'nf_calories', 'duration_min']
                           ].to_dict(orient='records')


def post_exercise(url, sheetname: str,
                  exercise: str, duration: int, calories: float):
    current_date = dt.datetime.now()
    formatted_date = current_date.strftime("%d/%m/%Y")
    formatted_time = current_date.strftime("%H:%M:%S")
    headers = {
        "Authorization": f"Bearer {TOKEN_SHEETY}"
    }
    body = {
        sheetname: {
            "date": formatted_date,
            "time": formatted_time,
            "exercise": exercise.title(),
            "duration": duration,
            "calories": calories
        }
    }
    response = requests.post(url, json=body, headers=headers)
    print(response, response.text)


request_url = f"{URL_SHEETY}/myWorkouts/workouts"


for ex in exercises:
    exercise = ex['name']
    duration = ex['duration_min']
    calories = ex['nf_calories']

    post_exercise(request_url, sheetname=GOOGLE_SHEET_NAME, exercise=exercise,
                  duration=duration, calories=calories)
