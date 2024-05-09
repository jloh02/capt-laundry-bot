import logging
import storage
import constants
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import CallbackContext, ConversationHandler

logger = logging.getLogger("select_house")

select_house_global = None


def create_select_house():
    global select_house_global
    if select_house_global:
        return select_house_global

    keyboard = []
    houses = list(constants.HOUSES.items())
    num_houses = len(houses)
    for i in range(0, num_houses, 2):
        house_id0, house_name0 = houses[i]
        if i + 1 == num_houses:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        house_name0,
                        callback_data=house_id0,
                    )
                ]
            )
        else:
            house_id1, house_name1 = houses[i + 1]
            keyboard.append(
                [
                    InlineKeyboardButton(
                        house_name0,
                        callback_data=house_id0,
                    ),
                    InlineKeyboardButton(
                        house_name1,
                        callback_data=house_id1,
                    ),
                ]
            )
    keyboard_markup = InlineKeyboardMarkup(keyboard)

    async def select_house(update: Update, context: CallbackContext) -> int:
        logger.info(f"{update.effective_user.username} started select house")

        send_message_method = (
            update.callback_query.edit_message_text
            if update.callback_query
            else update.effective_message.reply_text
        )

        await send_message_method(
            "Please choose your house:",
            reply_markup=keyboard_markup,
        )
        return constants.ConvState.SelectHouse

    select_house_global = select_house
    return select_house


async def select_house_completed(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    house = query.data
    logger.info(
        f"{update.effective_user.username} selected house for chat {update.effective_chat.id}: {house}"
    )
    context.chat_data.update({"house": house})
    storage.write_house(update.effective_chat.id, house)

    callback = context.chat_data.get("callback")

    return await callback(update, context) if callback else ConversationHandler.END
