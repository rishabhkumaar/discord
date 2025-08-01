import discord
from discord.ext import commands
from discord.ext.commands import Context, Bot, hybrid_command

class HelpCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @hybrid_command(name="help", description="Show the list of available commands.")
    async def help(self, ctx: Context):
        await ctx.defer()

        embed = discord.Embed(
            title="📖 Help Menu",
            description="Here are the available commands and their usage:",
            color=discord.Color.green()
        )

        for cog in self.bot.cogs.values():
            cog_commands = cog.get_commands()
            command_list = ""
            for command in cog_commands:
                if not command.hidden:
                    command_list += f"**/{command.name}** – {command.description or 'No description'}\n"
            if command_list:
                embed.add_field(name=f"📦 {cog.qualified_name}", value=command_list, inline=False)

        embed.set_footer(text="Use slash commands or prefix commands like !help")

        if self.bot.user and self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)

        # Add support server button
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Join Support Server", url="https://discord.gg/WjWZwmpK"))

        await ctx.send(embed=embed, view=view)

async def setup(bot: Bot):
    await bot.add_cog(HelpCog(bot))