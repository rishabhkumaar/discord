import discord
from discord.ext import commands
from discord import app_commands

class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="help", description="Show all available commands and usage.")
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(
            title="📖 Weather Bot Help",
            description="Here are the commands you can use:",
            color=0x00b0f4
        )

        embed.add_field(
            name="`!weather [city]` or `/weather`",
            value="Shows current weather and forecast for the given city.\nDefaults to **Muzaffarpur** if no city is provided.",
            inline=False
        )

        embed.add_field(
            name="`!air [city]` or `/air`",
            value="Shows air quality data (AQI, PM2.5, etc.) for a given city.",
            inline=False
        )

        embed.add_field(
            name="`!help` or `/help`",
            value="Displays this help message.",
            inline=False
        )

        embed.set_footer(text="Built with ❤️ by Rishabh")

        # Use reply for text command or followup for slash
        if isinstance(ctx, commands.Context):
            await ctx.reply(embed=embed)
        else:
            await ctx.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCog(bot))