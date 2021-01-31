import requests
import datetime as dt
import os

API_ID = os.environ.get("MY_API_ID")
API_KEY = os.environ.get("MY_XAPP_API_KEY")
GENDER = "female"
WEIGHT = 67.4
HEIGHT = 174
AGE = 26
TOKEN = os.environ.get("MY_TOKEN")
EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

request_header = {
    "x-app-key": API_KEY,
    "x-app-id": API_ID,
}

bearer_header = {
    "Authorization": f"Bearer {TOKEN}"
}

query = input("Tell me which exercise you did: ")

parameters = {
    "query": query,
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE
}

response = requests.post(url=EXERCISE_ENDPOINT, json=parameters, headers=request_header)
data = response.json()
print(data)

date = dt.datetime.now().strftime("%d/%m/%Y")
time = dt.datetime.now().strftime("%H:%M:%S")

sheet_endpoint = os.environ.get("SHEET_ENDPOINT")

for i in (range(len(data["exercises"]))):
    add_rows_param = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": (data["exercises"][i]["name"]).title(),
            "duration": data["exercises"][i]["duration_min"],
            "calories": data["exercises"][i]["nf_calories"]
        }
    }
    response = requests.post(url=sheet_endpoint, json=add_rows_param, headers=bearer_header)
