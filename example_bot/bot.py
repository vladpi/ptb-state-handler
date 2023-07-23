import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CallbackContext,
    CommandHandler,
)

from example_bot import states_names
from example_bot.states import about_state, contacts_state, main_menu_state
from state_handler import StateHandler


async def entry(update: "Update", context: "CallbackContext"):
    return states_names.MAIN_MENU


def main():
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN", "<PLACE_YOUR_BOT_TOKEN_HERE>")

    application = Application.builder().token(bot_token).build()

    state_handler = StateHandler(
        entry_point=CommandHandler("start", entry),
        states=[main_menu_state, about_state, contacts_state],
    )

    application.add_handler(state_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
