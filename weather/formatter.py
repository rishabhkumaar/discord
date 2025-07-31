from datetime import datetime

def format_current_weather(data: dict) -> str:
    """
    Formats current weather data into a readable message.
    """
    if not data:
        return "⚠️ Couldn't retrieve current weather data."

    name = data.get("name", "Unknown location")
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    clouds = data["clouds"]["all"]
    wind = data["wind"]["speed"]
    gust = data["wind"].get("gust", 0)
    condition = data["weather"][0]["description"].capitalize()
    icon = data["weather"][0]["icon"]

    sunrise = timestamp_to_time(data["sys"]["sunrise"])
    sunset = timestamp_to_time(data["sys"]["sunset"])
    updated = timestamp_to_datetime(data["dt"])

    lat = data["coord"]["lat"]
    lon = data["coord"]["lon"]

    return (
        f"**🌍 Weather for {name}**\n"
        f"> **Condition:** {condition}\n"
        f"> **Temperature:** {temp}°C (Feels like {feels_like}°C)\n"
        f"> **Humidity:** {humidity}%\n"
        f"> **Pressure:** {pressure} hPa\n"
        f"> **Cloud Coverage:** {clouds}%\n"
        f"> **Wind:** {wind} km/h (Gusts: {gust} km/h)\n"
        f"> **Sunrise:** {sunrise} | **Sunset:** {sunset}\n"
        f"> **Coordinates:** {lat}, {lon}\n"
        f"> *Last updated:* {updated}"
    )

def format_forecast(data: dict, count: int = 3) -> str:
    """
    Formats upcoming forecast entries (default: next 3 intervals).
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
        lines.append(f"> **{time}** — {temp}°C, {humidity}% humidity, {description}")

    return "\n".join(lines)

def generate_weather_tip(data: dict) -> str:
    """
    Returns a message with advice based on weather condition and temperature.
    """
    if not data:
        return ""

    temp = data["main"]["temp"]
    condition = data["weather"][0]["main"].lower()
    tips = []

    if temp > 30:
        tips.append("It’s quite hot. Stay hydrated and avoid direct sun.")
    elif temp < 10:
        tips.append("It’s cold. Dress warmly.")

    if "rain" in condition:
        tips.append("Carry an umbrella – it looks rainy.")
    elif "snow" in condition:
        tips.append("It might snow. Stay warm and drive safely.")
    elif "clear" in condition:
        tips.append("Clear skies – great time to go outside!")

    return "💡 **Tip:** " + " ".join(tips) if tips else ""

def timestamp_to_time(ts: int) -> str:
    return datetime.fromtimestamp(ts).strftime('%I:%M %p')

def timestamp_to_datetime(ts: int) -> str:
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %I:%M %p')