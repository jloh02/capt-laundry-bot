import logging
import constants
from machine import Machine
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

logger = logging.getLogger("status")

status_global = None


def create_status_command(machines: dict[str, dict[str, Machine]]):
    global status_global
    if status_global:
        return status_global

    keyboard_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Change House", callback_data=constants.ConvState.SelectHouse
                )
            ]
        ]
    )

    async def status(update: Update, context: CallbackContext):
        logger.info(f"{update.effective_user.username} started /status")
        house_id = context.chat_data.get(constants.CHAT_DATA_KEY_HOUSE)
        reply_text = f"Status of Laundry Machines:\n{constants.HOUSES.get(house_id)}"
        for machine in machines.get(house_id).values():
            reply_text += f"\n\n{machine.get_name()}: {machine.status()}"

        send_message_method = (
            update.callback_query.edit_message_text
            if update.callback_query
            else update.effective_message.reply_text
        )

        await send_message_method(reply_text, reply_markup=keyboard_markup)

        return constants.ConvState.StatusSelectHouse

    status_global = status
    return status
