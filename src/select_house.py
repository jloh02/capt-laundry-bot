import logging
import storage
import constants
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import CallbackContext, ConversationHandler

logger = logging.getLogger("select_house")


async def select_house(update: Update, context: CallbackContext) -> int:
    logger.info(f"User {update.effective_user.username} started select house")

    send_message_method = (
        update.callback_query.edit_message_text
        if update.callback_query
        else update.message.reply_text
    )
    await send_message_method(
        "Please choose your house:",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("House 1", callback_data="house1")]]
        ),
    )
    return constants.ConvState.SelectHouse


async def select_house_completed(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    house = query.data
    logger.info(
        f"User {update.effective_user.username} selected house for chat {update.effective_chat.id}: {house}"
    )
    context.chat_data.update({"house": house})
    storage.write_house(update.effective_chat.id, house)

    callback = context.chat_data.get("callback")

    return await callback(update, context) if callback else ConversationHandler.END
