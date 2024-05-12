import datetime
import logging
import storage
import constants
from select_house import create_select_house
from telegram import Message, Update
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
        house = storage.get_house(update.effective_user.id)
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


def with_deleted_previous_keyboards(callback):
    async def callback_with_deleted_previous_keyboards(
        update: Update, context: CallbackContext
    ):
        await delete_inline_keyboard_if_available(context)
        return await callback(update, context)

    return callback_with_deleted_previous_keyboards


async def delete_inline_keyboard_if_available(context: CallbackContext):
    bot_msg = context.user_data.get(constants.USER_DATA_KEY_BOT_MSG)
    if isinstance(bot_msg, Message):
        try:
            await bot_msg.edit_reply_markup(reply_markup=None)
        except Exception:
            pass
