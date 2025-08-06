import discord
from discord.ext import commands
from discord.ext.commands import Context, Bot, hybrid_command
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


class WikiPagination(discord.ui.View):
    def __init__(self, ctx: Context, pages: list[str], embed_base: discord.Embed):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.pages = pages
        self.embed_base = embed_base
        self.current_page = 0

    async def update_embed(self, interaction: discord.Interaction):
        embed = self.embed_base.copy()
        embed.description = self.pages[self.current_page]
        embed.set_footer(
            text=f"Page {self.current_page + 1}/{len(self.pages)} • Requested by {self.ctx.author.display_name}",
            icon_url=self.ctx.author.display_avatar.url
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="⬅️ Previous", style=discord.ButtonStyle.primary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_embed(interaction)

    @discord.ui.button(label="➡️ Next", style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            await self.update_embed(interaction)

    @discord.ui.button(label="🛑 Stop", style=discord.ButtonStyle.danger)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()
        self.stop()


class WikiCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def clean_text(self, text: str) -> str:
        # Remove references like [1], [a], etc.
        text = re.sub(r'\[[^\]]*\]', '', text)
        text = re.sub(r'\s{2,}', ' ', text)  # Collapse multiple spaces
        return text.strip()

    def split_into_sentences(self, text: str, max_sentences: int = 3) -> str:
        sentences = re.split(r'(?<=[.?!])\s+', text)
        return " ".join(sentences[:max_sentences])

    def split_text_into_pages(self, text: str, max_chars: int = 4096):
        sentences = re.split(r'(?<=[.?!])\s+', text)
        pages = []
        current = ""

        for sentence in sentences:
            if len(current) + len(sentence) + 1 > max_chars:
                pages.append(current.strip())
                current = sentence + " "
            else:
                current += sentence + " "

        if current.strip():
            pages.append(current.strip())

        return pages

    def fetch_summary(self, topic: str, detailed: bool = False):
        encoded_topic = quote(topic.strip())
        url = f"https://en.wikipedia.org/wiki/{encoded_topic}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException:
            return None, None, None, ":x: Could not retrieve the Wikipedia page."

        soup = BeautifulSoup(response.text, "html.parser")

        # Disambiguation check
        if soup.find("table", {"id": "disambigbox"}):
            return None, None, None, ":warning: Disambiguation page detected. Try a more specific term."

        paragraphs = soup.select("div.mw-parser-output > p")
        summary_text = ""

        for p in paragraphs:
            text = self.clean_text(p.get_text())
            if text and not text.lower().startswith(("pronunciation", "may refer to", "can refer to")):
                summary_text += " " + text
                if not detailed and len(summary_text.split('. ')) >= 3:
                    break

        if not summary_text.strip():
            return None, None, None, ":warning: No readable summary found."

        if not detailed:
            summary_text = self.split_into_sentences(summary_text, 3)

        image_tag = soup.select_one(".infobox img")
        image_url = f"https:{image_tag['src']}" if image_tag else None

        return topic.strip(), url, image_url, summary_text.strip()

    @hybrid_command(name="wiki", description="🔍 Get a short or detailed Wikipedia summary.")
    async def wiki(self, ctx: Context, *, query: str):
        await ctx.defer()

        # Allow input like "india detail:true"
        if "detail:" in query:
            parts = query.split("detail:")
            topic = parts[0].strip()
            detailed = parts[1].strip().lower() in ["true", "yes", "1"]
        else:
            topic = query.strip()
            detailed = False

        title, url, image_url, summary = self.fetch_summary(topic, detailed)

        if not title:
            await ctx.send(summary)
            return

        pages = self.split_text_into_pages(summary)
        base_embed = discord.Embed(
            title=f"📘 {title.title()}",
            url=url,
            color=discord.Color.blurple(),
            timestamp=datetime.utcnow()
        ).set_author(
            name="Wikipedia",
            icon_url="https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png"
        )

        if image_url:
            base_embed.set_thumbnail(url=image_url)

        base_embed.description = pages[0]
        base_embed.set_footer(
            text=f"Page 1/{len(pages)} • Requested by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url
        )

        if len(pages) == 1:
            await ctx.send(embed=base_embed)
        else:
            view = WikiPagination(ctx, pages, base_embed)
            await ctx.send(embed=base_embed, view=view)


async def setup(bot: Bot):
    await bot.add_cog(WikiCog(bot))