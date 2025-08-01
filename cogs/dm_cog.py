import discord
from discord.ext import commands
from discord.ext.commands import Context, Bot, hybrid_command, has_permissions

class DirectMessageCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @hybrid_command(name="dm", description="Send a beautiful DM to a user (admin-only).")
    @has_permissions(administrator=True)
    async def dm(self, ctx: Context, user: discord.User, *, message: str):
        """Sends a stylish embed DM to the specified user."""
        await ctx.defer()  # Defer without ephemeral since it's hybrid

        embed = discord.Embed(
            title="You've got a new message! <:pika_think:1380965597294104656> ",
            description=message,
            color=discord.Color.blurple()
        )

        if ctx.guild:
            embed.set_footer(
                text=f"Sent from {ctx.guild.name}",
                icon_url=getattr(ctx.guild.icon, 'url', None)
            )

        embed.set_author(
            name=ctx.author.display_name,
            icon_url=getattr(ctx.author.avatar, 'url', None)
        )

        try:
            await user.send(embed=embed)
            await ctx.send(f"✅ Message successfully sent to {user.mention}'s DMs.")
        except discord.Forbidden:
            await ctx.send(f"❌ Couldn't DM {user.mention}. They might have DMs disabled or blocked the bot.")
        except Exception as e:
            await ctx.send(f"⚠️ An unexpected error occurred:\n```{str(e)}```")

async def setup(bot: Bot):
    await bot.add_cog(DirectMessageCog(bot))