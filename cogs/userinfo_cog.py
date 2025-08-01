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

        user = user or ctx.author

        # Try to fetch full user profile (for banner)
        try:
            profile = await self.bot.fetch_user(user.id)
        except Exception:
            profile = user

        banner_url = profile.banner.url if hasattr(profile, "banner") and profile.banner else None
        avatar_url = user.avatar.url if user.avatar else None

        # Get member object (only available if in same guild)
        member = ctx.guild.get_member(user.id) if ctx.guild else None

        shared_servers = sum(1 for guild in self.bot.guilds if guild.get_member(user.id))

        # Main Info Embed
        embed = discord.Embed(
            title=f"{user.name}'s Profile",
            color=discord.Color.blurple(),
            timestamp=datetime.utcnow()
        )

        embed.set_thumbnail(url=avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

        embed.add_field(name="🆔 ID", value=f"`{user.id}`", inline=True)
        embed.add_field(name="👤 Username", value=str(user), inline=True)
        embed.add_field(name="🗓️ Account Created", value=user.created_at.strftime("%b %d, %Y"), inline=True)

        if member:
            embed.add_field(name="🔰 Nickname", value=member.nick or "None", inline=True)
            embed.add_field(name="📅 Joined Server", value=member.joined_at.strftime("%b %d, %Y") if member.joined_at else "Unknown", inline=True)
            embed.add_field(name="🛡️ Roles", value=str(len(member.roles) - 1), inline=True)

            if member.premium_since:
                embed.add_field(name="🚀 Boosting Since", value=member.premium_since.strftime("%b %d, %Y"), inline=True)

        embed.add_field(name="🌐 Shared Servers", value=str(shared_servers), inline=True)

        await ctx.send(embed=embed)

        # Separate embeds for avatar and banner
        if avatar_url:
            pfp_embed = discord.Embed(
                title=f"{user.name}'s Avatar",
                color=discord.Color.blue()
            )
            pfp_embed.set_image(url=avatar_url)
            await ctx.send(embed=pfp_embed)

        if banner_url:
            banner_embed = discord.Embed(
                title=f"{user.name}'s Banner",
                color=discord.Color.blue()
            )
            banner_embed.set_image(url=banner_url)
            await ctx.send(embed=banner_embed)

async def setup(bot: Bot):
    await bot.add_cog(UserInfoCog(bot))