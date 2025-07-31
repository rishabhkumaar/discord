import discord
from discord.ext import commands
from discord.ext.commands import Context, Bot, hybrid_command
from datetime import datetime

class UserInfoCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @hybrid_command(name="userinfo", description="Get detailed info about a user.")
    async def userinfo(self, ctx: Context, user: discord.User = None):
        await ctx.defer()

        user = user or ctx.author  # Default to invoker if no user is provided

        try:
            profile = await self.bot.fetch_user(user.id)
        except Exception:
            profile = user

        # Get banner if available
        banner_url = profile.banner.url if hasattr(profile, "banner") and profile.banner else None

        # Get member object from current guild
        member = ctx.guild.get_member(user.id) if ctx.guild else None

        # Count shared servers
        shared_servers = sum(1 for guild in self.bot.guilds if guild.get_member(user.id))

        # Build the embed
        embed = discord.Embed(
            title=f"{user.name}'s Profile",
            color=discord.Color.blurple(),
            timestamp=datetime.utcnow()
        )

        embed.set_thumbnail(url=user.avatar.url if user.avatar else None)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

        embed.add_field(name="🆔 ID", value=f"`{user.id}`", inline=True)
        embed.add_field(name="👤 Username", value=f"{user}", inline=True)
        embed.add_field(name="🗓️ Account Created", value=user.created_at.strftime("%b %d, %Y"), inline=True)

        if member:
            embed.add_field(name="🔰 Nickname", value=member.nick or "None", inline=True)
            embed.add_field(name="📅 Joined Server", value=member.joined_at.strftime("%b %d, %Y"), inline=True)
            embed.add_field(name="🛡️ Roles", value=str(len(member.roles) - 1), inline=True)

            if member.premium_since:
                embed.add_field(name="🚀 Boosting Since", value=member.premium_since.strftime("%b %d, %Y"), inline=True)

        embed.add_field(name="🌐 Shared Servers", value=str(shared_servers), inline=True)

        if banner_url:
            embed.set_image(url=banner_url)

        await ctx.send(embed=embed)

async def setup(bot: Bot):
    await bot.add_cog(UserInfoCog(bot))
