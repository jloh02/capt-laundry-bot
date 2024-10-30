import logging
import constants
from config import config
from machine import Machine
from telegram.ext import ConversationHandler, CallbackContext
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton

logger = logging.getLogger("set_timer_machine")


def set_timer_machine(machines: dict[str, dict[str, Machine]]):
    async def set_timer(update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        thread_id = update.effective_message.message_thread_id
        username = update.effective_user.username
        query = update.callback_query
        await query.answer()

        logger.info(query.data.split("|"))

        machine_id = query.data.split("|")[1].strip()
        house_id = context.user_data.get(constants.USER_DATA_KEY_HOUSE)
        machine = machines.get(house_id).get(machine_id)

        if machine == None:
            raise Exception(f"Unknown machine {machine_id}")

        machine_name = machine.get_name()

        # Create inline keyboard with wash duration options

        if "washer" in machine_name.lower():
            reply_markup = InlineKeyboardMarkup(
                list(
                    map(
                        lambda d: [
                            InlineKeyboardButton(
                                f"{d} mins",
                                callback_data=f"{machine_id},{d}",
                            )
                        ],
                        config.get("WASHER_TIMER_DURATION_MINUTES"),
                    )
                )
            )
        else:
            reply_markup = InlineKeyboardMarkup(
                list(
                    map(
                        lambda d: [
                            InlineKeyboardButton(
                                f"{d} mins",
                                callback_data=f"{machine_id},{d}",
                            )
                        ]
                    ),
                    config.get("DRYER_TIMER_DURATION_MINUTES"),
                )
            )

        # Ask user to select the duration before starting the machine
        text = f"Please select the duration for {machine_name}:"
        await query.edit_message_text(text=text, reply_markup=reply_markup)

        return constants.ConvState.SetDuration

    return set_timer
