import logging
from telegram import Update
from telegram.ext import CallbackContext

logger = logging.getLogger("status")


def create_status_command(DRYER_ONE, DRYER_TWO, WASHER_ONE, WASHER_TWO):
    async def status(update: Update, context: CallbackContext):
        logger.info(f"User {update.effective_user.username} started /status")
        DRYER_ONE_TIMER = DRYER_ONE.status()
        DRYER_TWO_TIMER = DRYER_TWO.status()
        WASHER_ONE_TIMER = WASHER_ONE.status()
        WASHER_TWO_TIMER = WASHER_TWO.status()

        reply_text = f"""Status of Laundry Machines:
      
Dryer One: {DRYER_ONE_TIMER}
  
Dryer Two: {DRYER_TWO_TIMER}
  
Washer One: {WASHER_ONE_TIMER}
  
Washer Two: {WASHER_TWO_TIMER}"""

        await update.message.reply_text(reply_text)

    return status
