import discord
from discord.ext import commands
from discord.ext.commands import Context, Bot, hybrid_command

class MutualGuilds(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.owner_id = 1177102238490050641  # Rishabh's user ID

    @hybrid_command(name="mutual", description="See mutual servers between you and another user.")
    async def mutual(self, ctx: Context, user: discord.User):
        if ctx.author.id != self.owner_id:
            return await ctx.reply("❌ Only the bot owner can use this command.")

        mutual_guilds = []
        for guild in self.bot.guilds:
            if guild.get_member(user.id) and guild.get_member(self.owner_id):
                invite = None
                # Try to get an existing invite if possible
                try:
                    invites = await guild.invites()
                    if invites:
                        invite = invites[0].url
                except:
                    pass

                mutual_guilds.append((guild.name, invite))

        if not mutual_guilds:
            return await ctx.reply("🔍 No mutual servers found between you and that user.")

        embed = discord.Embed(
            title=f"🔗 Mutual Servers with {user}",
            description="Here are the servers you both share:",
            color=discord.Color.blue()
        )

        for name, invite in mutual_guilds:
            display = f"[{name}]({invite})" if invite else name
            embed.add_field(name="Server", value=display, inline=False)

        await ctx.reply(embed=embed)

async def setup(bot: Bot):
    await bot.add_cog(MutualGuilds(bot))
