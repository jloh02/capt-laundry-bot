from enum import Enum

USER_DATA_KEY_HOUSE = "house"
USER_DATA_KEY_CALLBACK = "callback"
USER_DATA_KEY_BOT_MSG = "bot_msg"

HOUSES = {
    "ROC": "\U0001F499\U0001F43A ROC \U0001F43A\U0001F499",
    "Dragon": "\U0001F340\U0001F409 Dragon \U0001F409\U0001F340",
    "Garuda": "\U0001F34C\U0001F648 Garuda \U0001F648\U0001F34C",
    "Phoenix": "\U0001F525\U0001F425 Phoenix \U0001F425\U0001F525",
    "Tulpar": "\U0001F5A4\U0001F434 Tulpar \U0001F434\U0001F5A4",
}
MACHINE_NAMES = ["Dryer One", "Dryer Two", "Washer One", "Washer Two"]


class ConvState(str, Enum):
    RequestConfirmSelect = "RequestConfirmSelect"
    ConfirmSelect = "ConfirmSelect"
    SelectHouse = "SelectHouse"
    StatusSelectHouse = "StatusSelectHouse"
    SetDuration = "SetDuration"


SELECT_COMMAND_DESCRIPTION = "Select the washer/dryer that you want to use"
STATUS_COMMAND_DESCRIPTION = "Check the status of Washers and Dryers"

WELCOME_MESSAGE = f"Welcome to CAPT Laundry Bot!\n\nUse the following commands to use this bot:\n/select: {SELECT_COMMAND_DESCRIPTION}\n/status: {STATUS_COMMAND_DESCRIPTION}\n\nThank you for using the bot!\nDeveloped by: @jloh02, @zozibo"
