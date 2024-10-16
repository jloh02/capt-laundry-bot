import logging
import constants
from machine import Machine
from config import config
from telegram.ext import ConversationHandler, CallbackContext
from telegram import Update

logger = logging.getLogger("set_duration")

async def set_duration(machines: dict[str, dict[str, Machine]], update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    logger.info(query.data)
    
    # Extract machine_id and duration from the callback data
    machine_id, duration_str = query.data.split(",")
    house_id = context.user_data.get(constants.USER_DATA_KEY_HOUSE)
    machine = machines.get(house_id).get(machine_id)

    if machine is None:
        raise Exception(f"Unknown machine {machine_id}")

    username = update.effective_user.username
    chat_id = update.effective_chat.id
    thread_id = update.effective_message.message_thread_id

    # Start the machine with the selected duration
    machine_started = machine.start_machine(username, chat_id, thread_id, duration_str)
    
    if not machine_started:
        text = f"{machine.get_name()} is currently in use. Please come back again later!"
        await query.edit_message_text(text=text)
    else:
        logger.info(f"{username} started {house_id} {machine.get_name()}")
        text = f"Timer set for {config.get(duration_str)} mins for {house_id} {machine.get_name()} by @{username}!"
        await query.edit_message_text(text=text)

    return ConversationHandler.END
