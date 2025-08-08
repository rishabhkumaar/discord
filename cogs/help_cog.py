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
            description="Here’s what I can do!\nYou can use **slash commands** or prefix commands like `!command`.",
            color=discord.Color.blurple()
        )

        total_commands = 0

        # Loop through cogs and their commands
        for cog in sorted(self.bot.cogs.values(), key=lambda c: c.qualified_name.lower()):
            cog_commands = cog.get_commands()

            # Filter visible commands that the user can run
            visible_commands = [
                cmd for cmd in cog_commands
                if not cmd.hidden and await cmd.can_run(ctx)
            ]

            if not visible_commands:
                continue

            # Sort alphabetically
            visible_commands.sort(key=lambda c: c.name)

            # Build command list text
            command_list = ""
            for cmd in visible_commands:
                description = cmd.description or "No description provided."
                command_list += f"➤ `/{cmd.name}` – {description}\n"
                total_commands += 1

            embed.add_field(
                name=f"📦 {cog.qualified_name}",
                value=command_list,
                inline=False
            )

        embed.set_footer(text=f"{total_commands} commands available • Bot by rizzhub.kr")

        if self.bot.user and self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)

        # Buttons
        view = discord.ui.View()

        # Support Server Button
        view.add_item(discord.ui.Button(
            label="🌐 Support Server",
            url="https://discord.gg/WjWZwmpK"
        ))

        # Invite Button (auto-fetch client ID)
        client_id = self.bot.user.id
        invite_url = f"https://discord.com/oauth2/authorize?client_id={client_id}&permissions=8&scope=bot%20applications.commands"
        view.add_item(discord.ui.Button(
            label="➕ Invite Bot",
            url=invite_url
        ))

        await ctx.send(embed=embed, view=view)

async def setup(bot: Bot):
    await bot.add_cog(HelpCog(bot))
