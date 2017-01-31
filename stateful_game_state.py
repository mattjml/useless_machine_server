#!/usr/bin/env python3

from datetime import datetime
import random
import uuid

from game_state import (
    GameState, InvalidUserActionError, UserAlreadyExistsError, UserDoesntExistError
)

class StatefulGameState(GameState):
    """
    Locally stateful implementation of game_state.GameState.
    """
    def __init__(self, config):
        self.state = {}
        super().__init__(config)

    @staticmethod
    def _convert_uuid(id):
        """
        Converts string id, if a UUID, to UUID type.
        :param string/UUID id:

        :return UUID:

        :raises UserDoesntExistError: If id is not a valid UUID
        """
        try:
            if type(id) == str:
                id = uuid.UUID(id)
        except TypeError as error:
            raise UserDoesntExistError('invalid user uuid') from error
        return id
    
    def user_action(self, user_id, user_action):
        """
        Handle user action. Updates internal state and responds with user response.
        Raises UserDoesntExistError if user is already added to game
        Raises InvalidUserActionError if an invalid action is supplied

        Overrides GameState.user_action
        """
        result = None
        user_id = self.__class__._convert_uuid(user_id)
        print(user_action)
        if user_action['code'] == 'BUTTON_PRESS':
            print(user_action)
            result = self.handle_button_press(user_id, user_action)
        elif user_action['code'] == 'CHECK_IF_ALERTED':
            result = self.handle_check_if_alerted(user_id, user_action)
        else:
            raise InvalidUserActionError('{} is not a valid action'.format(user_action['code']))
        return result

    def add_user(self, user_id):
        """
        Add new user to game. Updates internal state with new user.
        Raises UserAlreadyExistsError if user is already added to game

        Overrides GameState.add_user
        """
        user_id = self.__class__._convert_uuid(user_id)
        if user_id in self.state.keys():
            raise UserAlreadyExistsError()

        self.state[user_id] = {
            'user_id': user_id,
            'last_pressed': None,
            'alert_state': None
        }

    def remove_user(self, user_id):
        """
        Remove user from game. Removes from internal state.
        Raises UserDoesntExistError if user has not been added to game

        Overrides GameState.remove_user
        """
        user_id = self.__class__._convert_uuid(user_id)
        try:
            del self.state[user_id]
        except KeyError as error:
            raise UserDoesntExistError() from error

    def clean_up(self):
        """
        Clears game state. Resets local game state dictionary.

        Overrides GameState.clean_up
        """
        self.state = {}

    def find_state(self, user_id):
        """
        Searches for state for user_id
        :param UUID user_id:

        :return state dict:

        :raises UserDoesntExistError:
        """
        state = None
        try:
            state = self.state[user_id]
        except KeyError as error:
            raise UserDoesntExistError() from error
        return state

    def handle_button_press(self, user_id, user_action):
        """
        Handles button press user action. Updates internal state, removing alert and updating
        last_pressed time.

        :param UUID user_id:
        :param dict user_action:

        :return dict: user action response

        :raises UserDoesntExistError:
        """
        state = self.find_state(user_id)
        state['last_pressed'] = datetime.now()
        state['alert_state'] = False
        other_users_state = [state for (id, state) in self.state.items() if id != user_id]
        for other_user_state in other_users_state:
            other_user_state['alert_state'] = bool(random.getrandbits(1))
        return self.__class__.create_user_button_press_response(user_id, user_action, True)

    def handle_check_if_alerted(self, user_id, user_action):
        """
        Handles check if alerted user action press. Updates internal state, removing alert and
        updating last_pressed time

        :param UUID user_id:
        :param dict user_action:

        :return dict: user action response

        :raises UserDoesntExistError:
        """
        return self.__class__.create_user_check_if_alerted_response(
            user_id,
            user_action,
            self.find_state(user_id)['alert_state']
        )
