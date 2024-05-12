import datetime
import logging
import storage
import constants
from select_house import create_select_house
from telegram import Update
from telegram.ext import CallbackContext

logger = logging.getLogger("utils")


# Returns True if end_time is None because timer not set --> not being used
def is_available(end_time):
    if not end_time:
        return True
    return end_time < datetime.datetime.now()


def with_house_context(callback):
    select_house = create_select_house()

    async def contexted_callback(update: Update, context: CallbackContext):
        house = storage.get_house(update.effective_message.chat_id)
        if not house:
            context.user_data.update({constants.USER_DATA_KEY_CALLBACK: callback})
            return await select_house(update, context)
        context.user_data.update({constants.USER_DATA_KEY_HOUSE: house})
        return await callback(update, context)

    return contexted_callback


def create_select_house_callback(callback):
    select_house = create_select_house()

    async def select_house_with_callback(update: Update, context: CallbackContext):
        logger.info(f"{update.effective_user.username} selected change house from menu")
        context.user_data.update({constants.USER_DATA_KEY_CALLBACK: callback})
        return await select_house(update, context)

    return select_house_with_callback
