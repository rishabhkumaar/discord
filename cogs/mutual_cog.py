import discord
from discord.ext import commands
from discord.ext.commands import Context, Bot, hybrid_command

class MutualGuilds(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.owner_id = 1177102238490050641  # Rishabh's user ID

    @hybrid_command(name="mutual", description="List mutual servers between you and another user.")
    async def mutual(self, ctx: Context, user: discord.User):
        if ctx.author.id != self.owner_id:
            return await ctx.reply(embed=self._error_embed("❌ Only the bot owner can use this command."))

        if user.bot:
            return await ctx.reply(embed=self._error_embed("🤖 Bots aren't supported for mutual guild lookup."))

        mutual_guilds = []

        for guild in self.bot.guilds:
            me = guild.get_member(self.owner_id)
            target = guild.get_member(user.id)

            if me and target:
                invite_url = None

                try:
                    bot_member = guild.me

                    # Check if bot has Manage Guild and Create Instant Invite
                    perms = guild.me.guild_permissions
                    if perms.manage_guild and perms.create_instant_invite:
                        invites = await guild.invites()

                        if invites:
                            invite_url = invites[0].url
                        else:
                            # Create a new invite from the first available text channel
                            text_channels = [c for c in guild.text_channels if c.permissions_for(bot_member).create_instant_invite]
                            if text_channels:
                                invite = await text_channels[0].create_invite(reason="Mutual command by owner", max_age=0, max_uses=0)
                                invite_url = invite.url
                except Exception:
                    invite_url = None  # silently fail if invite fetching/creation fails

                mutual_guilds.append((guild.name, invite_url))

        if not mutual_guilds:
            return await ctx.reply(embed=self._error_embed(f"🔍 No mutual servers found between you and {user.mention}."))

        embed = discord.Embed(
            title=f"🔗 Mutual Servers with {user}",
            description="Here are the servers you both share:",
            color=discord.Color.blurple()
        )

        for name, invite in mutual_guilds:
            display = f"[{name}]({invite})" if invite else f"{name} *(invite unavailable)*"
            embed.add_field(name="Server", value=display, inline=False)

        await ctx.reply(embed=embed)

    def _error_embed(self, message: str) -> discord.Embed:
        return discord.Embed(
            title="⚠️ Error",
            description=message,
            color=discord.Color.red()
        )

# Register the cog
async def setup(bot: Bot):
    await bot.add_cog(MutualGuilds(bot))