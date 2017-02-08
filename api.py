#!/usr/bin/env python3

import threading

from flask import Flask, jsonify, request
from flask_api import status

from game_state import UserDoesntExistError, UserAlreadyExistsError, InvalidUserActionError
from session import InvalidSessionError, InvalidCredentialsError

app = Flask(__name__)

# TODO session in cookies so GET can be used

# TODO dependency injection
session_config = {
    'expiry_timeout_s': 100,
    'expiry_sliding_window_s': 60
}
from stateful_ticket_session import StatefulTicketSessionManager as SessionManager
session_manager = SessionManager(session_config)
game_config = {'alert_chance_of_multiply':0.2}
from stateful_game_state import StatefulGameState as GameState
game_state = GameState(game_config)


def create_json_error_response(msg, code):
    """
    Returns flask error response body and code pair

    :param string msg: error message

    :param int code: HTTP Status Code

    :return (json, int): json message and status code
    """
    return jsonify({'msg': msg}), code


def parse_json(req):
    return req.get_json(force=True)


def check_expired_sessions():
    expired_sessions = session_manager.check_expired_sessions()
    for id in expired_sessions.keys():
        game_state.remove_user(id)

@app.route('/login', methods=['POST'])
def login():
    check_expired_sessions()
    result = None
    try:
        credentials = parse_json(request)
        result = session_manager.new_session(credentials)
        game_state.add_user(result['id'])
    except InvalidCredentialsError as exc:
        return create_json_error_response('failed to login', status.HTTP_401_UNAUTHORIZED)
    return jsonify(result)

@app.route('/session', methods=['POST'])
def session():
    check_expired_sessions()
    result = None
    try:
        session_details = parse_json(request)
        result = session_manager.extend_session(session_details)
    except InvalidSessionError as exc:
        return create_json_error_response('failed to extend session', status.HTTP_401_UNAUTHORIZED)
    return jsonify(result)

@app.route('/signout', methods=['POST'])
def signout():
    check_expired_sessions()
    try:
        session_details = parse_json(request)
        session_manager.destroy_session(session_details)
        game_state.remove_user(session_details['id'])
    except InvalidSessionError as exc:
        return create_json_error_response('failed to destroy session', status.HTTP_401_UNAUTHORIZED)
    except UserDoesntExistError:
        return create_json_error_response('unknown error', status.HTTP_500_INTERNAL_SERVER_ERROR)
    return '', status.HTTP_200_OK

@app.route('/action', methods=['POST'])
def action():
    check_expired_sessions()
    result = None
    try:
        req = parse_json(request)
        session_manager.authenticate_session(req['session'])
        req['session'] = session_manager.extend_session(req['session'])
        result = game_state.user_action(req['session']['id'], req['user_action'])
    except InvalidSessionError:
        return create_json_error_response('cant take user action', status.HTTP_401_UNAUTHORIZED)
    except InvalidUserActionError as error:
        return create_json_error_response(
            'invalid user action ' + error.msg,
            status.HTTP_400_BAD_REQUEST
        )
    except KeyError:
        return create_json_error_response('invalid request', status.HTTP_400_BAD_REQUEST)
    except UserDoesntExistError:
        return create_json_error_response('unknown error', status.HTTP_500_INTERNAL_SERVER_ERROR)
    return jsonify(result)

if __name__ == "__main__":
    app.run()

