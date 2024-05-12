import logging
import datetime
import constants
import storage
import commands
from telegram import Bot, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
)
from machine import Machine
from double_confirm import create_double_confirm
from select_house import select_house_completed
from status_select_house import create_status_select_house
from set_timer_machine import set_timer_machine
from convo_timeout import timeout_on_callback_query, timeout_on_message
from config import config, read_dotenv
from utils import with_house_context, with_deleted_previous_keyboards

read_dotenv()
storage.read_timers()
storage.read_house()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("apscheduler.scheduler").setLevel(logging.WARNING)
logging.getLogger("apscheduler.executors.default").setLevel(logging.WARNING)

logger = logging.getLogger("main")

TBOT = Bot(config.get("TELEGRAM_BOT_API_KEY"))

MACHINES = {}
for house_id in constants.HOUSES.keys():
    MACHINES.update(
        {
            house_id: dict(
                [
                    [machine_name, Machine(house_id, machine_name)]
                    for machine_name in constants.MACHINE_NAMES
                ]
            )
        }
    )

COMMANDS_DICT = {
    "start": "Display help page",
    "select": constants.SELECT_COMMAND_DESCRIPTION,
    "status": constants.STATUS_COMMAND_DESCRIPTION,
}

TBOT.set_my_commands(COMMANDS_DICT.items())


def main():
    application = (
        Application.builder().token(config.get("TELEGRAM_BOT_API_KEY")).build()
    )

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", commands.start),
            CommandHandler(
                "select",
                with_deleted_previous_keyboards(
                    with_house_context(commands.create_select_menu())
                ),
            ),
            CommandHandler(
                "status",
                with_deleted_previous_keyboards(
                    with_house_context(commands.create_status_command(MACHINES))
                ),
            ),
        ],
        states={
            constants.ConvState.RequestConfirmSelect: [
                CallbackQueryHandler(create_double_confirm(MACHINES))
            ],
            constants.ConvState.ConfirmSelect: [
                CallbackQueryHandler(backtomenu, pattern=r"^no$"),
                CallbackQueryHandler(set_timer_machine(MACHINES), pattern=r"^yes|.*$"),
            ],
            constants.ConvState.SelectHouse: [
                CallbackQueryHandler(select_house_completed)
            ],
            constants.ConvState.StatusSelectHouse: [
                CallbackQueryHandler(create_status_select_house(MACHINES))
            ],
            ConversationHandler.TIMEOUT: [
                MessageHandler(None, timeout_on_message),
                CallbackQueryHandler(timeout_on_callback_query),
            ],
        },
        fallbacks=[],
        allow_reentry=True,
        conversation_timeout=datetime.timedelta(
            seconds=config.get("CONVO_TIMEOUT_SECONDS", 300)
        ),
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
    for curr_user, chat_id, thread_id, machine_house_name in storage.check_alarms():
        logger.info(f"Sending alarm to {curr_user} in chat {chat_id}#{thread_id}")
        await TBOT.send_message(
            chat_id=chat_id,
            message_thread_id=thread_id,
            text=f"@{curr_user} your clothes from {machine_house_name} are ready for collection! Please collect them now so that others may use it!",
        )


async def backtomenu(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(constants.WELCOME_MESSAGE)


if __name__ == "__main__":
    main()
