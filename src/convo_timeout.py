import constants
from telegram import Message, Update
from telegram.ext import CallbackContext, ConversationHandler


async def timeout_on_message(update: Update, context: CallbackContext):
    bot_msg = context.user_data.get(constants.USER_DATA_KEY_BOT_MSG)
    if isinstance(bot_msg, Message):
        await bot_msg.edit_reply_markup(reply_markup=None)
    return ConversationHandler.END


async def timeout_on_callback_query(update: Update, context: CallbackContext):
    context.user_data.update({constants.USER_DATA_KEY_CALLBACK: None})
    await update.callback_query.edit_message_reply_markup(reply_markup=None)
    return ConversationHandler.END
