from machine import Machine
from utils import create_select_house_callback
from commands.status import create_status_command
from telegram import Update
from telegram.ext import CallbackContext

status_select_house_global = None


def create_status_select_house(machines: dict[str, dict[str, Machine]]):
    global status_select_house_global
    if status_select_house_global:
        return status_select_house_global

    async def status_select_house(update: Update, context: CallbackContext):
        return await create_select_house_callback(create_status_command(machines))(
            update, context
        )

    status_select_house_global = status_select_house
    return status_select_house
