import datetime
import storage
from select_house import select_house
from telegram import Update
from telegram.ext import CallbackContext


# Returns True if end_time is None because timer not set --> not being used
def is_available(end_time):
    if not end_time:
        return True
    return end_time < datetime.datetime.now()


def with_house_context(callback):
    async def contexted_callback(update: Update, context: CallbackContext):
        house = storage.get_house(update.message.chat_id)
        if not house:
            context.chat_data.update({"callback": callback})
            return await select_house(update, context)
        context.chat_data.update({"house": house})
        return await callback(update, context)

    return contexted_callback
