import discord
from discord.ext import commands
from discord import app_commands

from weather.air_quality import get_air_quality
from weather.formatter import format_air_quality
from config import load_env

load_env()  # Load environment variables

class AirQuality(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Slash command
    @app_commands.command(name="air", description="Get real-time air quality data for a city.")
    @app_commands.describe(city="The name of the city to check air quality for")
    async def air_slash(self, interaction: discord.Interaction, city: str):
        await interaction.response.defer()
        await self.send_air_quality(interaction, city, is_slash=True)

    # Text command
    @commands.command(name="air", help="Get air quality data for a city. Usage: !air <city>")
    async def air_text(self, ctx: commands.Context, *, city: str = None):
        if not city:
            await ctx.send("❌ Please provide a city name.\n**Example:** `!air Delhi`")
            return
        await self.send_air_quality(ctx, city, is_slash=False)

    # Shared logic
    async def send_air_quality(self, context, city: str, is_slash: bool):
        city_cleaned = city.strip().title()

        try:
            data = get_air_quality(city_cleaned)
        except Exception as e:
            content = f"⚠️ An error occurred while fetching air quality data for **{city_cleaned}**."
        else:
            if not data:
                content = f"⚠️ Couldn't retrieve air quality data for **{city_cleaned}**."
            else:
                content = f"📍 **Air Quality in {city_cleaned}**\n\n{format_air_quality(data)}"

        if is_slash:
            await context.followup.send(content)
        else:
            await context.send(content)

# Register the cog
async def setup(bot: commands.Bot):
    await bot.add_cog(AirQuality(bot))