from enum import Enum

HOUSES = {
    "ROC": "ROC",
    "Dragon": "\U0001F334\U0001F340\U0001F409 Dragon \U0001F409\U0001F340\U0001F334",
    "Garuda": "Garuda",
    "Phoenix": "Phoenix",
    "Tulpar": "Tulpar",
}
MACHINE_NAMES = ["Dryer One", "Dryer Two", "Washer One", "Washer Two"]


class ConvState(str, Enum):
    RequestConfirmSelect = "RequestConfirmSelect"
    ConfirmSelect = "ConfirmSelect"
    SelectHouse = "SelectHouse"
    StatusSelectHouse = "StatusSelectHouse"


SELECT_COMMAND_DESCRIPTION = "Select the washer/dryer that you want to use"
STATUS_COMMAND_DESCRIPTION = "Check the status of Washers and Dryers"

WELCOME_MESSAGE = f"Welcome to CAPT Laundry Bot!\n\nUse the following commands to use this bot:\n/select: {SELECT_COMMAND_DESCRIPTION}\n/status: {STATUS_COMMAND_DESCRIPTION}\n\nThank you for using the bot!\nDeveloped by: @jloh02"
