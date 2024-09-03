from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Replace 'YOUR_API_KEY' with your actual Google Maps API key
google_maps_api_key =os.getenv('GOOGLE_MAPS_API_KEY')
Weather_api_key =os.getenv('WEATHER_API_KEY')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/weather', methods=['POST'])
def weather():
    zip_code = request.form.get('zip')
    city = request.form.get('city')
    state = request.form.get('state')

    if zip_code:
        lat, lon = get_lat_lon_from_zip(zip_code)
    elif city and state:
        lat, lon = get_lat_lon_from_city_state(city, state)
    else:
        return render_template('home.html', error="Please provide either ZIP code or City and State")


    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={Weather_api_key}&units=imperial'

    response = requests.get(url)
    weather_data = response.json()

    if weather_data.get('cod') != '200':
        error_message = weather_data.get('message', '')
        return render_template('home.html', error=error_message)

    weather = {
        'city': weather_data['city']['name'],
        'temperature': weather_data['list'][0]['main']['temp'],
        'description': weather_data['list'][0]['weather'][0]['description'],
        'icon': weather_data['list'][0]['weather'][0]['icon'],
    }

    return render_template('result.html', weather=weather)

def get_lat_lon_from_zip(zip_code):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={zip_code}&key={google_maps_api_key}'
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        return None, None

def get_lat_lon_from_city_state(city, state):
    address = f"{city},{state}"
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={google_maps_api_key}'
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        return None, None

if __name__ == '__main__':
    app.run(debug=True)
