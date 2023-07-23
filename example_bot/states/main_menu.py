from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext, filters, MessageHandler

from example_bot import buttons, states_names
from state_handler import State


async def activator(update: Update, context: CallbackContext):
    keyboard = [[buttons.ABOUT, buttons.CONTACTS]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.effective_message.reply_text(
        "Its main menu", reply_markup=reply_markup
    )


async def to_about(update: Update, context: CallbackContext):
    return states_names.ABOUT


async def to_contacts(update: Update, context: CallbackContext):
    return states_names.CONTACTS


main_menu_state = State(
    name=states_names.MAIN_MENU,
    on_activate=activator,
    handlers=[
        MessageHandler(filters.Text(buttons.ABOUT), to_about),
        MessageHandler(filters.Text(buttons.CONTACTS), to_contacts),
    ],
)
