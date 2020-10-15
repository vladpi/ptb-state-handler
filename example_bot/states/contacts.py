from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext, Filters, MessageHandler

from example_bot import buttons, states_names
from state_handler import State

from .common import back


def activator(update: Update, context: CallbackContext):
    keyboard = [[buttons.ABOUT], [buttons.BACK]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.effective_message.reply_text(
        f'Its contacts section\n\n{context.user_data}', reply_markup=reply_markup
    )


def to_about(update: Update, context: CallbackContext):
    return states_names.ABOUT


contacts_state = State(
    name=states_names.CONTACTS,
    on_activate=activator,
    handlers=[
        MessageHandler(Filters.text(buttons.BACK), back),
        MessageHandler(Filters.text(buttons.ABOUT), to_about),
    ],
)
