from collections import defaultdict
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from telegram import Chat
from telegram.ext import CallbackContext, Application, BaseHandler, ConversationHandler

from .state import State

if TYPE_CHECKING:
    from telegram import Update


class StateHandler(BaseHandler):
    BACK = '_back'

    def __init__(
        self, entry_point: BaseHandler, states: List[State], allow_reentry: bool = True
    ):
        super().__init__(...)
        self.entry_point = entry_point
        self.states = self._states_to_mapping(states)
        self.users_states = defaultdict(list)
        self.allow_reentry = allow_reentry

    @staticmethod
    def _states_to_mapping(states: List[State]) -> Dict[str, State]:
        states_mapping = {}
        for state in states:
            if state.name in states_mapping:
                raise ValueError(f'Duplicate state name: {state.name}')

            states_mapping[state.name] = state

        return states_mapping

    def check_update(self, update: 'Update'):
        if update.effective_chat.type != Chat.PRIVATE:
            return False

        user_id, user_state = self._get_current_user_state(update)

        entry_check_result = self.entry_point.check_update(update)

        if not user_state or (self.allow_reentry and entry_check_result):
            return entry_check_result

        else:
            return True

    async def handle_update(
        self,
        update: 'Update',
        application: 'Application',
        check_result: Any,
        context: Optional['CallbackContext'] = None,
    ):
        user_id, user_state = self._get_current_user_state(update)

        reentry = self.allow_reentry and self.entry_point.check_update(update)

        if reentry or not user_state:
            new_state_key = await self.entry_point.handle_update(
                update, application, check_result, context
            )
            self.__clear_user_states(user_id)

        else:
            new_state_key = await user_state.handle(update, application, context)

        if new_state_key:
            await self.activate_state(user_id, new_state_key, update, context)

    def _get_current_user_state(self, update: 'Update'):
        user = update.effective_user
        user_states = self.__get_user_states(user.id)

        if user_states:
            user_state_key = user_states[-1]
            user_state = self.states.get(user_state_key, None)

            return user.id, user_state

        return user.id, None

    async def activate_state(
        self, user_id: int, state_key: str, update: 'Update', context: 'CallbackContext'
    ):
        if state_key == self.BACK:
            self.__pop_user_state(user_id)
            state_key = self.__pop_user_state(user_id)

        state = self.states.get(state_key, None)

        if state:
            result_state_key = await state.activate(update, context)

            if result_state_key:
                await self.activate_state(user_id, result_state_key, update, context)

            else:
                self.__set_user_state(user_id, state_key)

    def __set_user_state(self, user_id: int, state: str):
        self.users_states[user_id].append(state)

    def __get_user_states(self, user_id: int):
        return self.users_states.get(user_id)

    def __pop_user_state(self, user_id: int):
        return self.users_states.get(user_id).pop()

    def __clear_user_states(self, user_id: int):
        self.users_states[user_id] = []
