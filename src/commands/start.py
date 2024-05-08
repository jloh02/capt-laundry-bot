import constants
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

START_INLINE_KEYBOARD = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Exit", callback_data="exit")]]
)


async def start(update: Update, context: CallbackContext):
    if len(context.args) > 0:
        return

    await update.message.reply_text(
        constants.WELCOME_MESSAGE,
        reply_markup=START_INLINE_KEYBOARD,
    )
    return constants.STATES.get("MENU")
