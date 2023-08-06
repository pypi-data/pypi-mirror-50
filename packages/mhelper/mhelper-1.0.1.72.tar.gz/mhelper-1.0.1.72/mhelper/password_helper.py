"""
Fixes issues with the `keyring` library on Ubuntu - see the `get_keyring`
function.

Contains a `ManagedPassword` class, which wraps the `keyring` module.
"""

def get_keyring():
    """
    Python's `keyring` module is problematic (notably on Ubuntu) in that falls
    back to an error-producing backend if we couldn't start a normal backend.
    
    This means it hides the reason the normal backend didn't start, confusingly
    telling us we have no backends available instead. It also means that even if
    we do get the normal backend working, it's too late and the fallback is
    already in place.
    
    This function:
        * sets up the usual backend on Ubuntu *before* we import `keyring`.
        * translates the errors, producing only `RuntimeError` on failure.
        * tests that passwords can actually be retrieved
        
    The `keyring` package is returned on success.
    """
    
    # Ubuntu's secret-storage needs DBUS, which in turn needs an event loop.
    # There is usually one already, but for some reason in Flask there isn't,
    # so we create one.
    import asyncio
    
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop( loop )
    
    try:
        import keyring
    except ImportError as ex:
        raise RuntimeError( "The python 'keyring' package is not installed." ) from ex
    
    # Detect errors early - try to get a password now
    try:
        keyring.get_password( "test", "test" )
    except RuntimeError as ex:
        raise RuntimeError( "The python 'keyring' is not working properly." ) from ex
    
    return keyring


class ManagedPassword:
    DEFAULT_KEYRING = "python_mhelper"
    
    
    def __init__( self, password, *, key = None, keyring = None, managed = True ):
        if not key:
            import uuid
            key = str( uuid.uuid4() )
        
        self.__key = key
        self.__keyring = keyring
        self.__password = password
        self.__managed = managed
        
        if self.__password and self.__managed:
            keyring = get_keyring()
            keyring.set_password( self.keyring, self.key, self.__password )
    
    
    @property
    def key( self ):
        return self.__key
    
    
    @property
    def keyring( self ):
        return self.__keyring or self.DEFAULT_KEYRING
    
    
    @property
    def password( self ):
        if self.__password is None:
            if self.__managed:
                keyring = get_keyring()
                self.__password = keyring.get_password( self.keyring, self.key )
            else:
                raise ValueError( "Logic error, unmanaged password but no password is specified." )
        
        return self.__password
    
    
    def delete( self ):
        if not self.__key:
            raise ValueError( "Logic error, attempt to delete a password that is already deleted." )
        
        if self.__managed:
            keyring = get_keyring()
            keyring.delete_password( self.keyring, self.key )
        
        self.__key = None
        self.__keyring = None
        self.__password = None
        self.__managed = False
    
    
    def __setstate__( self, state ):
        self.__key = state["key"]
        self.__keyring = state["keyring"]
        self.__password = state["password"]
        self.__managed = state["managed"]
    
    
    def __getstate__( self ):
        return { "key"     : self.__key,
                 "keyring" : self.__keyring,
                 "managed" : self.__managed,
                 "password": self.password if not self.__managed else None }
    
    
    def __repr__( self ):
        return "{}(key={},keyring={})".format( type( self ).__name__, repr( self.__key ), repr( self.__keyring ) )
    
    
    def __str__( self ):
        return "********"
