from datetime import datetime
import pytz

# -----------------------------
# 📦 WEATHER FORMATTERS
# -----------------------------

def format_current_weather(data: dict) -> str:
    """
    Formats current weather data into a clean, readable message.
    """
    if not data:
        return "⚠️ Unable to retrieve current weather data."

    main = data["main"]
    weather = data["weather"][0]
    wind = data["wind"]
    sys = data["sys"]
    coord = data["coord"]

    emoji = get_weather_emoji(weather["main"])

    return (
        f"**🌤️ Current Weather Overview**\n"
        f"{emoji} **{weather['description'].capitalize()}**\n"
        f"> 🌡️ Temperature: `{main['temp']}°C` (Feels like `{main['feels_like']}°C`)\n"
        f"> 💧 Humidity: `{main['humidity']}%` | 🔵 Pressure: `{main['pressure']} hPa`\n"
        f"> ☁️ Cloudiness: `{data['clouds']['all']}%`\n"
        f"> 🌬️ Wind: `{wind['speed']} km/h` (Gusts: `{wind.get('gust', 0)} km/h`)\n"
        f"> 🌅 Sunrise: `{timestamp_to_time(sys['sunrise'])}` | 🌇 Sunset: `{timestamp_to_time(sys['sunset'])}`\n"
        f"> 📍 Location: `Lat {coord['lat']} / Lon {coord['lon']}`\n"
        f"> 🕒 Last updated: `{timestamp_to_datetime(data['dt'])}`"
    )

def format_forecast(data: dict, count: int = 3) -> str:
    """
    Formats forecast data for the next few intervals.
    """
    if not data or "list" not in data:
        return "⚠️ Unable to retrieve forecast data."

    lines = ["**📅 Forecast Snapshot:**"]
    for entry in data["list"][:count]:
        time = timestamp_to_time(entry["dt"])
        temp = entry["main"]["temp"]
        humidity = entry["main"]["humidity"]
        description = entry["weather"][0]["description"].capitalize()
        emoji = get_weather_emoji(entry["weather"][0]["main"])
        lines.append(f"> {emoji} **{time}** — `{temp}°C`, `{humidity}%` humidity, {description}")

    return "\n".join(lines)

def generate_weather_tip(data: dict) -> str:
    """
    Provides context-aware weather advice.
    """
    if not data:
        return ""

    temp = data["main"]["temp"]
    condition = data["weather"][0]["main"].lower()
    tips = []

    if temp >= 35:
        tips.append("Stay hydrated. Avoid direct sunlight.")
    elif temp <= 5:
        tips.append("Wear warm clothes. It's freezing!")

    if "rain" in condition:
        tips.append("Carry an umbrella. Rain expected.")
    elif "snow" in condition:
        tips.append("Snowfall ahead. Wear boots and stay warm.")
    elif "thunder" in condition:
        tips.append("Thunderstorm alert. Best to stay indoors.")
    elif "clear" in condition:
        tips.append("Perfect weather outside. Enjoy your day!")

    return "💡 **Pro Tip:** " + " ".join(tips) if tips else ""

def get_weather_emoji(condition: str) -> str:
    """
    Maps weather conditions to corresponding emojis.
    """
    condition = condition.lower()
    return {
        "clear": "☀️",
        "cloud": "☁️",
        "rain": "🌧️",
        "thunder": "⛈️",
        "drizzle": "🌦️",
        "snow": "❄️",
        "mist": "🌫️",
        "fog": "🌫️",
        "haze": "🌫️",
        "smoke": "🚬",
        "dust": "🏜️",
        "sand": "🏜️",
    }.get(condition, "🌡️")

# -----------------------------
# 🕒 TIME UTILITIES (IST Support)
# -----------------------------

def timestamp_to_time(ts: int) -> str:
    ist = pytz.timezone("Asia/Kolkata")
    return datetime.fromtimestamp(ts, ist).strftime('%I:%M %p')

def timestamp_to_datetime(ts: int) -> str:
    ist = pytz.timezone("Asia/Kolkata")
    return datetime.fromtimestamp(ts, ist).strftime('%Y-%m-%d %I:%M %p')

# -----------------------------
# 🌫️ AIR QUALITY FORMATTERS
# -----------------------------

def get_aqi_level_and_tip(aqi: int) -> tuple[str, str]:
    if aqi <= 50:
        return ("🟢 Good", "Air quality is excellent.")
    elif aqi <= 100:
        return ("🟡 Moderate", "Safe for most, but limit long outdoor exposure if sensitive.")
    elif aqi <= 150:
        return ("🟠 Unhealthy for Sensitive Groups", "People with breathing issues should avoid long outdoor activity.")
    elif aqi <= 200:
        return ("🔴 Unhealthy", "Avoid extended outdoor exposure. Wear a mask if needed.")
    elif aqi <= 300:
        return ("🟣 Very Unhealthy", "Stay indoors and use an air purifier if possible.")
    else:
        return ("⚫ Hazardous", "Avoid outdoor activity. Seek medical help if symptoms appear.")

def format_air_quality(data: dict) -> str:
    if not data:
        return "⚠️ Unable to retrieve air quality data."

    aqi = data.get("overall_aqi", "N/A")
    level, tip = get_aqi_level_and_tip(aqi)

    pollutants = {
        "PM2.5": data.get("PM2.5", {}).get("concentration", "N/A"),
        "PM10": data.get("PM10", {}).get("concentration", "N/A"),
        "CO": data.get("CO", {}).get("concentration", "N/A"),
        "SO₂": data.get("SO2", {}).get("concentration", "N/A"),
        "NO₂": data.get("NO2", {}).get("concentration", "N/A"),
        "O₃": data.get("O3", {}).get("concentration", "N/A"),
    }

    emoji_map = {
        "PM2.5": "🟤", "PM10": "⚪", "CO": "🟡",
        "SO₂": "🔴", "NO₂": "🔵", "O₃": "🟢"
    }

    unit_map = {
        "PM2.5": "μg/m³", "PM10": "μg/m³",
        "CO": "ppb", "SO₂": "ppb", "NO₂": "ppb", "O₃": "ppb"
    }

    lines = [
        "**🌫️ Air Quality Overview**",
        f"> **AQI**: `{aqi}` — {level}",
        f"> 💡 {tip}",
        "",
        "**📊 Pollutant Breakdown:**"
    ]

    for name, value in pollutants.items():
        emoji = emoji_map.get(name, "🔸")
        unit = unit_map.get(name, "")
        lines.append(f"> {emoji} **{name}**: `{value} {unit}`")

    return "\n".join(lines)
