import os
from dotenv import load_dotenv

def load_env():
    load_dotenv()

def get_discord_token():
    return os.getenv("DISCORD_TOKEN")

def get_weather_api_key():
    return os.getenv("WEATHER_API_KEY")

def get_rapidapi_key():
    return os.getenv("RAPIDAPI_KEY")
