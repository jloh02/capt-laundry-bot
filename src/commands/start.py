import constants
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler


async def start(update: Update, context: CallbackContext):
    if len(context.args) > 0:
        return

    await update.effective_message.reply_text(constants.WELCOME_MESSAGE)
    return ConversationHandler.END
