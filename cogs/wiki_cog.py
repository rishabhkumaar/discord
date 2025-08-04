import discord
from discord.ext import commands
from discord.ext.commands import Context, Bot, hybrid_command
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class WikiCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def fetch_summary(self, topic: str, max_lines: int = 2):
        encoded_topic = quote(topic.strip())
        url = f"https://en.wikipedia.org/wiki/{encoded_topic}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException:
            return None, None, None, ":x: Could not retrieve the Wikipedia page."

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.select("div.mw-parser-output > p")

        summary_lines = []
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text:
                summary_lines.extend(text.splitlines())
            if len(summary_lines) >= max_lines:
                break

        image_tag = soup.select_one(".infobox img")
        image_url = f"https:{image_tag['src']}" if image_tag else None

        if not summary_lines:
            return None, None, None, ":warning: No readable summary found."

        return topic.strip(), url, image_url, "\n".join(summary_lines[:max_lines])

    @hybrid_command(name="wiki", description="Get a short Wikipedia summary about a topic.")
    async def wiki(self, ctx: Context, *, topic: str):
        await ctx.defer()
        topic_clean = topic.strip()

        title, url, image_url, summary = self.fetch_summary(topic_clean)

        if not title:
            await ctx.send(summary)
            return

        embed = discord.Embed(
            title=f"📚 {title.title()} — Wikipedia",
            description=summary,
            url=url,
            color=discord.Color.from_rgb(255, 215, 0),  # Gold tone
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)
        if image_url:
            embed.set_thumbnail(url=image_url)

        await ctx.send(embed=embed)

async def setup(bot: Bot):
    await bot.add_cog(WikiCog(bot))
