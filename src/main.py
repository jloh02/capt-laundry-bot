import datetime
import strings
import storage
from telegram import (
    Bot,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
)
from machine import Machine
from config import config, read_dotenv

read_dotenv()
storage.read_timers()

MENU = 1

TBOT = Bot(config.get("TELEGRAM_BOT_API_KEY"))

WASHER_TIMER = 34 * 60
DRYER_TIMER = 34 * 60
DRYER_ONE = Machine(DRYER_TIMER, "DRYER ONE")
DRYER_TWO = Machine(DRYER_TIMER, "DRYER TWO")
WASHER_ONE = Machine(WASHER_TIMER, "WASHER ONE")
WASHER_TWO = Machine(WASHER_TIMER, "WASHER TWO")


COMMANDS_DICT = {
    "start": "Display help page and version",
    "select": strings.SELECT_COMMAND_DESCRIPTION,
    "status": strings.STATUS_COMMAND_DESCRIPTION,
}

TBOT.set_my_commands(COMMANDS_DICT.items())


def main():
    application = (
        Application.builder().token(config.get("TELEGRAM_BOT_API_KEY")).build()
    )

    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'

    ENTRY_POINT_DICT = {
        "start": start,
        "select": select,
        "status": status,
    }
    FALLBACK_DICT = ENTRY_POINT_DICT

    MENU_DICT = {
        "exit": cancel,
        "exits": cancel,
        "dryer_one": create_double_confirm_callback("dryer_one"),
        "dryer_two": create_double_confirm_callback("dryer_two"),
        "washer_one": create_double_confirm_callback("washer_one"),
        "washer_two": create_double_confirm_callback("washer_two"),
        "no_dryer_one": backtomenu,
        "no_dryer_two": backtomenu,
        "no_washer_one": backtomenu,
        "no_washer_two": backtomenu,
        "yes_dryer_one": set_timer_machine(DRYER_ONE),
        "yes_dryer_two": set_timer_machine(DRYER_TWO),
        "yes_washer_one": set_timer_machine(WASHER_ONE),
        "yes_washer_two": set_timer_machine(WASHER_TWO),
    }

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler(cmd, fn) for cmd, fn in ENTRY_POINT_DICT.items()],
        states={
            MENU: [
                CallbackQueryHandler(fn, pattern=f"^{cmd}$")
                for cmd, fn in MENU_DICT.items()
            ]
        },
        fallbacks=[CommandHandler(cmd, fn) for cmd, fn in FALLBACK_DICT.items()],
    )

    application.add_handler(conv_handler)

    application.job_queue.run_repeating(
        send_alarms, interval=datetime.timedelta(minutes=1)
    )
    send_alarms()

    if config.get("PRODUCTION"):
        application.run_webhook(
            listen="0.0.0.0",
            port=config.get("PORT"),
            webhook_url=config.get("WEBHOOK_URL"),
        )
    else:
        application.run_polling()


START_INLINE_KEYBOARD = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Exit", callback_data="exit")]]
)


async def send_alarms(context=None):
    for curr_user, chat_id in storage.check_alarms():
        await TBOT.send_message(
            chat_id=chat_id,
            text=f"@{curr_user} {strings.COMPLETION_MESSAGE}",
        )


async def start(update: Update, context: CallbackContext):
    if len(context.args) > 0:
        return

    await update.message.reply_text(
        strings.WELCOME_MESSAGE,
        reply_markup=START_INLINE_KEYBOARD,
    )
    return MENU


SELECT_MACHINE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Dryer One", callback_data="dryer_one"),
            InlineKeyboardButton("Dryer Two", callback_data="dryer_two"),
        ],
        [
            InlineKeyboardButton("Washer One", callback_data="washer_one"),
            InlineKeyboardButton("Washer Two", callback_data="washer_two"),
        ],
        [InlineKeyboardButton("Exit", callback_data="exit")],
    ]
)


async def select(update: Update, context: CallbackContext):
    # Don't allow users to use /select command in group chats
    if update.message.chat.type != "private":
        return MENU

    await update.message.reply_text(
        "\U0001F606\U0001F923 Please choose a service: \U0001F606\U0001F923",
        reply_markup=SELECT_MACHINE_INLINE_KEYBOARD,
    )
    return MENU


async def cancel(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Bye! Use /start again to call me again!")
    return ConversationHandler.END


def create_inline_for_callback(machine_name):
    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Yes", callback_data=f"yes_{machine_name}"),
            ],
            [InlineKeyboardButton("No", callback_data=f"no_{machine_name}")],
        ]
    )
    text = f"Timer for {machine_name.upper().replace('_',' ')} will begin?"
    return (text, markup)


def create_double_confirm_callback(machine_name: str):
    text, markup = create_inline_for_callback(machine_name)

    async def callback(update: Update, _: CallbackContext) -> int:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=text, reply_markup=markup)
        return MENU

    return callback


EXIT_INLINE_KEYBOARD = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Exit", callback_data="exits")]]
)


async def backtomenu(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        strings.WELCOME_MESSAGE,
        reply_markup=EXIT_INLINE_KEYBOARD,
    )


def alarm(context: CallbackContext, machine: Machine) -> None:
    job = context.job
    context.bot.send_message(
        job.context,
        text=f"@{machine.get_curr_user} {strings.COMPLETION_MESSAGE}",
    )


def set_timer_machine(machine: Machine):
    async def set_timer(update, context):
        machine_name = machine.get_name()
        upper_name = machine_name.upper()
        underscore_name = machine_name.lower().replace(" ", "_")

        chat_id = update.effective_message.chat_id
        query = update.callback_query
        await query.answer()

        if not (machine.start_machine(update.effective_message.chat.username, chat_id)):
            text = f"{upper_name} is currently in use. Please come back again later!"
            await query.edit_message_text(text=text)
        else:
            text = f"Timer Set for {machine.time_left_mins()}mins for {upper_name}. Please come back again!"
            await query.edit_message_text(text=text)

        return MENU

    return set_timer


async def status(update: Update, context: CallbackContext):
    DRYER_ONE_TIMER = DRYER_ONE.status()
    DRYER_TWO_TIMER = DRYER_TWO.status()
    WASHER_ONE_TIMER = WASHER_ONE.status()
    WASHER_TWO_TIMER = WASHER_TWO.status()

    reply_text = f"""Status of Laundry Machines:
  
Dryer One: {DRYER_ONE_TIMER}
  
Dryer Two: {DRYER_TWO_TIMER}
  
Washer One: {WASHER_ONE_TIMER}
  
Washer Two: {WASHER_TWO_TIMER}"""

    await update.message.reply_text(reply_text)


if __name__ == "__main__":
    main()
