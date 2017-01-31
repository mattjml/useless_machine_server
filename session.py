#!/usr/bin/env python3

from helpers import raise_not_implemented_error

class InvalidCredentialsError(Exception):
    """
    Exception class returned by Session instance when invalid credentials have
    been used in an attempt to create a session
    """
    pass

class InvalidSessionError(Exception):
    """
    Exception class returned by Session instance when invalid session details have
    been used in an attempt to extend a session
    """
    pass

class SessionManager:
    """
    Abstract implementation. Concrete implementations of this class are responsible for
    managing, authenticating and closing user sessions
    """

    def __init__(self, config):
        self.config = config
    
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
        InvalidCredentialsError
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
        InvalidSessionError
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
        InvalidSessionError
        """
        raise_not_implemented_error(self.destroy_session.__name__)
 
    def authenticate_session(self, session_details):
        """
        Authenticates session details

        Parameters
        ----------
        session_details : dict

        Raises
        ------
        InvalidSessionError
        """

