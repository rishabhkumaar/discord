import discord
from discord.ext import commands
from discord.ext.commands import Context, Bot, hybrid_command
from datetime import datetime

class UserInfoCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @hybrid_command(name="ui", description="Get detailed information about a user.")
    async def userinfo(self, ctx: Context, user: discord.User = None):
        await ctx.defer()
        user = user or ctx.author

        try:
            profile = await self.bot.fetch_user(user.id)
        except Exception:
            profile = user

        banner_url = profile.banner.url if hasattr(profile, "banner") and profile.banner else None
        avatar_url = user.display_avatar.url
        member = ctx.guild.get_member(user.id) if ctx.guild else None

        shared_servers = sum(1 for guild in self.bot.guilds if guild.get_member(user.id))

        embed = discord.Embed(
            title=f"🌌 {user.name}'s Profile Overview",
            color=discord.Color.from_rgb(138, 43, 226),  # Purple venom tone
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)

        # ─── General Info ─── #
        embed.add_field(name="🆔 User ID", value=f"`{user.id}`", inline=True)
        embed.add_field(name="✏️ Username", value=f"`{user}`", inline=True)
        embed.add_field(name="📆 Created On", value=f"<t:{int(user.created_at.timestamp())}:F>", inline=False)

        # ─── Server Specific Info ─── #
        if member:
            embed.add_field(name="💠 Nickname", value=f"`{member.nick}`" if member.nick else "None", inline=True)
            embed.add_field(name="📥 Joined Server", value=f"<t:{int(member.joined_at.timestamp())}:F>" if member.joined_at else "Unknown", inline=True)
            embed.add_field(name="🧷 Roles", value=f"`{len(member.roles) - 1}`", inline=True)

            if member.premium_since:
                embed.add_field(name="🚀 Boosting Since", value=f"<t:{int(member.premium_since.timestamp())}:F>", inline=True)

        # ─── Bot-wide Info ─── #
        embed.add_field(name="🌐 Shared Servers", value=f"`{shared_servers}`", inline=True)

        await ctx.send(embed=embed)

        # ─── Avatar Display ─── #
        if avatar_url:
            avatar_embed = discord.Embed(
                title=f"🖼️ Avatar of {user.name}",
                color=discord.Color.from_rgb(147, 112, 219)
            )
            avatar_embed.set_image(url=avatar_url)
            await ctx.send(embed=avatar_embed)

        # ─── Banner Display ─── #
        if banner_url:
            banner_embed = discord.Embed(
                title=f"🎨 Banner of {user.name}",
                color=discord.Color.from_rgb(186, 85, 211)
            )
            banner_embed.set_image(url=banner_url)
            await ctx.send(embed=banner_embed)

async def setup(bot: Bot):
    await bot.add_cog(UserInfoCog(bot))