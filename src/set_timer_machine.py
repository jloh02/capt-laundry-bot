from machine import Machine
import constants
import logging

logger = logging.getLogger("set_timer_machine")


def set_timer_machine(machines: dict[Machine]):
    async def set_timer(update, context):
        chat_id = update.effective_message.chat_id
        query = update.callback_query
        await query.answer()

        machine_id = query.data.split("|")[1].strip()
        machine = machines.get(machine_id)

        if machine == None:
            raise Exception(f"Unknown machine {machine_id}")

        machine_name = machine.get_name()

        if not (machine.start_machine(update.effective_message.chat.username, chat_id)):
            text = f"{machine_name} is currently in use. Please come back again later!"
            await query.edit_message_text(text=text)
        else:
            logger.info(f"User {update.effective_user.username} started {machine_name}")
            text = f"Timer Set for {Machine.COMPLETION_TIME // 60}mins for {machine_name}. Please come back again!"
            await query.edit_message_text(text=text)

        return constants.ConvState.Menu

    return set_timer
