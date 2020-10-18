from typing import TYPE_CHECKING, Callable, List

from telegram import Update

if TYPE_CHECKING:
    from telegram.ext import CallbackContext, Dispatcher, Handler


class State:
    def __init__(self, name: str, on_activate: Callable, handlers: List['Handler']):
        self.name = name
        self.on_activate: Callable = on_activate
        self.handlers: List['Handler'] = handlers

    def activate(self, update: 'Update', context: 'CallbackContext'):
        return self.on_activate(update, context)

    def handle(
        self,
        update: 'Update',
        dispatcher: 'Dispatcher',
        context: 'CallbackContext' = None,
    ):
        for handler in self.handlers:
            check_result = handler.check_update(update)
            if check_result:
                return handler.handle_update(update, dispatcher, check_result, context)
