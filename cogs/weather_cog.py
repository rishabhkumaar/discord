import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
import pytz

from weather.fetcher import get_current_weather, get_forecast
from weather.formatter import format_current_weather, format_forecast, generate_weather_tip

def convert_to_ist(dt_utc):
    ist = pytz.timezone("Asia/Kolkata")
    return dt_utc.astimezone(ist).strftime("%b %d, %Y | %I:%M %p IST")

def get_weather_emoji(condition: str) -> str:
    condition = condition.lower()
    if "clear" in condition:
        return "☀️"
    elif "cloud" in condition:
        return "☁️"
    elif "rain" in condition:
        return "🌧️"
    elif "thunder" in condition:
        return "⛈️"
    elif "snow" in condition:
        return "❄️"
    elif "mist" in condition or "fog" in condition:
        return "🌫️"
    elif "wind" in condition:
        return "🌪️"
    else:
        return "🌡️"

class WeatherCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="weather", description="Get detailed weather and forecast.")
    @app_commands.describe(city="City name, or use 'lat:<value> lon:<value>' for coordinates.")
    async def weather(self, ctx: commands.Context, *, city: str = "Muzaffarpur"):
        await ctx.defer()

        # Check for lat/lon override
        lat = lon = None
        if "lat:" in city and "lon:" in city:
            try:
                lat = float(city.split("lat:")[1].split()[0])
                lon = float(city.split("lon:")[1].split()[0])
                city = None
            except ValueError:
                return await ctx.reply("❌ Invalid `lat:` or `lon:` format. Use `lat:<value> lon:<value>`.")
        
        current = get_current_weather(city=city, lat=lat, lon=lon)
        forecast = get_forecast(city=city, lat=lat, lon=lon)

        if not current:
            return await ctx.reply("❌ Failed to fetch weather. Please check your input or try again.")

        # Emoji based on weather condition
        condition = current['weather'][0]['description']
        emoji = get_weather_emoji(condition)

        # IST time conversion
        dt_ist = convert_to_ist(datetime.utcfromtimestamp(current['dt']))

        # Basic data
        temp = round(current['main']['temp'])
        feels_like = round(current['main']['feels_like'])
        humidity = current['main']['humidity']
        wind_speed = current['wind']['speed']
        pressure = current['main']['pressure']
        visibility_km = current.get('visibility', 0) / 1000

        weather_desc = (
            f"{emoji} **{condition.title()}**\n"
            f"🌡️ Temp: `{temp}°C` | Feels like: `{feels_like}°C`\n"
            f"💧 Humidity: `{humidity}%` | 💨 Wind: `{wind_speed} m/s`\n"
            f"🧭 Pressure: `{pressure} hPa` | 👁️ Visibility: `{visibility_km} km`\n"
            f"🕒 Last updated: `{dt_ist}`"
        )

        tip = generate_weather_tip(current)

        embed = discord.Embed(
            title=f"{emoji} Weather in {current['name']}",
            description=f"{weather_desc}\n\n{tip}",
            color=discord.Color.blurple()
        )

        icon_code = current['weather'][0]['icon']
        embed.set_thumbnail(url=f"https://openweathermap.org/img/wn/{icon_code}@2x.png")
        embed.set_footer(text="Powered by OpenWeatherMap")

        await ctx.reply(embed=embed)

        if forecast:
            forecast_msg = format_forecast(forecast)
            await ctx.send(f"📅 **Forecast:**\n{forecast_msg}")
        else:
            await ctx.send("⚠️ No forecast data available.")

async def setup(bot: commands.Bot):
    await bot.add_cog(WeatherCog(bot))