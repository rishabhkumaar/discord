import discord
from discord.ext import commands
import requests
from urllib.parse import quote

class WikiDebug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="wikidebug", description="Fetch raw Wikipedia HTML for debugging")
    async def wikidebug(self, ctx, *, topic: str):
        await ctx.defer()

        encoded_topic = quote(topic.strip())
        url = f"https://en.wikipedia.org/wiki/{encoded_topic}"

        try:
            response = requests.get(url, timeout=10)
        except requests.exceptions.RequestException as e:
            await ctx.send(f":x: Request failed: `{e}`")
            return

        if response.status_code != 200:
            await ctx.send(f":x: Wikipedia returned status code {response.status_code}")
            return

        html_data = response.text

        # Print to console for debugging
        print("\n=== RAW HTML START ===\n")
        print(html_data[:2000])  # First 2000 characters
        print("\n=== RAW HTML END ===\n")

        await ctx.send(f"✅ Fetched {len(html_data)} characters from Wikipedia for `{topic}`.\nURL: {url}")

async def setup(bot):
    await bot.add_cog(WikiDebug(bot))