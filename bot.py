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

bot = commands.Bot(command_prefix='/', intents=intents)

# On ready
@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

# Load cogs (extensions)
initial_extensions = [
    "cogs.weather_cog"
]

for extension in initial_extensions:
    try:
        bot.load_extension(extension)
        print(f"✅ Loaded {extension}")
    except Exception as e:
        print(f"❌ Failed to load {extension}: {e}")

# Run the bot
if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ DISCORD_TOKEN not found in environment variables.")