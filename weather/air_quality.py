import http.client
import json
import urllib.parse  # ✅ For URL encoding
from config import get_rapidapi_key

def get_air_quality(city):
    """
    Fetch air quality data for the given city using the API Ninjas Air Quality API.
    Returns parsed JSON data or None on failure.
    """
    conn = http.client.HTTPSConnection("air-quality-by-api-ninjas.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': get_rapidapi_key(),
        'x-rapidapi-host': "air-quality-by-api-ninjas.p.rapidapi.com"
    }

    try:
        encoded_city = urllib.parse.quote(city)  # ✅ Properly encode city name for URL
        conn.request("GET", f"/v1/airquality?city={encoded_city}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        return json.loads(data.decode("utf-8"))
    except Exception as e:
        print(f"[AirQuality] Error fetching air quality data: {e}")
        return None