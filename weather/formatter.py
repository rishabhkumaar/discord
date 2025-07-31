from datetime import datetime

# -----------------------------
# 📦 WEATHER FORMATTERS
# -----------------------------

def format_current_weather(data: dict) -> str:
    """
    Formats current weather data into a clean, readable message with emoji.
    """
    if not data:
        return "⚠️ Couldn't retrieve current weather data."

    main = data["main"]
    weather = data["weather"][0]
    wind = data["wind"]
    sys = data["sys"]
    coord = data["coord"]

    emoji = get_weather_emoji(weather["main"])
    return (
        f"{emoji} **{weather['description'].capitalize()}**\n"
        f"🌡️ Temperature: {main['temp']}°C (Feels like {main['feels_like']}°C)\n"
        f"💧 Humidity: {main['humidity']}%\n"
        f"🔵 Pressure: {main['pressure']} hPa\n"
        f"☁️ Cloud Coverage: {data['clouds']['all']}%\n"
        f"🌬️ Wind: {wind['speed']} km/h (Gusts: {wind.get('gust', 0)} km/h)\n"
        f"🌅 Sunrise: {timestamp_to_time(sys['sunrise'])} | 🌇 Sunset: {timestamp_to_time(sys['sunset'])}\n"
        f"📍 Coordinates: [Lat: {coord['lat']}, Lon: {coord['lon']}]\n"
        f"🕒 Last updated: {timestamp_to_datetime(data['dt'])}"
    )


def format_forecast(data: dict, count: int = 3) -> str:
    """
    Formats forecast data for the next few intervals.
    """
    if not data or "list" not in data:
        return "⚠️ Couldn't retrieve forecast data."

    entries = data["list"][:count]
    lines = ["**📅 Forecast (next few intervals):**"]
    for entry in entries:
        time = timestamp_to_time(entry["dt"])
        temp = entry["main"]["temp"]
        humidity = entry["main"]["humidity"]
        description = entry["weather"][0]["description"].capitalize()
        emoji = get_weather_emoji(entry["weather"][0]["main"])

        lines.append(f"{emoji} **{time}** — {temp}°C, {humidity}% humidity, {description}")

    return "\n".join(lines)


def generate_weather_tip(data: dict) -> str:
    """
    Gives basic advice based on the temperature and weather condition.
    """
    if not data:
        return ""

    temp = data["main"]["temp"]
    condition = data["weather"][0]["main"].lower()
    tips = []

    if temp >= 35:
        tips.append("🔥 It's extremely hot! Stay hydrated and avoid going out.")
    elif temp <= 5:
        tips.append("🧊 It's freezing! Dress warmly and stay indoors if possible.")

    if "rain" in condition:
        tips.append("☔ Take an umbrella, it's rainy.")
    elif "snow" in condition:
        tips.append("❄️ Snow expected. Wear boots and warm layers.")
    elif "thunder" in condition:
        tips.append("⚡ Thunderstorm alert! Stay inside.")
    elif "clear" in condition:
        tips.append("🌞 Clear skies — a good time to go out!")

    return "💡 **Tip:** " + " ".join(tips) if tips else ""


def get_weather_emoji(condition: str) -> str:
    """
    Maps weather conditions to emojis.
    """
    condition = condition.lower()
    if "clear" in condition:
        return "☀️"
    elif "cloud" in condition:
        return "☁️"
    elif "rain" in condition:
        return "🌧️"
    elif "thunder" in condition:
        return "⛈️"
    elif "drizzle" in condition:
        return "🌦️"
    elif "snow" in condition:
        return "❄️"
    elif "mist" in condition or "fog" in condition or "haze" in condition:
        return "🌫️"
    elif "smoke" in condition:
        return "🚬"
    elif "dust" in condition or "sand" in condition:
        return "🏜️"
    else:
        return "🌡️"

# -----------------------------
# 🕒 UTILITIES
# -----------------------------

def timestamp_to_time(ts: int) -> str:
    return datetime.fromtimestamp(ts).strftime('%I:%M %p')


def timestamp_to_datetime(ts: int) -> str:
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %I:%M %p')


# -----------------------------
# 🌫️ AIR QUALITY FORMATTER
# -----------------------------

def format_air_quality(data: dict) -> str:
    """
    Formats air quality data into a Discord-friendly message.
    """
    if not data:
        return "⚠️ Couldn't retrieve air quality data."

    aqi = data.get("overall_aqi")
    pm25 = data.get("PM2.5", {}).get("concentration", "N/A")
    pm10 = data.get("PM10", {}).get("concentration", "N/A")
    co = data.get("CO", {}).get("concentration", "N/A")
    no2 = data.get("NO2", {}).get("concentration", "N/A")
    o3 = data.get("O3", {}).get("concentration", "N/A")

    health = interpret_aqi(aqi)

    return (
        f"**🌫️ Air Quality Index (AQI):** {aqi} — {health}\n"
        f"> 🟤 PM2.5: {pm25} μg/m³\n"
        f"> ⚪ PM10: {pm10} μg/m³\n"
        f"> 🟡 CO: {co} μg/m³\n"
        f"> 🔵 NO₂: {no2} μg/m³\n"
        f"> 🟢 O₃: {o3} μg/m³"
    )

def interpret_aqi(aqi: int) -> str:
    if aqi <= 50:
        return "Good 😊"
    elif aqi <= 100:
        return "Moderate 😐"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups 🤧"
    elif aqi <= 200:
        return "Unhealthy 😷"
    elif aqi <= 300:
        return "Very Unhealthy 🤢"
    else:
        return "Hazardous ☠️"

def get_aqi_level_and_tip(aqi: int) -> tuple[str, str]:
    """
    Returns the AQI level and a safety tip based on the overall AQI.
    """
    if aqi <= 50:
        return ("🟢 Good", "Air quality is great. Enjoy your day!")
    elif aqi <= 100:
        return ("🟡 Moderate", "Air is okay, but sensitive people should limit long outdoor exposure.")
    elif aqi <= 150:
        return ("🟠 Unhealthy for Sensitive Groups", "Children, elderly, and people with conditions should avoid long outdoor activity.")
    elif aqi <= 200:
        return ("🔴 Unhealthy", "Limit outdoor activity. Wear a mask if needed.")
    elif aqi <= 300:
        return ("🟣 Very Unhealthy", "Avoid going outside. Use air purifiers indoors.")
    else:
        return ("⚫ Hazardous", "Stay indoors. Consider medical attention if symptoms occur.")
