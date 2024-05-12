import constants
from utils import delete_inline_keyboard_if_available
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler


async def timeout_on_message(context: CallbackContext):
    await delete_inline_keyboard_if_available(context)
    return ConversationHandler.END


async def timeout_on_callback_query(update: Update, context: CallbackContext):
    context.user_data.update({constants.USER_DATA_KEY_CALLBACK: None})
    await update.callback_query.edit_message_reply_markup(reply_markup=None)
    return ConversationHandler.END
