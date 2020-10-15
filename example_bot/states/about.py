from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext, Filters, MessageHandler

from example_bot import buttons, states_names
from state_handler import State

from .common import back


def activator(update: Update, context: CallbackContext):
    keyboard = [[buttons.CONTACTS], [buttons.BACK]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.effective_message.reply_text('Its about section', reply_markup=reply_markup)


def to_contacts(update: Update, context: CallbackContext):
    return states_names.CONTACTS


about_state = State(
    name=states_names.ABOUT,
    on_activate=activator,
    handlers=[
        MessageHandler(Filters.text(buttons.BACK), back),
        MessageHandler(Filters.text(buttons.CONTACTS), to_contacts),
    ],
)
