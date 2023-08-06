"""
Provides an interprocess mutex.

Uses the `posix_ipc.Semaphore`. 
"""
import posix_ipc
import time
import warnings


TIMEOUT_FALLBACK_WARNING = True


class IpcMutex:
    def __init__( self, name ):
        self.name = name
        self.full_name = "Mutex.{}".format( name )
        self.semaphore = posix_ipc.Semaphore( self.full_name, flags = posix_ipc.O_CREAT, initial_value = 1 )
    
    
    def acquire( self, timeout = None ) -> bool:
        """
        Acquires the semaphore.
        
        .. warning::
        
            Due to a known bug with the OS (see posix_ipc) the timeout on MacOS does not work. 
        
        :return:    `True` if acquired, else `False`. 
        """
        if timeout and not posix_ipc.SEMAPHORE_TIMEOUT_SUPPORTED:
            self.__poll( timeout )
        
        try:
            self.semaphore.acquire( timeout )
            return True
        except posix_ipc.BusyError:
            return False
    
    
    def __poll( self, timeout ) -> bool:
        """
        Polls up to the timeout.
        This is a hack for MacOS.
        
        Pollse every:
              0.001s for the first 0.01s
              0.01s  ''            0.1s
              0.1s   ''            1s
              1s     ''            10s
              10s    ''            100s
              etc.
        """
        global TIMEOUT_FALLBACK_WARNING
        
        if TIMEOUT_FALLBACK_WARNING:
            warnings.warn( "Your platform does not support semaphore timeout. "
                           "I am going to poll instead. "
                           "Performance may be compromised if this semaphore is used frequently. "
                           "See `posix_ipc` documentation and comments in `{}`.".format( IpcMutex.__poll.__qualname__ ), UserWarning )
            TIMEOUT_FALLBACK_WARNING = False
        
        start = time.perf_counter()
        period = 0.01
        period2 = period / 10
        
        while True:
            if self.acquire( 0 ):
                return True
            
            elapsed = time.perf_counter() - start
            
            if elapsed > timeout:
                return False
            
            if elapsed > period:
                period *= 10
                period2 *= 10
            
            time.sleep( period2 )
    
    
    def release( self ):
        return self.semaphore.release()
    
    
    def __enter__( self ):
        self.acquire()
    
    
    def __exit__( self, exc_type, exc_val, exc_tb ):
        self.release()
