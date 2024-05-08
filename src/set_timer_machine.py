from machine import Machine
import constants


def set_timer_machine(machine: Machine):
    async def set_timer(update, context):
        machine_name = machine.get_name()
        # underscore_name = machine_name.lower().replace(" ", "_")

        chat_id = update.effective_message.chat_id
        query = update.callback_query
        await query.answer()

        if not (machine.start_machine(update.effective_message.chat.username, chat_id)):
            text = f"{machine_name} is currently in use. Please come back again later!"
            await query.edit_message_text(text=text)
        else:
            text = f"Timer Set for {Machine.COMPLETION_TIME}mins for {machine_name}. Please come back again!"
            await query.edit_message_text(text=text)

        return constants.STATES.get("MENU")

    return set_timer
