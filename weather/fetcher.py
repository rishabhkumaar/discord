import requests
from config import get_weather_api_key

BASE_URL = "https://api.openweathermap.org/data/2.5"

def get_current_weather(city: str = None, lat: float = None, lon: float = None) -> dict:
    """
    Fetches current weather data by city name or coordinates.
    Returns JSON response or None if failed.
    """
    api_key = get_weather_api_key()

    if city:
        url = f"{BASE_URL}/weather?q={city}&appid={api_key}&units=metric"
    elif lat is not None and lon is not None:
        url = f"{BASE_URL}/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    else:
        print("❌ No valid city or coordinates provided.")
        return None

    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            return data
        else:
            print(f"❌ Error fetching current weather: {data.get('message', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"❌ Exception occurred while fetching current weather: {e}")
        return None


def get_forecast(city: str = None, lat: float = None, lon: float = None) -> dict:
    """
    Fetches 5-day/3-hour weather forecast by city name or coordinates.
    Returns JSON response or None if failed.
    """
    api_key = get_weather_api_key()

    if city:
        url = f"{BASE_URL}/forecast?q={city}&appid={api_key}&units=metric"
    elif lat is not None and lon is not None:
        url = f"{BASE_URL}/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    else:
        print("❌ No valid city or coordinates provided.")
        return None

    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            return data
        else:
            print(f"❌ Error fetching forecast: {data.get('message', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"❌ Exception occurred while fetching forecast: {e}")
        return None
