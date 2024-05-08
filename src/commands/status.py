import logging
from machine import Machine
from telegram import Update
from telegram.ext import CallbackContext

logger = logging.getLogger("status")


def create_status_command(machines: dict[Machine]):
    async def status(update: Update, context: CallbackContext):
        logger.info(f"User {update.effective_user.username} started /status")
        reply_text = "Status of Laundry Machines:"
        for machine in machines.values():
            reply_text += f"\n\n{machine.get_name()}: {machine.status()}"

        await update.message.reply_text(reply_text)

    return status
