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

def validate_check_if_alerted_response(id, response, action, expected_alert_state):
    nose.tools.ok_(response['user_id'] == id)
    nose.tools.ok_(response['user_action']['code'] == action['code'])
    nose.tools.ok_(len(response['response'].keys()) == 1)
    nose.tools.ok_(response['response']['alerted'] == expected_alert_state)

#### Tests ####
@raises(game_state.UserDoesntExistError)
def test_user_action_nonexistant_user():
    gs, id = create_gs_and_add_user({})
    gs.user_action(gen_id(), {'code': 'CHECK_IF_ALERTED'})

@raises(game_state.InvalidUserActionError)
def test_user_action_nonexistant_action():
    gs, id = create_gs_and_add_user({})
    gs.user_action(id, {'code': 'CHECK_IF_ALERTIFIED'})

def test_user_action_check_if_new_user_alerted():
    gs, id = create_gs_and_add_user({})
    action = {'code': 'CHECK_IF_ALERTED'}

    # Newly instantiated users shouldn't have alerts
    res = gs.user_action(id, action)
    validate_check_if_alerted_response(id, res, action, False)

def test_user_action_check_user_is_alerted():
    gs, id = create_gs_and_add_user({})
    other_id = add_user(gs)
    action = {'code': 'CHECK_IF_ALERTED'}

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
        gs.user_action(id, {'code': 'BUTTON_PRESS'})
        nose.tools.ok_(gs.find_state(id)['alert_state'] is False)

    # TODO this is a bad way to test this
    # TODO probablistically we should never see this fail as after
    # 1000 iterations, each setting each user's alert_state
    # to (alert_state OR random_boolean), each user's alert_state
    # should be True
    # Likelihood of False is 1/2^1000 per user
    for other_id in other_ids:
        nose.tools.ok_(gs.find_state(other_id)['alert_state'] is True)
