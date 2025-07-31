import os
from dotenv import load_dotenv

def load_env():
    """
    Load environment variables from a .env file into the OS environment.
    Call this before accessing any secrets.
    """
    load_dotenv()

def get_discord_token():
    return os.getenv("DISCORD_TOKEN")

def get_weather_api_key():
    return os.getenv("WEATHER_API_KEY")