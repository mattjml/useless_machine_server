from datetime import datetime, timedelta
import uuid

import session

class StatefulTicketSession(session.SessionManager):
    """
    Session manager that creates unauthenticated session tickets and stores the state
    of these locally. 
    """
    def __init__(self, config):
        self.config = config
        self.sessions = {}

    @staticmethod
    def _extract_session_id_from_session_obj(session):
        id = None
        try:
            id = session['id']
            id = uuid.UUID(id)
        except (KeyError, TypeError) as error:
            raise session.InvalidSession('no id field in session object') from error
        except Value as error:
            raise session.InvalidSession('invalid id field in session object') from error
        return id
    
    def new_session(self, credentials):
        """
        Creates new session. Creates new session ticket in local dictionary 
        *without any authentication*.

        Overrides SessionManager.new_session
        """
        session_result = {
            'id': uuid.uuid4(),
            'expiry': (
                datetime.now()
                + timedelta(seconds=self.config['expiry_timeout_s'])
            )
        }
        self.sessions[session_result['id']] = session_result
        return session_result
    
    def extend_session(self, session_details):
        """
        Extends existing session. Checks local dictionary and updates
        stored existing session with longer expiry time if it exists. Raises
        session.InvalidSession if it does not or the session is invalid.

        Overrides SessionManager.extend_session
        """
        id = self.__class__._extract_session_id_from_session_obj(session_details) 
        print(id)
        print(type(id))
        print([key for key in self.sessions.keys()])
        print(self.sessions[id])

        try: 
            current_expiry = self.sessions[id]['expiry']
            now = datetime.now()
            if now > current_expiry:
                raise session.InvalidSession('Session has expired')
            self.sessions[id]['expiry'] = (
                datetime.now()
                + timedelta(seconds=self.config['expiry_sliding_window_s'])
            )
        except KeyError as error:
            raise session.InvalidSession('Unknown session') from error

        return self.sessions[id]
    
    def destroy_session(self, session_details):
        """
        Destroys existing session. Checks local dictionary and and updates
        stored existing session with in-the-past expiry time if it exists. Raises
        session.InvalidSession if it does not.

        Overrides SessionManager.extend_session
        """
        id = self.__class__._extract_session_id_from_session_obj(session_details) 

        try: 
            self.sessions[id]['expiry'] = (
                datetime.now()
            )
        except KeyError as error:
            raise session.InvalidSession('Unknown session') from error

