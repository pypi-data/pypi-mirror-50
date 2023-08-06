"""
Contains an advanced display hook more suitable for interactive Python
than a simple `repr`.

When passed a raw function, this display hook includes the documentation,
arguments, and PEP-484 annotations.

When passed a type, the documentation and available methods are included.

When passed a list, tuple, or dict, the contents are of the iterable included,
one per line. 

When passed any object, the fields of the object are listed, if available,
alongside the object repr.
"""

import base64
import inspect
import sys
import warnings
from enum import EnumMeta

from mhelper import documentation_helper, mannotation, special_types, utf_table
from typing import Callable, Sequence


_RETURN_VALUE = special_types.Sentinel( "_RV" )


def _get_doc( x ):
    if isinstance( x, type ) or inspect.isroutine( x ) or inspect.ismodule( x ):
        return documentation_helper.Documentation( x.__doc__ ).get_element( "", "" )
    else:
        return None


def str_repr( v ):
    if inspect.isroutine( v ) or isinstance( v, type ) or inspect.ismodule( v ):
        if hasattr( v, "__qualname__" ) and v.__qualname__:
            return v.__qualname__
        elif hasattr( v, "__name__" ) and v.__name__:
            return v.__name__
    
    try:
        x = repr( v )
        
        if x.startswith( "<" ) and x.endswith( ">" ) and " object at " in x:
            return "{}({})".format( type( v ).__name__, base64.b85encode( id( v ).to_bytes( 8, "little" ) ).decode( "utf-8" ) )
        
        return x
    except Exception as ex:
        return "(cannot repr due to error: {}('{}'))".format( type( ex ).__name__, ex )


class _Root:
    """
    Root objects.
    """
    
    
    def __repr__( self ):
        return "."


_root = _Root


class ObjectViewer:
    """
    Acts as a function that provides information about python objects, similar
    to `help` and `dir` in one.
    
    :ivar exclude:      Types of objects never to display (e.g. `type(None)`).
    :ivar verbatim:     Types of objects use the default hook for (e.g. `str`).
    :ivar print:        Which function to use to print the displayed content
    :ivar box:          Drawing box to use (see `ansi.BoxChars`)
    :ivar last:         Holds a reference to the last displayed object. Because
                        the ObjectViewer does not display the full contents
                        of strings, this is used to retain temporary values
                        until they are displayed.
    """
    
    
    @staticmethod
    def PRINT_TO_STDERR( x ):
        print( x, file = sys.stderr )
    
    
    @staticmethod
    def PRINT_TO_PAGER( x ):
        import pydoc
        pydoc.pager( x )
    
    
    @staticmethod
    def REMOVE_PROXY( x ):
        from mhelper.proxy_helper import SimpleProxy
        
        if isinstance( x, SimpleProxy ):
            return SimpleProxy.get_source( x )
        
        return x
    
    
    def __init__( self,
                  exclude = (),
                  verbatim = (),
                  print: Callable[[str], None] = None,
                  box: utf_table.BoxChars = None,
                  remove_proxy: Callable[[object], object] = None ):
        self.print = print or self.PRINT_TO_STDERR
        self.exclude = exclude
        self.verbatim = verbatim
        self.box = box if box else utf_table.BoxChars.CURVED.pad()
        self.last = None
        self.remove_proxy = remove_proxy or self.REMOVE_PROXY
    
    
    def __repr__( self ):
        return "Call this function with an object to query its attributes."
    
    
    def hook( self ):
        """
        Sets this object as the system display hook.
        """
        sys.displayhook = self
    
    
    def __call__( self, obj: object = _root ) -> None:
        """
        This is the same as `display`, but honours the `exclude` and `verbatim`
        lists, unwraps proxies, and includes the results for `display` called
        on the `type` of the `obj`. 
        """
        if any( isinstance( obj, x ) for x in self.exclude ):
            return
        
        if any( isinstance( obj, x ) for x in self.verbatim ):
            sys.__displayhook__( obj )
            return
        
        r = []
        
        proxy_removed = self.remove_proxy( obj )
        
        if proxy_removed is not obj:
            obj = proxy_removed
            tbl = self.__mk_table()
            tbl.add_line()
            tbl.add( ["NOTE", "This object is wrapped in a proxy. It has been unwrapped to provide the documentation.", None] )
            tbl.add_line()
            r.append( tbl.to_string() )
        
        r.append( self.get_display_text( obj ) )
        
        obj = type( obj )
        
        if obj is not type:
            r.append( self.get_display_text( obj ) )
        
        self.print( "\n\n\n".join( r ) )
    
    
    def display( self, obj: object = _root ):
        """
        Displays an object, type, or routine.
        
        :param obj:     Target object
        :return:        Nothing is returned 
        """
        self.print( self.get_display_text( obj ) )
    
    
    def get_display_text( self, obj: object = _root ):
        self.last = obj
        tbl = self.__mk_table()
        
        # Title
        tbl.add_line()
        
        obj_title = str_repr( obj )
        ov = _AttrView( "", obj )
        
        tbl.add( [ov.type_desc, obj_title, None] )
        
        # Documentation
        obj_doc = _get_doc( obj )
        
        if obj_doc:
            tbl.add_line()
            tbl.add( ["DOCUMENTATION"] )
            tbl.add_line()
            tbl.add_wrapped( [obj_doc] )
        
        # Fields (attributes for classes or arguments for routines)
        attrs = sorted( _iter_attrs( obj ),
                        key = lambda x: "{} {}".format( x.priority, x.name ) )
        last_section = ""
        
        for vv in attrs:
            section = vv.category
            
            if section != last_section:
                tbl.add_line()
                tbl.add( ["{}".format( section )] )
                tbl.add_line()
                last_section = section
            
            tbl.add( [vv.type_desc, vv.name, vv.desc] )
        
        tbl.add_line()
        
        return tbl.to_string()
    
    
    def __mk_table( self ):
        box: utf_table.BoxChars = self.box
        tbl = utf_table.TextTable( [20, 25, 60], box = box )
        return tbl


def _iter_attrs( v ) -> Sequence["_AttrView"]:
    if v is _root:
        for x in dir():
            yield _AttrView( x, eval( x ) )
    
    elif inspect.isroutine( v ):
        fi = mannotation.FunctionInspector( v )
        for arg in fi.args:
            yield _AttrView( arg.name, arg )
        
        yield _AttrView( "(return)", mannotation.ArgInspector( "(return)", fi.return_type, _RETURN_VALUE, fi.return_description, True, -1 ) )
    
    for n in dir( v ):
        if not n.startswith( "_" ):
            try:
                a = getattr( v, n )
            except Exception as ex:
                a = ex
            yield _AttrView( n, a )
    
    if isinstance( v, dict ):
        try:
            for i, (n2, v2) in enumerate( v.items() ):
                yield _AttrView( "[{}]".format( repr( n2 ) ), v2 )
                
                if i > 1000:
                    yield _AttrView( "[...]".format( i ), "..." )
                    break
        
        except Exception:
            pass
        
        return
    
    if hasattr( v, "__iter__" ) and not isinstance( v, str ):
        try:
            for i, v2 in enumerate( v ):
                yield _AttrView( "[{}]".format( i ), v2 )
                
                if i > 1000:
                    yield _AttrView( "[...]".format( i ), "..." )
                    break
        
        except Exception:
            pass


class _AttrView:
    def __init__( self, name, value ):
        self.name = name
        self.value = value
        self.type = type( value )
        
        if isinstance( value, mannotation.ArgInspector ):
            self.priority, self.category = 0, "ARGUMENTS"
        elif inspect.ismemberdescriptor( value ):
            self.priority, self.category = 1, "MEMBERS"
        elif isinstance( value, property ):
            self.priority, self.category = 2, "PROPERTIES"
        elif inspect.ismodule( value ):
            self.priority, self.category = 3, "MODULES"
        elif isinstance( value, type ) and not isinstance( value, EnumMeta ) and not issubclass( value, BaseException ):
            if hasattr( value, "__name__" ) and value.__name__ != name:
                self.priority, self.category = 8, "DATA"
            else:
                self.priority, self.category = 4, "TYPES"
        elif isinstance( value, type ) and issubclass( value, BaseException ):
            self.priority, self.category = 5, "EXCEPTION TYPES"
        elif isinstance( value, EnumMeta ):
            self.priority, self.category = 6, "ENUMERATION TYPES"
        elif inspect.isroutine( value ):
            self.priority, self.category = 7, "FUNCTIONS"
        else:
            self.priority, self.category = 8, "DATA"
        
        if isinstance( value, mannotation.ArgInspector ):
            self.type_desc = str( value.annotation )
        else:
            self.type_desc = str( mannotation.AnnotationInspector( self.type ) )
        
        if value is None:
            self.desc = "-"
        elif inspect.isroutine( value ) or isinstance( value, type ) or inspect.ismodule( value ):
            if hasattr( value, "__name__" ) and value.__name__ != name:
                self.desc = value.__qualname__ if hasattr( value, "__qualname__" ) else value.__name__
            else:
                if value.__doc__:
                    for line in value.__doc__.strip().split( "\n" ):
                        line = line.strip()
                        if line and not line.startswith( "!" ):
                            self.desc = line
                            break
                    else:
                        self.desc = ""
                else:
                    self.desc = ""
        elif inspect.ismemberdescriptor( value ):
            self.desc = "{}.{}".format( value.__objclass__.__name__, value.__name__ )
        elif isinstance( value, mannotation.ArgInspector ):
            if value.default is _RETURN_VALUE:
                self.desc = value.description
            elif value.default is special_types.NOT_PROVIDED:
                self.desc = "(mandatory) {}".format( value.description )
            else:
                self.desc = "(default={}) {}".format( value.default, value.description )
        else:
            self.desc = str_repr( value )


def set_display_hook( *args, **kwargs ):
    """
    Sets the default display hook as `display`.
    """
    x = ObjectViewer( *args, **kwargs )
    x.hook()
    
    print( " * THE MHELPER.DEBUG_HELPER ASSISTANT HAS TAKEN CONTROL OF YOUR DISPLAY HOOK.\n"
           " * USE `sys.displayhook = sys.__displayhook__` TO DEACTIVATE IT.",
           file = sys.stderr )


view = ObjectViewer( print = ObjectViewer.PRINT_TO_PAGER )


def __display_triline( print, x ):
    print( "| " + x * 17 + " | " + x * 60 + " | " + x * 13 + " |" )


def dump_repr( obj, **kwargs ):
    """
    Designed for returning from an object's `__repr__`, this method returns
    a string like: "spam(eggs=1, beans=2)". Values are displayed using
    `str_repr`.
    
    :param obj:         The object who's class should be queried (or the name of the class). 
    :param kwargs:      The values to display. If not provided `obj`'s fields
                        will be enumerated.      
    :return:            The string representation. 
    """
    
    if not kwargs:
        vs = __iter_fields( obj )
    else:
        vs = kwargs.items()
    
    if not isinstance( obj, str ):
        obj = type( obj ).__name__
    
    return "{}({})".format( obj, ", ".join( "{}={}".format( k, str_repr( v ) ) for k, v in vs ) )


# noinspection PyDeprecation
def dump( _message = None, *args, **kwargs ):
    """
    !DEPRECATED
    
    Please don't use this method.
    """
    warnings.warn( "This method is deprecated and will be removed. Use `display` instead.", DeprecationWarning )
    r = []
    seen = set()
    
    if args or kwargs:
        if _message is not None:
            r.append( _message )
        
        r.append( "(dump)" )
        
        for i, v in enumerate( args ):
            __dump_object( "[{}]".format( i ), v, r, seen )
        
        for k, v in kwargs.items():
            __dump_object( k, v, r, seen )
    else:
        __dump_object( "(dump)", _message, r, seen )
    
    return "\n".join( r )


# noinspection PyDeprecation
def __dump_object( k, v, r, seen, i = 1 ):
    """
    !DEPRECATED
    
    Please don't use this method.
    """
    warnings.warn( "This method is deprecated and will be removed. Use `display` instead.", DeprecationWarning )
    ind = ("|   " * i)
    
    r.append( ind + "{} ({}) = {}".format( k, type( v ).__name__, str_repr( v ) ) )
    
    if any( isinstance( v, x ) for x in (int, float, bool, str) ):
        return
    
    id_ = id( v )
    
    if id_ in seen:
        r.append( ind + "    - repeat" )
        return
    
    seen.add( id_ )
    
    if i > 10:
        r.append( ind + "    ..." )
        return
    
    for k2, v2 in __iter_fields( v ):
        __dump_object( k2, v2, r, seen, i + 1 )


def __iter_fields( obj ):
    if hasattr( obj, "__dict__" ):
        for k, v in obj.__dict__.items():
            if not k.startswith( "_" ):
                yield k, v
    
    from mhelper import reflection_helper
    for cls in reflection_helper.iter_hierarchy( type( obj ) ):
        if hasattr( cls, "__slots__" ):
            for slot in cls.__slots__:
                try:
                    yield slot, getattr( obj, slot )
                except Exception:
                    pass
    
    if isinstance( obj, dict ):
        try:
            for i, (n2, v2) in enumerate( obj.items() ):
                yield "[{}]".format( repr( n2 ) ), v2
                
                if i > 1000:
                    yield "[...]".format( i ), "..."
                    break
        
        except Exception:
            pass
        
        return
    
    if hasattr( obj, "__iter__" ) and not isinstance( obj, str ):
        try:
            for i, v2 in enumerate( obj ):
                yield "[{}]".format( i ), v2
                
                if i > 1000:
                    yield "[...]".format( i ), "..."
                    break
        
        except Exception:
            pass


# noinspection PyDeprecation
