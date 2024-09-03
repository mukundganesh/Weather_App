from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os
from datetime import datetime

app = Flask(__name__)

# Load environment variables
load_dotenv()
google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
weather_api_key = os.getenv('WEATHER_API_KEY')


if not google_maps_api_key or not weather_api_key:
    raise ValueError("Missing API keys. Please check your .env file.")


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/weather', methods=['POST'])
def weather():
    zip_code = request.form.get('zip')
    city = request.form.get('city')
    state = request.form.get('state')

    # Prefer city and state over zip code if both are provided
    if city and state:
        lat, lon = get_lat_lon_from_city_state(city, state)
        location_name = f"{city}, {state}"
    elif zip_code:
        lat, lon, city, state = get_lat_lon_from_zip(zip_code)
        if city and state:
            location_name = f"{city}, {state} (ZIP Code: {zip_code})"
        else:
            location_name = f"ZIP Code: {zip_code}"
    else:
        return render_template('home.html', error="Please provide either a ZIP code or both a City and State")

    if lat is None or lon is None:
        return render_template('home.html', error="Could not detect location. Please check the ZIP code or city/state provided.")

    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={weather_api_key}&units=imperial'

    response = requests.get(url)
    if response.status_code != 200:
        return render_template('home.html', error="Error fetching data from weather service.")

    weather_data = response.json()

    if weather_data.get('cod') != '200':
        error_message = weather_data.get('message', '')
        return render_template('home.html', error=error_message)

    # Extract current weather data (first item in the list)
    current_weather_data = weather_data['list'][0]
    current_weather = {
        'date': datetime.now().strftime("%d %B %Y"),
        'temp_fahrenheit': current_weather_data['main']['temp'],
        'temp_celsius': round((current_weather_data['main']['temp'] - 32) * 5.0 / 9.0, 2),
        'description': current_weather_data['weather'][0]['description'],
        'icon': current_weather_data['weather'][0]['icon'],
        'humidity': current_weather_data['main']['humidity'],
        'wind_speed': current_weather_data['wind']['speed'],
        'rain': current_weather_data['rain']['3h'] if 'rain' in current_weather_data else 0,
        'precipitation_chance': current_weather_data['pop'] * 100 if 'pop' in current_weather_data else 0
    }

    # Extract 5-day forecast data
    forecast_list = []
    for i in range(0, len(weather_data['list']), 8):  # 8 data points per day (3-hour intervals)
        day_data = weather_data['list'][i]
        celsius_temp = (day_data['main']['temp'] - 32) * 5.0 / 9.0
        formatted_date = datetime.strptime(day_data['dt_txt'], "%Y-%m-%d %H:%M:%S").strftime("%d %B %Y")
        day_forecast = {
            'date': formatted_date,
            'temp_fahrenheit': day_data['main']['temp'],
            'temp_celsius': round(celsius_temp, 2),
            'description': day_data['weather'][0]['description'],
            'icon': day_data['weather'][0]['icon'],
            'humidity': day_data['main']['humidity'],
            'wind_speed': day_data['wind']['speed'],
            'rain': day_data['rain']['3h'] if 'rain' in day_data else 0,
            'precipitation_chance': day_data['pop'] * 100 if 'pop' in day_data else 0
        }
        forecast_list.append(day_forecast)

    return render_template('result.html', location_name=location_name, current_weather=current_weather, forecast_list=forecast_list)



@app.route('/info')
def info():
    return render_template('info.html')


def get_lat_lon_from_zip(zip_code):
    try:
        url = f'https://maps.googleapis.com/maps/api/geocode/json?address={zip_code}&key={google_maps_api_key}'
        response = requests.get(url)
        data = response.json()

        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            address_components = data['results'][0]['address_components']

            # Extract city and state
            city = state = None
            for component in address_components:
                if 'locality' in component['types']:
                    city = component['long_name']
                if 'administrative_area_level_1' in component['types']:
                    state = component['short_name']

            return location['lat'], location['lng'], city, state
        else:
            return None, None, None, None
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None, None, None, None




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
