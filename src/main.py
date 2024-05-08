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

MACHINES = {
    "Dryer One": Machine("Dryer One"),
    "Dryer Two": Machine("Dryer Two"),
    "Washer One": Machine("Washer One"),
    "Washer Two": Machine("Washer Two"),
}

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
    }

    COMMANDS = [
        CommandHandler("start", commands.start),
        CommandHandler("select", commands.create_select_menu(MACHINES)),
        CommandHandler(
            "status",
            commands.create_status_command(MACHINES),
        ),
    ]
    conv_handler = ConversationHandler(
        entry_points=COMMANDS,
        states={
            constants.ConvState.Menu: [
                CallbackQueryHandler(fn, pattern=f"^{cmd}$")
                for cmd, fn in MENU_DICT.items()
            ],
            constants.ConvState.RequestConfirmSelect: [
                CallbackQueryHandler(double_confirm)
            ],
            constants.ConvState.ConfirmSelect: [
                CallbackQueryHandler(backtomenu, pattern=r"^no$"),
                CallbackQueryHandler(set_timer_machine(MACHINES), pattern=r"^yes|.*$"),
            ],
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
        send_alarms, interval=datetime.timedelta(seconds=30)
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


async def double_confirm(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    machine_id = query.data
    machine = MACHINES.get(machine_id)

    if machine == None:
        raise Exception(f"Unknown machine {machine_id}")

    machine_name = machine.get_name()

    await query.edit_message_text(
        text=f"Timer for {machine_name} will begin?",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Yes", callback_data=f"yes|{machine_id}")],
                [InlineKeyboardButton("No", callback_data="no")],
            ]
        ),
    )

    return constants.ConvState.ConfirmSelect


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
