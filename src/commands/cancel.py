from telegram import (
    Update,
)
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
)


async def cancel(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Bye! Use /start again to call me again!")
    return ConversationHandler.END
