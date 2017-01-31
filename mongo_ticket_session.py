#!/usr/bin/env python3

import session

class MongoTicketSessionManager(session.SessionManager):
    """
    SessionManager that creates unauthenticated session tickets and stores the state
    of these in a mongodb instance. 
    """
    def __init__(self, config):
        #TODO validate mongo config
        self.config = config
    
    def new_session(self, credentials):
        """
        Creates new session. Goes to the configured mongodb and creates new
        session ticket *without any authentication*.

        Overrides SessionManager.new_session
        """
        from session import raise_not_implemented_error
        raise_not_implemented_error(self.new_session.__name__)
    
    def extend_session(self, session_details):
        """
        Extends existing session. Goes to the configured mongodb and updates
        stored existing session with longer expiry time if it exists. Raises
        session.InvalidSessionError if it does not.

        Overrides SessionManager.extend_session
        """
        from session import raise_not_implemented_error
        raise_not_implemented_error(self.extend_session.__name__)

    def destroy_session(self, session_details):
        """
        Destroys existing session. Goes to the configured mongodb and updates
        stored existing session with in-the-past expiry time if it exists. Raises
        session.InvalidSessionError if it does not.

        Overrides SessionManager.extend_session
        """
        from session import raise_not_implemented_error
        raise_not_implemented_error(self.destroy_session.__name__)
 
    def authenticate_session(self, session_details):
        """
        Authenticates existing session. Goes to the configured mongodb and checks
        if stored existing session exists and is within expiry time. Raises
        session.InvalidSessionError if it isn't.

        Overrides SessionManager.authenticate_session
        """
        from session import raise_not_implemented_error
        raise_not_implemented_error(self.authenticate_session.__name__)

