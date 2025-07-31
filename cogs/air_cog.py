import discord
from discord.ext import commands
from discord import app_commands

from weather.air_quality import get_air_quality
from weather.formatter import format_air_quality
from config import load_env

load_env()  # ensure env is loaded

class AirQuality(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash command
    @app_commands.command(name="air", description="Get air quality data for a city")
    @app_commands.describe(city="City name to check air quality")
    async def air_slash(self, interaction: discord.Interaction, city: str):
        await interaction.response.defer()
        await self.send_air_quality(interaction, city, is_slash=True)

    # Text command
    @commands.command(name="air")
    async def air_text(self, ctx: commands.Context, *, city: str = None):
        if not city:
            await ctx.send("❌ Please provide a city name. Example: `!air Delhi`")
            return
        await self.send_air_quality(ctx, city, is_slash=False)

    # Shared logic
    async def send_air_quality(self, context, city: str, is_slash: bool):
        data = get_air_quality(city)
        if not data:
            content = f"⚠️ Couldn't retrieve air quality data for **{city.title()}**."
        else:
            content = f"📍 **Air Quality in {city.title()}**\n" + format_air_quality(data)

        if is_slash:
            await context.followup.send(content)
        else:
            await context.send(content)

# Required to register cog
async def setup(bot):
    await bot.add_cog(AirQuality(bot))