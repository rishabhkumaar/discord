import discord
from discord.ext import commands
from discord.ext.commands import Context, Bot

class CustomHelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return f"`{self.clean_prefix}{command.qualified_name} {command.signature}`"

    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="📖 Help Menu",
            description="Here’s what I can do!\nUse either `/slash` commands or `!prefix` commands.",
            color=discord.Color.blurple()
        )

        # Static categorized fields
        embed.add_field(
            name="📡 Weather",
            value="`/weather <city>` – Check the weather and air quality of a city.",
            inline=False
        )

        embed.add_field(
            name="🌫️ Air Quality",
            value="`/air <city>` – Shows AQI, pollutants, and health tips.",
            inline=False
        )

        embed.add_field(
            name="📩 Direct Message",
            value="`/dm <user> <message>` – Sends a private message. *(Admin-only)*",
            inline=False
        )

        embed.add_field(
            name="⚙️ Moderation",
            value="`/kick`, `/ban`, `/mute`, `/unmute`, `/clear`, `/unban` – Manage your server.",
            inline=False
        )

        embed.add_field(
            name="👤 User Info",
            value="`/userinfo <user>` – View full user profile, common servers, badges, etc.",
            inline=False
        )

        # Dynamic cog-based listing (optional fallback if any extra commands exist)
        for cog, commands_list in mapping.items():
            filtered = await self.filter_commands(commands_list, sort=True)
            if filtered:
                name = cog.qualified_name if cog else "Uncategorized"
                value = ", ".join(f"`{cmd.name}`" for cmd in filtered)
                embed.add_field(name=f"🔹 {name}", value=value, inline=False)

        embed.set_footer(text="Tip: Use /help <command> to get detailed info.")
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(
            title=f"ℹ️ Help: `{command.qualified_name}`",
            description=command.help or "No description provided.",
            color=discord.Color.green()
        )

        embed.add_field(name="Usage", value=self.get_command_signature(command), inline=False)

        if command.aliases:
            embed.add_field(name="Aliases", value=", ".join(f"`{alias}`" for alias in command.aliases), inline=False)

        await self.get_destination().send(embed=embed)

class HelpCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        help_cmd = CustomHelpCommand()
        help_cmd.cog = self
        bot.help_command = help_cmd

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

async def setup(bot: Bot):
    await bot.add_cog(HelpCog(bot))
