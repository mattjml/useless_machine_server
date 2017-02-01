#!/usr/bin/env python3

import nose
from nose.tools import raises
import os
import sys

from .helper import gen_id

# Allow relative imports of the parent modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
import game_state
import stateful_game_state


#### Helper functions ####
def create_gs(config):
    return stateful_game_state.StatefulGameState({})

def add_user(gs):
    id = gen_id()
    gs.add_user(id)
    return id

def create_gs_and_add_user(config):
    gs = create_gs({})
    id = add_user(gs)
    return gs, id

def create_user_action(code):
    return {
        'api': {
            'name': 'stateful',
            'version': 1
        },
        'action': code
    }

def create_gs_user_and_action(config):
    gs, id = create_gs_and_add_user({})
    return gs, id, create_user_action({'code': 'CHECK_IF_ALERTED'})

def validate_check_if_alerted_response(id, response, action, expected_alert_state):
    nose.tools.ok_(response['user_id'] == id)
    # Cheeky by-reference comparison
    nose.tools.ok_(response['user_action']['action'] == action['action'])
    nose.tools.ok_(len(response['response'].keys()) == 1)
    nose.tools.ok_(response['response']['alerted'] == expected_alert_state)


#### Tests ####
@raises(game_state.UserDoesntExistError)
def test_user_action_nonexistant_user():
    gs, id = create_gs_and_add_user({})
    gs.user_action(gen_id(), create_user_action({'code': 'CHECK_IF_ALERTED'}))

@raises(game_state.InvalidUserActionError)
def test_user_action_nonexistant_action():
    gs, id = create_gs_and_add_user({})
    gs.user_action(id, create_user_action({'code': 'CHECK_IF_ALERTIFIED'}))

@raises(game_state.InvalidUserActionError)
def test_user_action_no_api_detais():
    gs, id, action = create_gs_user_and_action({})
    del action['api']
    gs.user_action(id, action)

@raises(game_state.InvalidUserActionError)
def test_user_action_wrong_api_name():
    gs, id, action = create_gs_user_and_action({})
    action['api']['name'] = 'giraffe'
    gs.user_action(id, action)

@raises(game_state.InvalidUserActionError)
def test_user_action_no_api_name():
    gs, id, action = create_gs_user_and_action({})
    del action['api']['name']
    gs.user_action(id, action)

@raises(game_state.InvalidUserActionError)
def test_user_action_wrong_api_version():
    gs, id, action = create_gs_user_and_action({})
    action['api']['version'] = 2
    gs.user_action(id, action)

@raises(game_state.InvalidUserActionError)
def test_user_action_no_api_version():
    gs, id, action = create_gs_user_and_action({})
    del action['api']['version']
    gs.user_action(id, action)

@raises(game_state.InvalidUserActionError)
def test_user_action_no_action_details():
    gs, id, action = create_gs_user_and_action({})
    del action['action']
    gs.user_action(id, action)

@raises(game_state.InvalidUserActionError)
def test_user_action_no_action_code():
    gs, id, action = create_gs_user_and_action({})
    del action['action']['code']
    gs.user_action(id, action)

def test_user_action_check_if_new_user_alerted():
    gs, id, action = create_gs_user_and_action({})

    # Newly instantiated users shouldn't have alerts
    res = gs.user_action(id, action)
    validate_check_if_alerted_response(id, res, action, False)

def test_user_action_check_user_is_alerted():
    gs, id = create_gs_and_add_user({})
    other_id = add_user(gs)
    action = create_user_action({'code': 'CHECK_IF_ALERTED'})

    # Insert an alert
    gs.find_state(other_id)['alert_state'] = True
    # Check for alert
    res = gs.user_action(other_id, action)
    validate_check_if_alerted_response(other_id, res, action, True)
    # Check for alert again
    res = gs.user_action(other_id, action)
    validate_check_if_alerted_response(other_id, res, action, True)

    # Check first user doesn't also receive an alert
    res = gs.user_action(id, action)
    validate_check_if_alerted_response(id, res, action, False)

def test_user_action_button_press():
    gs, id = create_gs_and_add_user({})
    other_ids = [add_user(gs) for i in range(10)]
    # On BUTTON_PRESS, our user's state should be marked with
    # an alert_state=False whilst each other user should
    # have their alert_state updated to (alert_state OR random_boolean)
    # TODO mock out random such that we don't have to do
    # TODO ... this crazy loop
    for i in range(1000):
        gs.user_action(id, create_user_action({'code': 'BUTTON_PRESS'}))
        nose.tools.ok_(gs.find_state(id)['alert_state'] is False)

    # TODO this is a bad way to test this
    # TODO probablistically we should never see this fail as after
    # 1000 iterations, each setting each user's alert_state
    # to (alert_state OR random_boolean), each user's alert_state
    # should be True
    # Likelihood of False is 1/2^1000 per user
    for other_id in other_ids:
        nose.tools.ok_(gs.find_state(other_id)['alert_state'] is True)
