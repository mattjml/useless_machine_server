import session

class MongoTicketSession(session.SessionManager):
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
        session ticket *without any authentication*. Raises session.InvalidCredentials
        if it does not. 

        Overrides SessionManager.new_session
        """
        raise_not_implemented_error(self.new_session.__name__)
    
    def extend_session(self, session):
        """
        Extends existing session. Goes to the configured mongodb and updates
        stored existing session with longer timestamp if it exists. Raises
        session.InvalidSession if it does not.

        Overrides SessionManager.extend_session
        """
        raise_not_implemented_error(self.extend_session.__name__)

