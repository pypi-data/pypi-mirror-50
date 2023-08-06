"""
This package contains decorators that can be used to annotate the purpose of a method.

mh_package_status = SUSPENDED
mh_status_reason  = I now use PyDoc comments for the same purpose
"""
from inspect import isclass
from typing import TypeVar


_T = TypeVar( "_T" )


def identity( x ):
    """
    Returns its parameter
    """
    return x


def ignore( *_, **__ ):
    """
    Ignores its parameters
    """
    pass


def protected( f ):
    return f


def sealed( f ):
    return f


def override( f ):  # means "I'm not documenting this because the documentation is in the base class"
    return f


def overrides( interface ):
    ignore( interface )
    return override


def virtual( f ):
    return f


def abstract( f ):
    if isclass( f ):
        return f
    
    
    def fn( self, *_, **__ ):
        raise NotImplementedError( "An attempt has been made to call an abstract method «{1}.{0}». The object's string representation is «{2}».".format( f.__name__, type( self ).__name__, repr( self ) ) )
    
    
    return fn


