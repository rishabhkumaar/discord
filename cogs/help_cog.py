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
            value="Shows current weather and forecast for the given city. Defaults to Muzaffarpur if no city is provided.",
            inline=False
        )

        embed.add_field(
            name="`!help` or `/help`",
            value="Displays this help message.",
            inline=False
        )

        embed.set_footer(text="Built with ❤️ by Rishabh")

        await ctx.reply(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCog(bot))