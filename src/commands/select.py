import logging
import constants
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    CallbackContext,
)

logger = logging.getLogger("select")

select_menu_global = None


def create_select_menu():
    global select_menu_global
    if select_menu_global:
        return select_menu_global

    keyboard = []
    num_machines = len(constants.MACHINE_NAMES)
    for i in range(0, num_machines, 2):
        if i + 1 == num_machines:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        constants.MACHINE_NAMES[i],
                        callback_data=constants.MACHINE_NAMES[i],
                    )
                ]
            )
        else:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        constants.MACHINE_NAMES[i],
                        callback_data=constants.MACHINE_NAMES[i],
                    ),
                    InlineKeyboardButton(
                        constants.MACHINE_NAMES[i + 1],
                        callback_data=constants.MACHINE_NAMES[i + 1],
                    ),
                ]
            )
    keyboard.append(
        [
            InlineKeyboardButton(
                "Change House", callback_data=constants.ConvState.SelectHouse
            )
        ]
    )
    keyboard_markup = InlineKeyboardMarkup(keyboard)

    async def select_menu(update: Update, context: CallbackContext):
        logger.info(f"User {update.effective_user.username} started /select")
        send_message_method = (
            update.callback_query.edit_message_text
            if update.callback_query
            else update.effective_message.reply_text
        )
        await send_message_method(
            f"{constants.HOUSES.get(context.chat_data.get(constants.CHAT_DATA_KEY_HOUSE))}\n\nPlease choose a service:",
            reply_markup=keyboard_markup,
        )
        return constants.ConvState.RequestConfirmSelect

    select_menu_global = select_menu
    return select_menu
