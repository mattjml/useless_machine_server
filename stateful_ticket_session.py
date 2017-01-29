import session

class StatefulTicketSession(session.Session):
    """
    Session manager that creates unauthenticated session tickets and stores the state
    of these locally. 
    """
    def __init__(self, config):
        self.config = config
    
    def new_session(self, credentials):
        """
        Creates new session. Goes to the configured mongodb and creates new
        session ticket *without any authentication*. Raises session.InvalidCredentials
        if it does not. 

        Overrides session.new_session
        """
        raise_not_implemented_error(self.new_session.__name__)
    
    def extend_session(self, session):
        """
        Extends existing session. Goes to the configured mongodb and updates
        stored existing session with longer timestamp if it exists. Raises
        session.InvalidSession if it does not.

        Overrides session.extend_session
        """
        raise_not_implemented_error(self.extend_session.__name__)

