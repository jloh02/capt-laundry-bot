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
from commands.select import create_select_menu

logger = logging.getLogger("double_confirm")

double_confirm_global = None


def create_double_confirm(machines: dict[str, dict[str, Machine]]):
    global double_confirm_global
    if double_confirm_global:
        return double_confirm_global

    select_menu = create_select_menu()

    async def double_confirm(update: Update, context: CallbackContext) -> int:
        query = update.callback_query
        await query.answer()

        logger.info(query.data)

        if query.data == constants.ConvState.SelectHouse:
            return await create_select_house_callback(select_menu)(update, context)

        house_id = context.user_data.get(constants.USER_DATA_KEY_HOUSE)
        machine_id = query.data.split("|")[0].strip()
        duration_str = query.data.split("|")[1].strip()
        machine = machines.get(house_id).get(machine_id)

        if machine == None:
            raise Exception(f"Unknown machine {machine_id}")

        machine_name = machine.get_name()

        await query.edit_message_text(
            text=f"{duration_str} mins timer for {house_id} {machine_name} will begin?",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Yes", callback_data=f"yes|{machine_id}|{duration_str}"
                        )
                    ],
                    [InlineKeyboardButton("No", callback_data="no")],
                ]
            ),
        )

        return constants.ConvState.ConfirmSelect

    double_confirm_global = double_confirm
    return double_confirm
