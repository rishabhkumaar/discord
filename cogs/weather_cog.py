import discord
from discord.ext import commands
from discord import app_commands

from weather.fetcher import get_current_weather, get_forecast
from weather.formatter import format_current_weather, format_forecast, generate_weather_tip

class WeatherCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Hybrid command: works with both !weather and /weather
    @commands.hybrid_command(name="weather", description="Get current weather and forecast for a city.")
    @app_commands.describe(city="Name of the city to get weather for")
    async def weather(self, ctx: commands.Context, city: str = "Muzaffarpur"):
        """
        Fetches and displays current weather and short forecast for a city.
        Works with both !weather and /weather.
        """
        await ctx.defer()  # Show "Bot is thinking..." for slash commands

        current = get_current_weather(city)
        forecast = get_forecast(city)

        if not current:
            await ctx.reply(f"❌ Couldn't fetch weather for `{city}`. Please try a valid city.")
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

        await ctx.reply(embed=embed)
        await ctx.send(forecast_msg)

async def setup(bot: commands.Bot):
    await bot.add_cog(WeatherCog(bot))