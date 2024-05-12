import logging
import constants
from machine import Machine
from telegram.ext import ConversationHandler, CallbackContext
from telegram import Update

logger = logging.getLogger("set_timer_machine")


def set_timer_machine(machines: dict[str, dict[str, Machine]]):
    async def set_timer(update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        thread_id = update.effective_message.message_thread_id
        username = update.effective_user.username
        query = update.callback_query
        await query.answer()

        machine_id = query.data.split("|")[1].strip()
        house_id = context.user_data.get(constants.USER_DATA_KEY_HOUSE)
        machine = machines.get(house_id).get(machine_id)

        if machine == None:
            raise Exception(f"Unknown machine {machine_id}")

        machine_name = machine.get_name()

        machine_started = machine.start_machine(username, chat_id, thread_id)
        if not machine_started:
            text = f"{machine_name} is currently in use. Please come back again later!"
            await query.edit_message_text(text=text)
        else:
            logger.info(f"{username} started {house_id} {machine_name}")
            text = f"Timer Set for {Machine.COMPLETION_TIME // 60}mins for {house_id} {machine_name} by @{username}!"
            await query.edit_message_text(text=text)

        return ConversationHandler.END

    return set_timer
