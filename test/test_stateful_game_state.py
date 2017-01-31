#!/usr/bin/env python3

import nose
import os
import uuid
import sys

# Allow relative imports of the parent modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
import stateful_game_state

def setup_func():
    print('set up test fixtures')

def teardown_func():
    print('tear down test fixtures')

@nose.with_setup(setup_func, teardown_func)
def test_add_user():
    gs = stateful_game_state.StatefulGameState({})
    gs.add_user(uuid.uuid4())
    print(gs.state)
