import discord
from discord.ext import commands
import random

class MemeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command with cooldown (per user)
    @commands.command(name="meme", help="Steal someone's name and roast them 💀")
    @commands.cooldown(1, 10, commands.BucketType.user)  # 1 use per 10 sec per user
    async def meme(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("🧐 You gotta tag someone to meme! Try `!meme @someone`.")
            return

        original = member.display_name
        twisted = self._twist_name(original)

        # Choose a joke pack
        joke_templates = [
            [
                f"🎭 Meme upload complete. **{original}** just got roasted.",
                f"💡 New alias: **{twisted}**.",
                "📞 Calling the FBI now... oops, too late. 🚓💨"
            ],
            [
                f"🧠 Downloaded brain data of **{original}**...",
                f"🔁 Rebooted as: **{twisted}** 2.0.",
                "💀 You’re legally a meme now."
            ],
            [
                f"🥷 Just borrowed **{original}**'s personality.",
                f"🧬 Rebranded to: **{twisted}**.",
                "📦 Packaging meme... Delivered to Area 51. 🛸"
            ]
        ]

        jokes = random.choice(joke_templates)
        embed = discord.Embed(
            title="🕵️ Meme Heist In Progress...",
            description="\n".join(jokes),
            color=random.choice([
                discord.Color.blurple(),
                discord.Color.red(),
                discord.Color.green(),
                discord.Color.gold()
            ])
        )

        embed.set_footer(text=f"Initiated by {ctx.author.display_name}")
        embed.set_thumbnail(url=member.display_avatar.url)

        await ctx.send(embed=embed)

    def _twist_name(self, name: str) -> str:
        """Generate a funny twist on the original name."""
        suffixes = ["inator", "zilla", "master3000", "the_fake", "bot.exe", "sus", "v2", "jr", "the_third"]
        emojis = ["😈", "🧠", "💀", "🛸", "🎭", "🔥"]

        # Transform name
        core = name.lower().replace(" ", "")[:8]
        twist = core[::-1].capitalize()
        return twist + random.choice(suffixes) + " " + random.choice(emojis)

async def setup(bot):
    await bot.add_cog(MemeCog(bot))
