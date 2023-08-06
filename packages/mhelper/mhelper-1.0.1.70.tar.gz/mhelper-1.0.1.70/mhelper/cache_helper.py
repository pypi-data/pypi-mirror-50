import types


class _CachingFunction:
    def __init__( self, name, function ):
        self.name = name
        self.function = function
    
    
    def __call__( self, self2, *args, **kwargs ):
        
        
        key = self.function, args, tuple( kwargs.items() )
        try:
            r = self2._Caching__cache.get( key, None )
        except AttributeError:
            self2._Caching__cache = {}
            r = None
            
        if r is None:
            r = self.function( self2, *args, **kwargs )
            self2._Caching__cache[key] = r
        return r
    
    
    def __get__( self, instance, cls ):
        if instance is None:
            return self
        
        return types.MethodType( self, instance )


class _CachedPlaceholder:
    def __init__( self, function ):
        self.function = function
    
    
    def __call__( self, *args, **kwargs ):
        raise ReferenceError( "This method is still being processed. Did you forget to decorate the class with `cache_enabled` before using the `cache` decorator?" )


class CacheEnabled:
    def __init__( self ):
        self._Caching__cache = { }
    
    
    def __init_subclass__( cls, **kwargs ):
        _replace_methods( cls )


def _replace_methods( cls ):
    for k, v in list( cls.__dict__.items() ):
        if isinstance( v, _CachedPlaceholder ):
            setattr( cls, k, _CachingFunction( k, v.function ) )


def cache_enabled( cls = None ):
    if cls:
        _replace_methods( cls )
        return cls
    else:
        return cache_enabled


def cached( fn = None ):
    if fn:
        return _CachedPlaceholder( fn )
    else:
        return cached
