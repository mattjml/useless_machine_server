#!/usr/bin/env python3

#### Imports ####

from jsonschema import Draft4Validator
from jsonschema.exceptions import ValidationError

from helpers import raise_not_implemented_error

#### Constants ####
USER_ACTION_CODES = ['BUTTON_PRESS', 'CHECK_IF_ALERTED', 'START', 'STOP']
USER_ACTION = {
    'type': 'object',
    'properties': {
        'api': {
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
                'version': {'type': 'integer'}
            },
            'required': ['name', 'version']
        },
        'action': {
            'type': 'object',
            'properties': {
                'code': {'enum': USER_ACTION_CODES},
                'data': {'type': 'object'}
            },
            'required': ['code']
        }
    },
    'required': ['api', 'action']
}
USER_ACTION_VALIDATOR = Draft4Validator(USER_ACTION)

#### Classes ####

class InvalidUserActionError(Exception):
    """
    Raised on parsing an invalid user_action dictionary
    """
    pass

class UserAlreadyExistsError(Exception):
    """
    Raised on adding a pre-added user to the game state or attempting a game action with
    a non-existent user
    """
    pass

class UserDoesntExistError(Exception):
    """
    Raised on removing a non-added user from the game state
    """
    pass

class GameState:
    """
    Abstract implementation of game state and its control.
    Concrete implementations of this class are responsible for managing and updating game state
    """

    def __init__(self, config):
        self.config = config

    @staticmethod
    def validate_user_action(user_action):
        """
        Validate user_action dictionary against USER_ACTION schema

        :param user_action:

        :return None:

        :raises InvalidUserActionError:
        """
        try:
            USER_ACTION_VALIDATOR.validate(user_action)
        except ValidationError as error:
            raise InvalidUserActionError('user action does not meet the JSON schema') from error

    @staticmethod
    def create_user_button_press_response(user_id, user_action, success):
        """
        Creates dictionary ready to be jsonify'd that contains response to 'BUTTON_PRESS' user
        action.
        :param uuid.UUID user_id: user UUID
        :param dict user_action:
        :param bool success:
        :return dict:
        """
        return {
            'user_id': user_id,
            'user_action': user_action,
            'response': {
                'success': success
            }
        }

    @staticmethod
    def create_user_check_if_alerted_response(user_id, user_action, alerted):
        """
        Creates dictionary ready to be jsonify'd that contains response to 'CHECK_IF_ALERTED' user
        action.
        :param uuid.UUID user_id: user UUID
        :param dict user_action:
        :param bool alerted:
        :return dict:
        """
        return {
            'user_id': user_id,
            'user_action': user_action,
            'response': {
                'alerted': alerted
            }
        }

    @staticmethod
    def create_user_start_stop_response(user_id, user_action, success):
        """
        Creates dictionary ready to be jsonify'd that contains response to 'START' or 'STOP' user
        actions.
        :param uuid.UUID user_id: user UUID
        :param dict user_action:
        :param bool success:
        :return dict:
        """
        return {
            'user_id': user_id,
            'user_action': user_action,
            'response': {
                'success': success
            }
        }
    
    def user_action(self, user_id, user_action):
        """
        Handle user action

        :param string/uuid.UUID user_id: user UUID
        :param dict user_action: This must follow the USER_ACTION schema

        :return dict: user action response

        :raises InvalidUserActionError:
        :raises UserDoesntExistError:
        """
        raise_not_implemented_error(self.user_action.__name__)

    def add_user(self, user_id):
        """
        Add new user to game

        :param string/uuid.UUID user_id: user UUID

        :return None:

        :raises UserAlreadyExistsError: If user is already added to game
        """
        raise_not_implemented_error(self.add_user.__name__)

    def remove_user(self, user_id):
        """
        Remove user from game

        :param string/uuid.UUID user_id: user UUID

        :return None:

        :raises UserDoesntExistError: If user has not been added to game
        """
        raise_not_implemented_error(self.remove_user.__name__)

    def clean_up(self):
        """
        Clears game state.

        :return None:
        """
