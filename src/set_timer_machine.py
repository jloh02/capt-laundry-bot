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
        washer_keyboard = [
            [InlineKeyboardButton("30", callback_data=f"{machine_id},WASHER_TIMER_DURATION_MINUTES_SHORT")],
            [InlineKeyboardButton("32", callback_data=f"{machine_id},WASHER_TIMER_DURATION_MINUTES_MID")],
            [InlineKeyboardButton("34", callback_data=f"{machine_id},WASHER_TIMER_DURATION_MINUTES_LONG")],
        ]

        dryer_keyboard = [
            [InlineKeyboardButton("30", callback_data=f"{machine_id},DRYER_TIMER_DURATION_MINUTES_SHORT")],
            [InlineKeyboardButton("45", callback_data=f"{machine_id},DRYER_TIMER_DURATION_MINUTES_MID")],
            [InlineKeyboardButton("60", callback_data=f"{machine_id},DRYER_TIMER_DURATION_MINUTES_LONG")],
        ]
        if "Washer" in machine_name:
            reply_markup = InlineKeyboardMarkup(washer_keyboard)
        else:
            reply_markup = InlineKeyboardMarkup(dryer_keyboard)

        # Ask user to select the duration before starting the machine
        text = f"Please select the wash duration for {machine_name}:"
        await query.edit_message_text(text=text, reply_markup=reply_markup)
    
        return constants.ConvState.SetDuration
    
    return set_timer


