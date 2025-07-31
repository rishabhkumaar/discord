import discord
from discord.ext import commands
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

# On ready
@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

# Load cogs (extensions)
initial_extensions = [
    "cogs.weather_cog",
    "cogs.help_cog"
]

# Load extensions asynchronously
async def load_cogs():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f"✅ Loaded {extension}")
        except Exception as e:
            print(f"❌ Failed to load {extension}: {e}")

# Run the loading function
@bot.event
async def on_ready():
    await load_cogs()
    await bot.tree.sync()  # Sync slash commands
    print(f"✅ Bot is online as {bot.user}")

# Run the bot
if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ DISCORD_TOKEN not found in environment variables.")