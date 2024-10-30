import logging
import constants
from machine import Machine
from config import config
from telegram.ext import CallbackContext
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton

logger = logging.getLogger("set_duration")


def select_duration(machines: dict[str, dict[str, Machine]]):
    async def select_duration_handler(update: Update, context: CallbackContext):
        query = update.callback_query
        await query.answer()

        logger.info(query.data)

        machine_id = query.data
        house_id = context.user_data.get(constants.USER_DATA_KEY_HOUSE)
        machine = machines.get(house_id).get(machine_id)
        machine_name = machine.get_name()

        if machine is None:
            raise Exception(f"Unknown machine {machine_id}")

        CANCEL_BUTTON = InlineKeyboardButton(
            "Cancel",
            callback_data="cancel",
        )
        if "washer" in machine_name.lower():
            reply_markup = InlineKeyboardMarkup(
                [
                    list(
                        map(
                            lambda d: InlineKeyboardButton(
                                f"{d} mins",
                                callback_data=f"{machine_id}|{d}",
                            ),
                            config.get("WASHER_TIMER_DURATION_MINUTES"),
                        )
                    )
                ]
                + [[CANCEL_BUTTON]]
            )
        else:
            reply_markup = InlineKeyboardMarkup(
                [
                    list(
                        map(
                            lambda d: InlineKeyboardButton(
                                f"{d} mins",
                                callback_data=f"{machine_id}|{d}",
                            ),
                            config.get("DRYER_TIMER_DURATION_MINUTES"),
                        )
                    )
                ]
                + [[CANCEL_BUTTON]]
            )

        # Ask user to select the duration before starting the machine
        text = f"Please select the duration for {house_id} {machine_name}:"
        await query.edit_message_text(text=text, reply_markup=reply_markup)

        return constants.ConvState.RequestConfirmSelect

    return select_duration_handler
