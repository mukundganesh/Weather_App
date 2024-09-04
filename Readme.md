# Weather App

## Introduction
Weather App is a Python Flask application that provides real-time weather updates based on the user's location. Users enter their ZIP code, and the application uses both OpenWeather and Google Maps APIs to fetch and display the weather information.

## Features
- Get real-time weather updates by entering a ZIP code or Name of the City and State.
- Displays detailed weather information such as temperature, humidity, weather conditions, and more.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Flask
- Requests library

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Weather_App.git

2. Navigate to the project directory:
   ```bash
   cd Weather_App
   
3. Install the required packages:
   ```bash
   pip install -r requirements.txt

# API Keys

This application requires API keys from OpenWeather and Google Maps:

## Obtaining the API Keys

### OpenWeather API Key:

1. Sign up or log in at [OpenWeatherMap](https://openweathermap.org/).
2. Navigate to the 'API keys' tab and generate a new API key.

### Google Maps API Key:

1. Visit [Google Cloud Platform](https://cloud.google.com/).
2. Create a new project and enable the Maps  Geocoding API.
3. Navigate to the 'Credentials' page and click on 'Create Credentials' to generate a new API key.

## Configuration

After obtaining the keys, create a `.env` file in the root directory of your project and add the following entries:

```makefile
WEATHER_API_KEY=your_openweather_api_key_here
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

## Running the Application

To start the server, run the following command in your terminal:

```bash
python app.py
```

Open a web browser and navigate to http://127.0.0.1:5000/ to use the application.

``` css
This Markdown text provides clear instructions for starting the application server and accessing it via a web browser. It uses a code block for the command to run the application, enhancing clarity and usability.
```