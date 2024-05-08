import constants
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    CallbackContext,
)

SELECT_MACHINE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Dryer One", callback_data="dryer_one"),
            InlineKeyboardButton("Dryer Two", callback_data="dryer_two"),
        ],
        [
            InlineKeyboardButton("Washer One", callback_data="washer_one"),
            InlineKeyboardButton("Washer Two", callback_data="washer_two"),
        ],
        [InlineKeyboardButton("Exit", callback_data="exit")],
    ]
)


async def select(update: Update, context: CallbackContext):
    # Don't allow users to use /select command in group chats
    if update.message.chat.type != "private":
        return constants.STATES.get("MENU")

    await update.message.reply_text(
        "\U0001F606\U0001F923 Please choose a service: \U0001F606\U0001F923",
        reply_markup=SELECT_MACHINE_INLINE_KEYBOARD,
    )
    return constants.STATES.get("MENU")
