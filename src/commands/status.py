import logging
import constants
from machine import Machine
from telegram import Update
from telegram.ext import CallbackContext

logger = logging.getLogger("status")


def create_status_command(machines: dict[str, dict[str, Machine]]):
    async def status(update: Update, context: CallbackContext):
        logger.info(f"User {update.effective_user.username} started /status")
        house_id = context.chat_data.get("house")
        reply_text = f"Status of Laundry Machines:\n{constants.HOUSES.get(house_id)}"
        for machine in machines.get(house_id).values():
            reply_text += f"\n\n{machine.get_name()}: {machine.status()}"

        send_message_method = (
            update.callback_query.edit_message_text
            if update.callback_query
            else update.message.reply_text
        )

        await send_message_method(reply_text)

    return status
