from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext, Filters, MessageHandler

from example_bot import buttons, states_names
from state_handler import State


def activator(update: Update, context: CallbackContext):
    keyboard = [[buttons.ABOUT, buttons.CONTACTS]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.effective_message.reply_text('Its main menu', reply_markup=reply_markup)


def to_about(update: Update, context: CallbackContext):
    return states_names.ABOUT


def to_contacts(update: Update, context: CallbackContext):
    return states_names.CONTACTS


main_menu_state = State(
    name=states_names.MAIN_MENU,
    on_activate=activator,
    handlers=[
        MessageHandler(Filters.text(buttons.ABOUT), to_about),
        MessageHandler(Filters.text(buttons.CONTACTS), to_contacts),
    ],
)
