import discord
from discord.ext import commands
from discord.ext.commands import Context, Bot, hybrid_command, has_permissions

class DirectMessageCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @hybrid_command(name="dm", description="Send a stylish DM to a user.")
    @has_permissions(administrator=True)
    async def dm(self, ctx: Context, user: discord.User, *, message: str):
        """Sends a beautifully formatted DM to the specified user."""
        await ctx.defer(ephemeral=True)
        try:
            # Create the embed
            embed = discord.Embed(
                title="📬 You've got a new message!",
                description=message,
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"Sent from {ctx.guild.name}", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

            # Send the DM
            await user.send(embed=embed)
            await ctx.followup.send(f"✅ Message successfully sent to {user.mention}'s DMs.")
        except discord.Forbidden:
            await ctx.followup.send(f"❌ I couldn't DM {user.mention}. They might have DMs disabled or blocked the bot.")
        except Exception as e:
            await ctx.followup.send(f"⚠️ Something went wrong while sending the DM:\n`{str(e)}`")

async def setup(bot: Bot):
    await bot.add_cog(DirectMessageCog(bot))