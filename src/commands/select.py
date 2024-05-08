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


def create_select_menu(machines: dict[Machine]):
    keyboard = []
    machineKV = list(machines.items())
    num_machines = len(machineKV)
    for i in range(0, num_machines, 2):
        machine_id0, machine0 = machineKV[i]
        if i + 1 == num_machines:
            keyboard.append(
                [InlineKeyboardButton(machine0.get_name(), callback_data=machine_id0)]
            )
        else:
            machine_id1, machine1 = machineKV[i + 1]
            keyboard.append(
                [
                    InlineKeyboardButton(
                        machine0.get_name(), callback_data=machine_id0
                    ),
                    InlineKeyboardButton(
                        machine1.get_name(), callback_data=machine_id1
                    ),
                ]
            )

    async def select(update: Update, context: CallbackContext):
        logger.info(f"User {update.effective_user.username} started /select")
        await update.message.reply_text(
            "\U0001F606\U0001F923 Please choose a service: \U0001F606\U0001F923",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return constants.ConvState.RequestConfirmSelect

    return select
