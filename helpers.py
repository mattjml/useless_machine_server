#!/usr/bin/env python3

def raise_not_implemented_error(func_name):
    """
    Raises
    ------
    NotImplementedError
        Raises NotImplementedError with a message string containing the function name
    """
    raise NotImplementedError('Please implement concrete version of {}'.format(func_name))
