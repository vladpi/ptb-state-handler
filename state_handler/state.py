from typing import TYPE_CHECKING, Callable, List

from telegram import Update

if TYPE_CHECKING:
    from telegram.ext import CallbackContext, Application, BaseHandler


class State:
    def __init__(self, name: str, on_activate: Callable, handlers: List['BaseHandler']):
        self.name = name
        self.on_activate: Callable = on_activate
        self.handlers: List['BaseHandler'] = handlers

    async def activate(self, update: 'Update', context: 'CallbackContext'):
        return await self.on_activate(update, context)

    async def handle(
        self,
        update: 'Update',
        application: 'Application',
        context: 'CallbackContext' = None,
    ):
        for handler in self.handlers:
            check_result = handler.check_update(update)
            if check_result:
                return await handler.handle_update(update, application, check_result, context)
