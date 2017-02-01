#!/usr/bin/env python3

import nose
from nose.tools import raises
import os
import sys

from .helper import gen_id

# Allow relative imports of the parent modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from game_state import GameState, InvalidUserActionError


#### Helper functions ####

#### Tests ####
#GameState.create_user_button_press_response()
#GameState.create_user_check_if_alerted_response()
#@raises(UserDoesntExistError)
#def test_validate_user_action_nonexistant_user():
#    gs, id = create_gs_and_add_user({})
#    gs.validate_user_action(gen_id(), {'code': 'CHECK_IF_ALERTED'})

#@raises(InvalidUserActionError)
#def test_validate_user_action_nonexistant_action():
#    gs, id = create_gs_and_add_user({})
#    gs.validate_user_action(id, {'code': 'CHECK_IF_ALERTIFIED'})


def create_user_action(code):
    return {
        'api': {
            'name': 'stateful',
            'version': 1
        },
        'action': {'code': code}
    }

def create_user_action_check_if_alerted():
    return create_user_action('CHECK_IF_ALERTED')

def validate_check_if_alerted_response(id, response, action, expected_alert_state):
    nose.tools.ok_(response['user_id'] == id)
    nose.tools.ok_(response['user_action']['action'] == action['action'])
    nose.tools.ok_(len(response['response'].keys()) == 1)
    nose.tools.ok_(response['response']['alerted'] == expected_alert_state)

#### Tests ####
@raises(InvalidUserActionError)
def test_validate_user_action_nonexistant_action():
    action = create_user_action('CHECK_IF_ALERTIFIED')
    GameState.validate_user_action(action)

@raises(InvalidUserActionError)
def test_validate_user_action_no_api_detais():
    action = create_user_action_check_if_alerted()
    del action['api']
    GameState.validate_user_action(action)

@raises(InvalidUserActionError)
def test_validate_user_action_no_api_name():
    action = create_user_action_check_if_alerted()
    del action['api']['name']
    GameState.validate_user_action(action)

@raises(InvalidUserActionError)
def test_validate_user_action_no_api_version():
    action = create_user_action_check_if_alerted()
    del action['api']['version']
    GameState.validate_user_action(action)

@raises(InvalidUserActionError)
def test_validate_user_action_no_action_details():
    action = create_user_action_check_if_alerted()
    del action['action']
    GameState.validate_user_action(action)

@raises(InvalidUserActionError)
def test_validate_user_action_no_action_code():
    action = create_user_action_check_if_alerted()
    del action['action']['code']
    GameState.validate_user_action(action)

@raises(InvalidUserActionError)
def test_validate_user_action_wrong_api_name_type():
    action = create_user_action_check_if_alerted()
    action['api']['name'] = 2
    GameState.validate_user_action(action)

@raises(InvalidUserActionError)
def test_validate_user_action_wrong_api_version_type():
    action = create_user_action_check_if_alerted()
    action['api']['version'] = 'baguette'
    GameState.validate_user_action(action)

@raises(InvalidUserActionError)
def test_validate_user_action_wrong_action_code_type():
    action = create_user_action_check_if_alerted()
    action['action']['code'] = 3
    GameState.validate_user_action(action)

@raises(InvalidUserActionError)
def test_validate_user_action_nonexistant_action():
    action = create_user_action('HELLO')
    GameState.validate_user_action(action)

def test_validate_user_action_check_if_alerted():
    action = create_user_action('CHECK_IF_ALERTED')
    GameState.validate_user_action(action)

def test_validate_user_action_button_press():
    action = create_user_action('BUTTON_PRESS')
    GameState.validate_user_action(action)

def test_create_user_button_press_response():
    user_id = gen_id()
    user_action = create_user_action('BUTTON_PRESS')
    success = True
    result = GameState.create_user_button_press_response(user_id, user_action, success)
    # Some cheeky by-reference comparisons
    nose.tools.ok_(result['user_id'] == user_id)
    nose.tools.ok_(result['user_action'] == user_action)
    nose.tools.ok_(result['response']['success'] == success)

def test_create_user_check_if_alerted_response():
    user_id = gen_id()
    user_action = create_user_action('BUTTON_PRESS')
    alerted = True
    result = GameState.create_user_check_if_alerted_response(user_id, user_action, alerted)
    # Some cheeky by-reference comparisons
    nose.tools.ok_(result['user_id'] == user_id)
    nose.tools.ok_(result['user_action'] == user_action)
    nose.tools.ok_(result['response']['alerted'] == alerted)
