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
        duration_str = query.data.split("|")[2].strip()
        house_id = context.user_data.get(constants.USER_DATA_KEY_HOUSE)
        machine = machines.get(house_id).get(machine_id)

        if machine == None:
            raise Exception(f"Unknown machine {machine_id}")

        # Start the machine with the selected duration
        machine_started = machine.start_machine(
            username, chat_id, thread_id, int(duration_str)
        )

        if not machine_started:
            text = f"{machine.get_name()} is currently in use. Please come back again later!"
            await query.edit_message_text(text=text)
        else:
            logger.info(f"{username} started {house_id} {machine.get_name()}")
            text = f"Timer set for {duration_str} mins for {house_id} {machine.get_name()} by @{username}!"
            await query.edit_message_text(text=text)

        return ConversationHandler.END

    return set_timer
