import discord
from discord.ext import commands, tasks
import os
from config import load_env

# Load environment variables from .env
load_env()

# Get Discord token from environment
TOKEN = os.getenv("DISCORD_TOKEN")

# Setup bot with command prefix and intents
intents = discord.Intents.default()
intents.message_content = True  # Required to read user messages

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command("help")

# List of initial extensions (cogs)
initial_extensions = [
    "cogs.weather_cog",
    "cogs.help_cog",
    "cogs.air_cog",
    "cogs.moderation_cog",
    "cogs.dm_cog",
    "cogs.userinfo_cog",
    "cogs.mutual_cog"
]

# Background task to update status every 5 minutes
@tasks.loop(minutes=5)
async def update_presence():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"🌦️ | rizzhub.kr | {len(bot.guilds)} servers"
        ),
        status=discord.Status.online
    )

@update_presence.before_loop
async def before_presence():
    await bot.wait_until_ready()

# Load cogs and setup status on bot ready
@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

    # Load cogs only once
    if not hasattr(bot, "cogs_loaded"):
        for extension in initial_extensions:
            try:
                await bot.load_extension(extension)
                print(f"✅ Loaded {extension}")
            except Exception as e:
                print(f"❌ Failed to load {extension}: {e}")
        await bot.tree.sync()
        print("🔁 Slash commands synced.")
        bot.cogs_loaded = True

    # Set initial presence and start loop
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"🌦️ | <:rishabh:1372620142894383134> by rizzhub.kr | {len(bot.guilds)} servers"
        ),
        status=discord.Status.online
    )
    if not update_presence.is_running():
        update_presence.start()

# Run the bot
if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ DISCORD_TOKEN not found in environment variables.")
