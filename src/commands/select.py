import logging
import constants
from machine import Machine
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    CallbackContext,
)

logger = logging.getLogger("select")


def create_select_menu():
    keyboard = []
    num_machines = len(constants.MACHINE_NAMES)
    for i in range(0, num_machines, 2):
        if i + 1 == num_machines:
            keyboard.append(
                [InlineKeyboardButton(constants.MACHINE_NAMES[i], callback_data=constants.MACHINE_NAMES[i])]
            )
        else:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        constants.MACHINE_NAMES[i], callback_data=constants.MACHINE_NAMES[i]
                    ),
                    InlineKeyboardButton(
                        constants.MACHINE_NAMES[i+1], callback_data=constants.MACHINE_NAMES[i+1]
                    ),
                ]
            )
    keyboard_markup = InlineKeyboardMarkup(keyboard)
    async def select(update: Update, context: CallbackContext):
        logger.info(f"User {update.effective_user.username} started /select")
        send_message_method = (
            update.callback_query.edit_message_text
            if update.callback_query
            else update.message.reply_text
        )
        await send_message_method(
            f"Welcome to {context.chat_data.get("house")} Laundry Bot!\n\nPlease choose a service:",
            reply_markup=keyboard_markup,
        )
        return constants.ConvState.RequestConfirmSelect

    return select
