from flask import Flask, request
from flask_api import status
import pymongo

from session import SessionManager, InvalidSession

app = Flask(__name__)

def create_session():
    return "blah" 

def extend_session(request):
    session_details = request.get_json(force=True) 
    return "blah" 

@app.route('/session', methods=['GET', 'POST'])
def session():
    if request.method == 'POST':
        try:
            session = extend_session(request)
        except InvalidSession as exc:
            return {'failed to extend session': 'unauthorised'}, status.HTTP_401_UNAUTHORIZED
    else:
        session = create_session()
    return session

if __name__ == "__main__":
    app.run()
