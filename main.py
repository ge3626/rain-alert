import requests
from twilio.rest import Client
import os
import json

admin_info = os.getenv('ADMIN_JSON_INFO')
with open(admin_info, 'r') as file:
    contents = file.read()
    admin_json_info = json.loads(contents)

weather_apikey = admin_json_info['weather']['api_key']
account_sid = admin_json_info['twilio']['account_sid']
auth_token = admin_json_info['twilio']['auth_token']

CITYNAME = "Seoul"

geocoding_params = {
    "q": CITYNAME,
    "appid": weather_apikey
}
response = requests.get("http://api.openweathermap.org/geo/1.0/direct", params=geocoding_params)
geological_data = response.json()
latitude = geological_data[0]['lat']
longitude = geological_data[0]['lon']

parameter = {
    "lat": latitude,
    "lon": longitude,
    "appid": weather_apikey,
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=parameter)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["list"][:12]

is_rain = False

for hour_data in weather_slice:
    condition_code = hour_data['weather'][0]["id"]
    if int(condition_code) < 700:
        is_rain = True

if is_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It's going to rain today. Bring your umbrella!☂️",
        from_=admin_json_info['twilio']['phone_number'],
        to=admin_json_info['twilio']['my_phone_number']
    )
    print(message.status)
