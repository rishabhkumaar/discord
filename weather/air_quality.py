import http.client
import json
import urllib.parse
from config import get_rapidapi_key

# AQI category thresholds and messages
AQI_LEVELS = [
    (0, 50, "Good", "✅ Air quality is good. Enjoy outdoor activities."),
    (51, 100, "Moderate", "⚠️ Acceptable, but some pollutants may affect sensitive people."),
    (101, 150, "Unhealthy for Sensitive Groups", "😷 Reduce prolonged outdoor exertion if sensitive."),
    (151, 200, "Unhealthy", "🚫 Everyone may begin to experience health effects."),
    (201, 300, "Very Unhealthy", "🛑 Health warnings of emergency conditions."),
    (301, 500, "Hazardous", "☠️ Serious health effects. Avoid all outdoor activity."),
]

def get_aqi_level(aqi: float | int):
    """
    Returns the AQI category label and health message.
    """
    for low, high, label, message in AQI_LEVELS:
        if low <= aqi <= high:
            return label, message
    return "Unknown", "⚠️ AQI is out of range. Stay cautious."

def get_air_quality(city: str) -> dict | None:
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
        encoded_city = urllib.parse.quote_plus(city.strip())  # Handles spaces like "new delhi"
        conn.request("GET", f"/v1/airquality?city={encoded_city}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        json_data = json.loads(data.decode("utf-8"))

        if "overall_aqi" not in json_data:
            print(f"[AirQuality] No AQI data for: {city}")
            return None

        # Append level + tip into the response
        label, tip = get_aqi_level(json_data["overall_aqi"])
        json_data["category"] = label
        json_data["tip"] = tip
        return json_data

    except Exception as e:
        print(f"[AirQuality] Error fetching air quality data: {e}")
        return None
