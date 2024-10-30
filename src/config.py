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
            "WASHER_TIMER_DURATION_MINUTES_LONG": int(os.getenv("WASHER_TIMER_DURATION_MINUTES_LONG")),
            "WASHER_TIMER_DURATION_MINUTES_MID": int(os.getenv("WASHER_TIMER_DURATION_MINUTES_MID")),
            "WASHER_TIMER_DURATION_MINUTES_SHORT": int(os.getenv("WASHER_TIMER_DURATION_MINUTES_SHORT")),
            "DRYER_TIMER_DURATION_MINUTES_LONG": int(os.getenv("DRYER_TIMER_DURATION_MINUTES_LONG")),
            "DRYER_TIMER_DURATION_MINUTES_MID": int(os.getenv("DRYER_TIMER_DURATION_MINUTES_MID")),
            "DRYER_TIMER_DURATION_MINUTES_SHORT": int(os.getenv("DRYER_TIMER_DURATION_MINUTES_SHORT")),
            "CONVO_TIMEOUT_SECONDS": int(os.getenv("CONVO_TIMEOUT_SECONDS", 300)),
        }
    )
