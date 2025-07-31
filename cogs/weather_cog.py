import discord
from discord.ext import commands
from weather.fetcher import get_current_weather, get_forecast
from weather.formatter import format_current_weather, format_forecast, generate_weather_tip

class WeatherCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="weather")
    async def weather(self, ctx, *, city: str = "Muzaffarpur"):
        """
        Fetches and displays current weather and short forecast for a city.
        Usage: /weather [city name]
        """
        await ctx.send(f"🌦️ Fetching weather for **{city}**...")

        current = get_current_weather(city)
        forecast = get_forecast(city)

        if not current:
            await ctx.send(f"❌ Couldn't fetch weather for `{city}`. Please try a valid city.")
            return

        weather_msg = format_current_weather(current)
        tip_msg = generate_weather_tip(current)
        forecast_msg = format_forecast(forecast)

        embed = discord.Embed(title=f"Weather for {city}", color=0x3498db)
        embed.description = weather_msg + "\n\n" + tip_msg
        embed.set_footer(text="Powered by OpenWeatherMap")

        icon_code = current['weather'][0]['icon']
        icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
        embed.set_thumbnail(url=icon_url)

        await ctx.send(embed=embed)
        await ctx.send(forecast_msg)

async def setup(bot):
    await bot.add_cog(WeatherCog(bot))
