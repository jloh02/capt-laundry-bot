import logging
import constants
from machine import Machine
from utils import create_select_house_callback
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    CallbackContext,
)
from select_house import create_select_house
from commands.select import create_select_menu

logger = logging.getLogger("double_confirm")

double_confirm_global = None


def create_double_confirm(machines: dict[str, dict[str, Machine]]):
    global double_confirm_global
    if double_confirm_global:
        return double_confirm_global

    select_house = create_select_house()
    select_menu = create_select_menu()

    async def double_confirm(update: Update, context: CallbackContext) -> int:
        query = update.callback_query
        await query.answer()

        if query.data == constants.ConvState.SelectHouse:
            return await create_select_house_callback(select_menu)(update, context)

        machine_id = query.data
        machine = machines.get(context.chat_data.get("house")).get(machine_id)

        if machine == None:
            raise Exception(f"Unknown machine {machine_id}")

        machine_name = machine.get_name()

        await query.edit_message_text(
            text=f"Timer for {machine_name} will begin?",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Yes", callback_data=f"yes|{machine_id}")],
                    [InlineKeyboardButton("No", callback_data="no")],
                ]
            ),
        )

        return constants.ConvState.ConfirmSelect

    double_confirm_global = double_confirm
    return double_confirm
