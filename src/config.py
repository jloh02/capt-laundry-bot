import os
from dotenv import load_dotenv

config = {}


def read_dotenv():
    global config
    load_dotenv()
    config.update(
        {
            "TELEGRAM_BOT_API_KEY": os.getenv("TELEGRAM_BOT_API_KEY"),
            "WEBHOOK_URL": os.getenv("WEBHOOK_URL"),
            "PRODUCTION": os.getenv("PRODUCTION") == "True",
            "BASE_PATH": os.getenv("BASE_PATH", "./data"),
            "PORT": os.getenv("PORT", 8080),
        }
    )
