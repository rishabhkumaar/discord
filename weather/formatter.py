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

def get_weather_emoji(condition):
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


def format_current_weather(data):
    main = data['main']
    weather = data['weather'][0]
    wind = data['wind']
    sys = data['sys']
    coord = data['coord']

    emoji = get_weather_emoji(weather['main'])

    return (
        f"{emoji} **{weather['description'].capitalize()}**\n"
        f"🌡️ Temperature: {main['temp']}°C (Feels like {main['feels_like']}°C)\n"
        f"💧 Humidity: {main['humidity']}%\n"
        f"🌬️ Wind Speed: {wind['speed']} m/s\n"
        f"📍 Coordinates: [Lat: {coord['lat']}, Lon: {coord['lon']}]\n"
        f"🌅 Sunrise: <t:{sys['sunrise']}:t> | 🌇 Sunset: <t:{sys['sunset']}:t>"
    )


def format_forecast(data):
    forecast_text = "**Next Forecast Intervals:**\n"
    for item in data['list'][:4]:
        weather = item['weather'][0]
        emoji = get_weather_emoji(weather['main'])

        forecast_text += (
            f"{emoji} `{item['dt_txt']}`: {weather['description'].capitalize()}, "
            f"{item['main']['temp']}°C\n"
        )
    return forecast_text


def generate_weather_tip(current):
    temp = current['main']['temp']
    condition = current['weather'][0]['main'].lower()

    if temp >= 35:
        return "🔥 It's really hot! Stay hydrated."
    elif temp <= 5:
        return "🧊 It's freezing! Dress warmly."
    elif "rain" in condition:
        return "☔ Carry an umbrella — it's rainy!"
    elif "snow" in condition:
        return "❄️ Wear boots — snow expected."
    elif "thunder" in condition:
        return "⚡ Thunderstorms possible — stay indoors."
    else:
        return "✅ Weather looks fine. Enjoy your day!"