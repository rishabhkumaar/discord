import discord
import time
from discord.ext import commands
from discord.ext.commands import Context, Bot, hybrid_command

class PingCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.bot.launch_time = time.time()

    @hybrid_command(name="ping", description="Check the bot's latency and connection stats.")
    async def ping(self, ctx: Context):
        start = time.perf_counter()
        msg = await ctx.reply("🏓 Pinging...")
        end = time.perf_counter()

        websocket_ping = round(self.bot.latency * 1000, 2)
        message_ping = round((end - start) * 1000, 2)
        uptime_seconds = round(time.time() - self.bot.launch_time)

        days, rem = divmod(uptime_seconds, 86400)
        hours, rem = divmod(rem, 3600)
        minutes, seconds = divmod(rem, 60)
        uptime = f"{days}d {hours}h {minutes}m {seconds}s"

        embed = discord.Embed(
            title="📡 Bot Connection Stats",
            color=discord.Color.from_rgb(138, 43, 226),
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="🔌 WebSocket Latency", value=f"`{websocket_ping} ms`", inline=True)
        embed.add_field(name="💬 Message Latency", value=f"`{message_ping} ms`", inline=True)
        embed.add_field(name="⏱️ Uptime", value=f"`{uptime}`", inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)

        await msg.edit(content=None, embed=embed)

async def setup(bot: Bot):
    await bot.add_cog(PingCog(bot))
