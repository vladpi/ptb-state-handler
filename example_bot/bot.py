import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Dispatcher, Updater

from example_bot import states_names
from example_bot.states import about_state, contacts_state, main_menu_state
from state_handler import StateHandler


def entry(update: 'Update', context: 'CallbackContext'):
    return states_names.MAIN_MENU


def main():
    load_dotenv()
    bot_token = os.getenv('BOT_TOKEN', 'PLACE_YOU_BOT_TOKEN_HERE')

    updater = Updater(bot_token, use_context=True)
    dp: Dispatcher = updater.dispatcher

    state_handler = StateHandler(
        entry_point=CommandHandler('start', entry),
        states=[main_menu_state, about_state, contacts_state],
    )

    dp.add_handler(state_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
