from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext, filters, MessageHandler

from example_bot import buttons, states_names
from state_handler import State

from .common import back


async def activator(update: Update, context: CallbackContext):
    keyboard = [[buttons.ABOUT], [buttons.BACK]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.effective_message.reply_text(
        f"Its contacts section\n\n{context.user_data}", reply_markup=reply_markup
    )


async def to_about(update: Update, context: CallbackContext):
    return states_names.ABOUT


contacts_state = State(
    name=states_names.CONTACTS,
    on_activate=activator,
    handlers=[
        MessageHandler(filters.Text(buttons.BACK), back),
        MessageHandler(filters.Text(buttons.ABOUT), to_about),
    ],
)
