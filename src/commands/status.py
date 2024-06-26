import logging
import constants
from machine import Machine
from telegram import Chat, Update, InlineKeyboardMarkup, InlineKeyboardButton
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

        house_id = context.user_data.get(constants.USER_DATA_KEY_HOUSE)
        reply_text = f"{constants.HOUSES.get(house_id)}"
        dm = update.effective_chat.type == Chat.PRIVATE

        for machine in machines.get(house_id).values():
            reply_text += f"\n\n{machine.get_name()}: {machine.status(dm)}"

        if not dm:
            reply_text += f"\n\nUse /status in DMs to @ people in status. You can DM me using @{context.bot.username}"

        send_message_method = (
            update.callback_query.edit_message_text
            if update.callback_query
            else update.effective_message.reply_text
        )

        message = await send_message_method(reply_text, reply_markup=keyboard_markup)
        context.user_data.update({constants.USER_DATA_KEY_BOT_MSG: message})

        return constants.ConvState.StatusSelectHouse

    status_global = status
    return status
