# 🌤️ Discord Weather Bot

A simple, extensible Python-based Discord bot that fetches real-time weather and forecast data using the OpenWeatherMap API and displays it neatly in Discord.

---

## 🚀 Features

- Fetch **current weather** by city name
- Show **3-hour interval forecasts**
- Display helpful **weather tips** (heat, rain, snow, etc.)
- Embedded messages with weather icons, coordinates, sunrise/sunset
- Clean, modular Python code using `discord.py`

---

## 📁 File Structure

```

discord-weather-bot/
├── bot.py               # Main entrypoint
├── config.py            # Loads environment variables
├── .env                 # Stores API keys (DO NOT push to GitHub)
├── cogs/
│   └── weather\_cog.py   # Contains the /weather command logic
├── weather/
│   ├── fetcher.py       # Handles API calls
│   └── formatter.py     # Formats weather data into Discord messages
├── requirements.txt     # Project dependencies
└── README.md            # You're here!

````

---

## 🔧 Requirements

- Python 3.8+
- [Discord Bot Token](https://discord.com/developers/applications)
- [OpenWeatherMap API Key](https://openweathermap.org/api)

Install dependencies:
```bash
pip install -r requirements.txt
````

---

## 🔐 Setup

1. **Create a `.env` file** in the root:

   ```
   DISCORD_TOKEN=your_discord_bot_token_here
   WEATHER_API_KEY=your_openweathermap_api_key_here
   ```

2. **Run the bot:**

   ```bash
   python bot.py
   ```

3. **Invite your bot** to your server with the `message content intent` enabled.

---

## 💬 Usage

In your Discord server:

```
/weather [city]
```

Examples:

```
/weather delhi
/weather pune
/weather bangalore
```

---

## 🛡️ Security Tips

* Never commit your `.env` file.
* Always rotate your keys if they get exposed.

---

## 📜 License

MIT License. Feel free to use and expand this bot for your own projects!

---

## ✨ Credits

Built with ❤️ by Rishabh using:

* [discord.py](https://discordpy.readthedocs.io/)
* [OpenWeatherMap API](https://openweathermap.org/api)

---