#!/usr/bin/env python3

import nose
from nose.tools import raises
import os
import uuid
import sys

# Allow relative imports of the parent modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
import game_state
import stateful_game_state

def create_gs(config):
    return stateful_game_state.StatefulGameState({})

def test_add_user():
    create_gs({}).add_user(uuid.uuid4())

def test_remove_user():
    gs = create_gs({})
    id = uuid.uuid4()
    gs.add_user(id)
    gs.remove_user(id)

@raises(game_state.UserDoesntExistError)
def test_remove_user_when_no_users():
    create_gs({}).remove_user(uuid.uuid4())

@raises(game_state.UserDoesntExistError)
def test_remove_user_twice():
    gs = create_gs({})
    id = uuid.uuid4()
    gs.add_user(id)
    gs.remove_user(id)
    gs.remove_user(id)

@raises(game_state.UserAlreadyExistsError)
def test_add_user_twice():
    gs = create_gs({})
    id = uuid.uuid4()
    gs.add_user(id)
    gs.add_user(id)

def test_double_add_remove_user():
    gs = create_gs({})
    id = uuid.uuid4()
    gs.add_user(id)
    gs.remove_user(id)
    gs.add_user(id)
    gs.remove_user(id)

def test_add_user_string_uuid():
    gs = create_gs({})
    gs.add_user(str(uuid.uuid4()))

def test_remove_user_string_uuid():
    gs = create_gs({})
    id = uuid.uuid4()
    gs.add_user(id)
    gs.remove_user(str(id))

@raises(game_state.UserDoesntExistError)
def test_remove_nonexistant_user():
    gs = create_gs({})
    gs.add_user(uuid.uuid4())
    gs.remove_user(uuid.uuid4())

@raises(game_state.UserDoesntExistError)
def test_cleanup():
    gs = create_gs({})
    id = uuid.uuid4()
    gs.add_user(id)
    gs.clean_up()
    gs.remove_user(id)

def test_find_state():
    gs = create_gs({})
    ids = [uuid.uuid4(), uuid.uuid4()]
    gs.add_user(ids[0])
    gs.add_user(ids[1])
    nose.tools.ok_(gs.find_state(ids[1])['user_id'] == ids[1])
    nose.tools.ok_(gs.find_state(ids[1])['user_id'] == ids[1])
    nose.tools.ok_(gs.find_state(ids[0])['user_id'] == ids[0])

@raises(game_state.UserDoesntExistError)
def test_find_state_no_match():
    gs = create_gs({})
    id = uuid.uuid4()
    gs.add_user(id)
    nose.tools.ok_(gs.find_state(uuid.uuid4()))

@raises(game_state.UserDoesntExistError)
def test_find_state_no_states():
    gs = create_gs({})
    nose.tools.ok_(gs.find_state(uuid.uuid4()))
