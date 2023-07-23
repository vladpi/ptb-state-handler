from typing import TYPE_CHECKING

from state_handler import StateHandler

if TYPE_CHECKING:
    from telegram import Update
    from telegram.ext import CallbackContext


async def back(update: "Update", context: "CallbackContext"):
    return StateHandler.BACK
