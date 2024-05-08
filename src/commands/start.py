import constants
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


async def start(update: Update, context: CallbackContext):
    if len(context.args) > 0:
        return

    await update.message.reply_text(constants.WELCOME_MESSAGE)
    return constants.ConvState.Menu
