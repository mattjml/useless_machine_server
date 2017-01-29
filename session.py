class InvalidCredentials(Exception):
    """
    Exception class returned by Session instance when invalid credentials have
    been used in an attempt to create a session
    """
    pass

class InvalidSession(Exception):
    """
    Exception class returned by Session instance when invalid session details have
    been used in an attempt to extend a session
    """
    pass

def raise_not_implemented_error(func_name):
    """
    Raises
    ------
    NotImplementedError
        Raises NotImplementedError with a message string containing the function name
    """
    raise NotImplementedError('Please implement concrete version of {}'.format(func_name))

class SessionManager:
    """
    Abstract implementation. Concrete implementations of this class are responsible for
    managing, authenticating and closing user sessions
    """
    
    def new_session(self, credentials):
        """
        Creates new session

        Parameters
        ----------
        credentials : dict
        
        Returns
        -------
        dict
            Session details

        Raises
        ------
        InvalidCredentials
        """
        raise_not_implemented_error(self.new_session.__name__)
    
    def extend_session(self, session_details):
        """
        Extends existing session

        Parameters
        ----------
        session_details : dict
        
        Returns
        -------
        dict
            Session details

        Raises
        ------
        InvalidSession
        """
        raise_not_implemented_error(self.extend_session.__name__)

    def destroy_session(self, session_details):
        """
        Destroys existing session

        Parameters
        ----------
        session_details : dict

        Raises
        ------
        InvalidSession
        """
        raise_not_implemented_error(self.destroy_session.__name__)

