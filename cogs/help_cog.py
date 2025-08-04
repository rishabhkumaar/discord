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
            description="Explore all available features below.\nUse **slash commands** or **prefix `!`**!",
            color=discord.Color.blurple()
        )

        total_commands = 0

        for cog in self.bot.cogs.values():
            cog_commands = cog.get_commands()
            visible_commands = [cmd for cmd in cog_commands if not cmd.hidden]

            if not visible_commands:
                continue

            command_list = ""
            for cmd in visible_commands:
                description = cmd.description or "No description"
                command_list += f"➤ `/{cmd.name}` – {description}\n"
                total_commands += 1

            if command_list:
                embed.add_field(
                    name=f"📦 {cog.qualified_name}",
                    value=command_list,
                    inline=False
                )

        embed.set_footer(text=f"{total_commands} commands available • Bot by rizzhub.kr")

        if self.bot.user and self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)

        # Add support server and invite buttons
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="🌐 Support Server", url="https://discord.gg/WjWZwmpK"))
        view.add_item(discord.ui.Button(label="➕ Invite Bot", url="https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot%20applications.commands"))

        await ctx.send(embed=embed, view=view)

async def setup(bot: Bot):
    await bot.add_cog(HelpCog(bot))
