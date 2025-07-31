import requests
import os
from config import get_weather_api_key

BASE_URL = "https://api.openweathermap.org/data/2.5"

def get_current_weather(city: str) -> dict:
    """
    Fetches current weather data for a given city.
    Returns JSON response or None if failed.
    """
    api_key = get_weather_api_key()
    url = f"{BASE_URL}/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            return data
        else:
            print(f"❌ Error fetching current weather: {data.get('message')}")
            return None
    except Exception as e:
        print(f"❌ Exception occurred while fetching current weather: {e}")
        return None

def get_forecast(city: str) -> dict:
    """
    Fetches 5-day/3-hour weather forecast for a given city.
    Returns JSON response or None if failed.
    """
    api_key = get_weather_api_key()
    url = f"{BASE_URL}/forecast?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            return data
        else:
            print(f"❌ Error fetching forecast: {data.get('message')}")
            return None
    except Exception as e:
        print(f"❌ Exception occurred while fetching forecast: {e}")
        return None