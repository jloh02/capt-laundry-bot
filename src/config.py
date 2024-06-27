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
            "PORT": os.getenv("PORT", 3000),
            "TIMER_DURATION_MINUTES": int(os.getenv("TIMER_DURATION_MINUTES", 34)),
            "CONVO_TIMEOUT_SECONDS": int(os.getenv("CONVO_TIMEOUT_SECONDS", 300)),
        }
    )
