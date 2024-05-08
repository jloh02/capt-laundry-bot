import logging
import datetime
import constants
import storage
import commands
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
from set_timer_machine import set_timer_machine
from config import config, read_dotenv

read_dotenv()
storage.read_timers()


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("apscheduler.scheduler").setLevel(logging.WARNING)
logging.getLogger("apscheduler.executors.default").setLevel(logging.WARNING)

logger = logging.getLogger("main")

TBOT = Bot(config.get("TELEGRAM_BOT_API_KEY"))

DRYER_ONE = Machine("Dryer One")
DRYER_TWO = Machine("Dryer Two")
WASHER_ONE = Machine("Washer One")
WASHER_TWO = Machine("Washer Two")

COMMANDS_DICT = {
    "start": "Display help page and version",
    "select": constants.SELECT_COMMAND_DESCRIPTION,
    "status": constants.STATUS_COMMAND_DESCRIPTION,
}

TBOT.set_my_commands(COMMANDS_DICT.items())


def main():
    application = (
        Application.builder().token(config.get("TELEGRAM_BOT_API_KEY")).build()
    )

    MENU_DICT = {
        "exit": commands.cancel,
        "exits": commands.cancel,
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

    COMMANDS = [
        CommandHandler("start", commands.start),
        CommandHandler("select", commands.select),
        CommandHandler(
            "status",
            commands.create_status_command(
                DRYER_ONE, DRYER_TWO, WASHER_ONE, WASHER_TWO
            ),
        ),
    ]
    conv_handler = ConversationHandler(
        entry_points=COMMANDS,
        states={
            constants.STATES.get("MENU"): [
                CallbackQueryHandler(fn, pattern=f"^{cmd}$")
                for cmd, fn in MENU_DICT.items()
            ]
        },
        fallbacks=COMMANDS,
    )

    application.add_handler(conv_handler)
    application.add_error_handler(
        lambda update, context: logger.error(
            f"Update {update} caused error: {context.error}"
        )
    )

    application.job_queue.run_repeating(
        send_alarms, interval=datetime.timedelta(minutes=1)
    )

    if config.get("PRODUCTION"):
        application.run_webhook(
            listen="0.0.0.0",
            port=config.get("PORT"),
            webhook_url=config.get("WEBHOOK_URL"),
        )
    else:
        application.run_polling()


async def send_alarms(context=None):
    for curr_user, chat_id in storage.check_alarms():
        logger.info(f"Sending alarm to {curr_user} in chat {chat_id}")
        await TBOT.send_message(
            chat_id=chat_id,
            text=f"@{curr_user} {constants.COMPLETION_MESSAGE}",
        )


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
        return constants.STATES.get("MENU")

    return callback


EXIT_INLINE_KEYBOARD = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Exit", callback_data="exits")]]
)


async def backtomenu(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        constants.WELCOME_MESSAGE,
        reply_markup=EXIT_INLINE_KEYBOARD,
    )


if __name__ == "__main__":
    main()
