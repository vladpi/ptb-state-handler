from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext, filters, MessageHandler

from example_bot import buttons, states_names
from state_handler import State

from .common import back


async def activator(update: Update, context: CallbackContext):
    keyboard = [[buttons.CONTACTS], [buttons.BACK]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.effective_message.reply_text(
        "Its about section", reply_markup=reply_markup
    )


async def to_contacts(update: Update, context: CallbackContext):
    return states_names.CONTACTS


about_state = State(
    name=states_names.ABOUT,
    on_activate=activator,
    handlers=[
        MessageHandler(filters.Text(buttons.BACK), back),
        MessageHandler(filters.Text(buttons.CONTACTS), to_contacts),
    ],
)
