from flask import Flask, jsonify, request
from flask_api import status
import pymongo

from session import InvalidSession, InvalidCredentials

app = Flask(__name__)

# TODO dependency injection
config = {
    'expiry_timeout_s': 100,
    'expiry_sliding_window_s': 20
}
from stateful_ticket_session import StatefulTicketSession as SessionManager
session_manager = SessionManager(config)


def create_json_error_response(body, code):
    """
    Returns flask error response
    
    Parameters
    ----------
    body : object
       Must be jsonify'able
    code : int
       HTTP status error code
    """
    return jsonify(body), code

@app.route('/login', methods=['POST'])
def login():
    result = None
    try:
        credentials = request.get_json(force=True) 
        result = session_manager.new_session(credentials)
    except InvalidCredentials as exc:
        return create_json_error_response(
            {'failed to login': 'unauthorised'},
            status.HTTP_401_UNAUTHORIZED
        )
    return jsonify(result)

@app.route('/session', methods=['POST'])
def session():
    result = None
    try:
        session_details = request.get_json(force=True) 
        result = session_manager.extend_session(session_details)
    except InvalidSession as exc:
        return create_json_error_response(
            {'failed to extend session': 'unauthorised'},
            status.HTTP_401_UNAUTHORIZED
        )
    return jsonify(result)

@app.route('/signout', methods=['POST'])
def signout():
    result = None
    try:
        session_details = request.get_json(force=True) 
        result = session_manager.destroy_session(session_details)
    except InvalidSession as exc:
        return create_json_error_response(
            {'failed to destroy session': 'unauthorised'},
            status.HTTP_401_UNAUTHORIZED
        )
    return '', status.HTTP_200_OK

if __name__ == "__main__":
    app.run()

