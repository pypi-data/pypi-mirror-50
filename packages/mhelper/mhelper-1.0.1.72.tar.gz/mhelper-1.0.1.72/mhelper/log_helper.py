"""
Logging helpers.

Includes:

* A logging handler that formats for the terminal, including thread and process information.
* A logger which highlights variadic values, contains helpers for dealing with progress bars, iteration, enumeration and timing.
* A function to iterate information on existing loggers.
"""
import logging
import os
import sys
import time
import warnings
import threading
from collections import namedtuple
from typing import Union, Iterable, TypeVar, Iterator, List
from mhelper import ansi, string_helper, progress_helper, disposal_helper


T = TypeVar( "T" )

_TIME = string_helper.timedelta_to_string
_FLOAT = lambda x: "{0:.2f}".format( x )
_PERCENT = lambda x: "{0:.0f}".format( x * 100 )
_INT = lambda x: "{:,}".format( x )


class Handler( logging.Handler ):
    """
    A logging handler that formats for the terminal and displays thread and
    process information.
    """
    
    target = sys.__stderr__.write
    show_name = True
    show_processes = True
    show_threads = True
    
    __FG_COLOURS = [ansi.FR,
                    ansi.FG,
                    ansi.FB,
                    ansi.FC,
                    ansi.FY,
                    ansi.FM,
                    ansi.FW,
                    ansi.FK,
                    ansi.FBR,
                    ansi.FBG,
                    ansi.FBB,
                    ansi.FBC,
                    ansi.FBY,
                    ansi.FBM,
                    ansi.FBW,
                    ansi.FBK]
    __BG_COLOURS = [ansi.BR,
                    ansi.BG,
                    ansi.BB,
                    ansi.BC,
                    ansi.BY,
                    ansi.BM,
                    ansi.BW,
                    ansi.BK,
                    ansi.BBR,
                    ansi.BBG,
                    ansi.BBB,
                    ansi.BBC,
                    ansi.BBY,
                    ansi.BBM,
                    ansi.BBW,
                    ansi.BBK]
    
    
    def __repr__( self ):
        return "{}('{}')".format( "log_helper.Handler", self.name )
    
    
    def __str__( self ):
        return self.name
    
    
    def __init__( self,
                  name,
                  *,
                  show_processes = None,
                  target = None,
                  show_threads = None,
                  show_name = None,
                  minimal = False ):
        """
        :param name:                Name of the log
        :param show_processes:      Show the process sidebar.
                                    Overrides the Handler cvar if provided. 
        :param target:              Where to send the output.
                                    Overrides the Handler cvar if provided.
        :param show_threads:        Show the thread sidebar.
                                    Overrides the Handler cvar if provided. 
        :param show_name:           Show the name sidebar.
                                    Overrides the Handler cvar if provided.
        :param minimal:             When `True`, overrides the Handler cvars `show_processes`, `show_threads` and `show_name`.
        """
        super().__init__()
        
        if isinstance( name, Logger ):
            self.logger = name
            name = name.name
        else:
            self.logger = None
        
        self.name = name
        
        if "." in name:
            name = ".".join( name.rsplit( ".", 2 )[-2:] )
        
        if minimal:
            self.show_processes = False
            self.show_threads = False
            self.show_name = False
        
        if show_name is not None:
            self.show_name = show_name
        
        if show_processes is not None:
            self.show_processes = show_processes
        
        if target is not None:
            self.target = target
        
        if show_threads is not None:
            self.show_threads = show_threads
        
        c1 = hash( name ) % len( self.__FG_COLOURS )
        c2 = hash( name * 2 ) % len( self.__BG_COLOURS )
        
        if c2 == c1:
            c2 = (c1 + 1) % len( self.__FG_COLOURS )
        
        sigil_1 = self.__FG_COLOURS[c1]
        sigil_2 = self.__BG_COLOURS[c2]
        self.sigil_n = sigil_1 + sigil_2 + " {} ".format( string_helper.fix_width( name, 15 ) ) + ansi.RESET + " " + ansi.FORE_CYAN + " "
        self.sigil_0 = sigil_1 + sigil_2 + " {} ".format( string_helper.fix_width( "''", 15 ) ) + ansi.RESET + " " + ansi.FORE_CYAN + " "
    
    
    def emit( self, x: logging.LogRecord ):
        if self.show_name:
            sigil_n = self.sigil_n
            sigil_0 = self.sigil_0
        else:
            sigil_n = ""
            sigil_0 = ""
        
        fw = string_helper.fix_width
        text = x.getMessage()
        text = string_helper.highlight_quotes( text, "«", "»", ansi.FORE_YELLOW, ansi.FORE_GREEN )
        tname = threading.current_thread().name
        
        #
        # Thread
        #
        if not self.show_threads:
            thread = ""
        elif tname == "MainThread":
            thread = ""
        elif tname.startswith( "Thread-" ) and tname[7:].isdigit():
            thread = ansi.BACK_BLUE + ansi.FORE_WHITE + " {} ".format( fw( tname[7:].strip(), 3 ) ) + ansi.RESET
        else:
            thread = ansi.BACK_BLUE + ansi.FORE_WHITE + " {} ".format( fw( tname, 15 ) ) + ansi.RESET
        
        #
        # Process
        #
        pid = os.getpid()
        
        if self.show_processes:
            process = ansi.BACK_BLUE + ansi.FORE_BRIGHT_BLUE + " {} ".format( fw( str( pid ), 8 ) ) + ansi.RESET
        else:
            process = ""
        
        sigil = sigil_n
        
        text = text.split( "\n" )
        
        for tex in text:
            tex = ansi.FORE_GREEN + "{}{}{}{}\n".format( process, thread, sigil, tex ) + ansi.FORE_RESET
            self.target( tex )
            
            sigil = sigil_0
            process = process and ansi.BACK_BLUE + ansi.FORE_BRIGHT_BLUE + " {} ".format( fw( "''", 8 ) ) + ansi.RESET
            thread = thread and ansi.BACK_BLUE + ansi.FORE_WHITE + " {} ".format( fw( "'' ", 3 ) ) + ansi.RESET


class RootLogHandler( logging.Handler ):
    __slots__ = ["handlers"]
    
    
    def __init__( self ):
        super().__init__()
        
        self.handlers = { }
    
    
    def emit( self, record: logging.LogRecord ):
        s = self.handlers.get( record.name )
        
        if not s:
            s = Handler( record.name )
            self.handlers[record.name] = s
        
        return s.emit( record )


class Logger:
    """
    Logging simplified.
    
    This just wraps logging.Logger and provides an ANSI-terminal handler (`Handler`) by
    default. All messages are logged at the same level. The target terminal can be changed via
    `Logger.Handler.target`. The provided handler can be changed or removed by setting
    `Logger.handler`.
    
    Usage::
    
        log = Logger( "my logger", True )
        log( "hello {}", x )
    """
    __INDENT_SIZE = 4
    Handler = Handler
    __slots__ = "__level", "__true_logger", "__indent", "__handler", "__true_logger", "comment"
    
    
    def __init__( self,
                  name: str,
                  enabled: Union[bool, str] = False,
                  comment: str = "",
                  handler: Union[None, bool, dict, logging.Handler] = None ):
        """
        
        :param name:        Default value to :property:`name`. 
        :param enabled:     Default value to :property:`enabled`. 
        :param comment:     A description of the logger, for reference only.
        :param handler:     Keyword arguments passed to the `Handler` (as a `dict`) or a logging handler to set, or `False`. 
        """
        assert name
        self.__level = logging.INFO
        self.__true_logger = logging.getLogger( name )
        self.__indent = 0
        
        if handler is None:
            for handler_ in self.__true_logger.handlers:
                if isinstance( handler_, Handler ):
                    self.__handler = handler_
                    break
            else:
                self.__handler = Handler( self )
        elif handler is False:
            self.__handler = None
        elif isinstance( handler, dict ):
            self.__handler = Handler( self, **handler )
        elif isinstance( handler, logging.Handler ):
            self.__handler = handler
        else:
            raise ValueError( "Invalid value for `handler`: {}".format( handler ) )
        
        self.__true_logger.addHandler( self.__handler )
        self.comment = comment
        
        # Set the enabled property
        self.enabled = enabled
    
    
    @property
    def handler( self ) -> object:
        """
        Gets or sets the `handler`, this is attached to the underlying logger.
        
        To maintain synchronisation between the underlying logger and this
        class, handlers attached using this property should be removed
        through this property, and not by calling `removeHandler` directly.  
        """
        return self.__handler
    
    
    @handler.setter
    def handler( self, value: logging.Handler ) -> None:
        if self.__handler is not None:
            self.__true_logger.removeHandler( self.__handler )
        
        if value is not None:
            self.__true_logger.addHandler( value )
    
    
    @property
    def name( self ) -> str:
        return self.__true_logger.name
    
    
    def __bool__( self ) -> bool:
        return self.enabled
    
    
    def pause( self, *_, **__ ) -> None:
        warnings.warn( "Deprecated. No longer functional.", DeprecationWarning )
    
    
    @property
    def enabled( self ) -> bool:
        """
        Gets or sets whether the underlying logger is enabled.
        """
        return self.__true_logger.isEnabledFor( self.__level )
    
    
    @enabled.setter
    def enabled( self, value: bool ) -> None:
        """
        Setter.
        """
        if value:
            self.__true_logger.setLevel( logging.DEBUG )
        else:
            self.__true_logger.setLevel( logging.NOTSET )
    
    
    def __call__( self, *args, **kwargs ) -> "Logger":
        """
        Logs text.
        """
        if self.enabled:
            self.print( self.format( *args, *kwargs ) )
        
        return self
    
    
    def format( self, *args, **kwargs ) -> str:
        """
        Formats text for output.
        """
        if len( args ) == 1:
            r = str( args[0] )
        elif len( args ) > 1:
            vals = list( args[1:] )
            for i in range( len( vals ) ):
                v = vals[i]
                
                if type( v ) in (set, list, tuple, frozenset):
                    v = string_helper.array_to_string( v, **kwargs )
                
                vals[i] = "«" + str( v ) + "»"
            
            r = args[0].format( *vals )
        else:
            r = ""
        
        indent = " " * (self.__indent * self.__INDENT_SIZE)
        return indent + r.replace( "\n", "\n" + indent )
    
    
    class defer:
        """
        Allows a function passed via format to lazily load its string representation.
        """
        
        
        def __init__( self, fn ):
            self.fn = fn
        
        
        def __repr__( self ):
            return self.fn()
    
    
    def print( self, message: str ) -> None:
        self.__true_logger.log( self.__level, message )
    
    
    @property
    def indent( self ) -> int:
        return self.__indent
    
    
    @indent.setter
    def indent( self, level: int ) -> None:
        assert isinstance( level, int )
        self.__indent = level
    
    
    def __enter__( self ) -> None:
        """
        Indents the logger.
        
        Since `self` is returned from `__call__`, both `with log:` and
        `with log("spam"):` are permissible.
        """
        self.indent += 1
    
    
    def __exit__( self, exc_type, exc_val, exc_tb ) -> None:
        """
        Un-indents the logger.
        """
        self.indent -= 1
    
    
    def time( self, title ):
        """
        Logs the time taken for the `with` block::
        
            with log.time():
                ...
        """
        return _Time( self, title )
    
    
    def attach( self, fn = None ):
        """
        Logs when a function is called.
        """
        
        
        def dec( fn ):
            def ret( *args, **kwargs ):
                self( "@{}", fn.__name__ )
                
                with self:
                    return fn( *args, **kwargs )
            
            
            return ret
        
        
        if fn:
            return dec( fn )
        else:
            return dec
    
    
    def enumerate( self, *args, **kwargs ):
        """
        Logs the iterations of an `enumerate`.
        See `iterate`.
        """
        return enumerate( self.iterate( *args, **kwargs ) )
    
    
    def action( self, title = None, *args, **kwargs ):
        pm = progress_helper.ProgressMaker( *args,
                                            title = title,
                                            issue = self.__action_iterate,
                                            **kwargs )
        
        return disposal_helper.ManagedWith( target = pm,
                                            on_exit = self.__action_exit,
                                            on_enter = self.__action_enter )
    
    
    def __action_iterate( self, x: progress_helper.Progress ):
        self( x )
    
    
    def __action_enter( self, action: progress_helper.ProgressMaker ):
        action.begin()
        self.indent += 1
    
    
    def __action_exit( self, action: progress_helper.ProgressMaker ):
        self.indent -= 1
        action.complete()
    
    
    def iterate( self, records: Iterable[T], count = None, *args, **kwargs ) -> Iterator[T]:
        """
        Logs the iterations.
        
        :param records:     Iterable 
        :param count:       Number of records (can be ignored if `records` has a `len`)
        :param args:        See `progress_helper.ProgressMaker`
        :param kwargs:      See `progress_helper.ProgressMaker`
        :return:            Iterator over `records` that logs the iterator's progress. 
        """
        if not self:
            for record in records:
                yield record
        else:
            if count is None:
                try:
                    # noinspection PyTypeChecker
                    count = len( records )
                except Exception:
                    count = None
            
            with self.action( total = count, *args, **kwargs ) as action:
                for current, record in enumerate( records ):
                    action.report( current )
                    yield record


class _Time:
    def __init__( self, logger, name ):
        self.logger = logger
        self.name = name
    
    
    def __enter__( self ):
        self.start = time.perf_counter()
        self.logger( "{} - {}".format( self.name, "...please wait..." ) )
        self.logger.indent += 1
    
    
    def __exit__( self, exc_type, exc_val, exc_tb ):
        elapsed = time.perf_counter() - self.start
        self.logger( "{} - ...completed in {{}}.".format( self.name ), string_helper.timedelta_to_string( elapsed, hz = True ) )
        self.logger.indent -= 1


def open_parallel_log_view():
    th = threading.Thread( target = __parallel_log_view, daemon = True, name = "parallel_log_view" )
    th.start()


def __parallel_log_view():
    print( "~~~~ THE PARALLEL LOG VIEW IS ACCEPTING INPUT", file = sys.stderr )
    
    while True:
        try:
            input_ = input( "" )
        except KeyboardInterrupt:
            input_ = None  # for IDE
            print( "~~~~ THE PROGRAM WILL BE FORCEFULLY TERMINATED", file = sys.stderr )
            os._exit( 0 )
        
        if input_ == "exit":
            print( "~~~~ THE PROGRAM WILL BE FORCEFULLY TERMINATED", file = sys.stderr )
            os._exit( 0 )
        elif input_ == "return":
            print( "~~~~ THE PARALLEL LOG VIEW IS NO LONGER ACCEPTING INPUT", file = sys.stderr )
            return
        elif not input_:
            print( "~~~~ AVAILABLE LOGGERS:", file = sys.stderr )
            
            for name in logging.root.manager.loggerDict:
                logger = logging.getLogger( name )
                if logger.level == logging.DEBUG:
                    level = "[X]"
                elif logger.level == logging.NOTSET:
                    level = "[ ]"
                else:
                    level = "[{}]".format( logging.getLevelName( logger.level )[0] )
                
                print( "~~~~     {1} {0}".format( logger.name, level ), file = sys.stderr )
        else:
            if input_.startswith( "+" ):
                toggle = True
                input_ = input_[1:]
            elif input_.startswith( "-" ):
                toggle = False
                input_ = input_[1:]
            else:
                toggle = None
            
            if input_ == "all":
                loggers = list( logging.root.manager.loggerDict.values() )
            else:
                logger = logging.root.manager.loggerDict.get( input_ )
                
                if not logger:
                    print( "~~~~ No such logger as '{}'.".format( input_ ), file = sys.stderr )
                    continue
                
                loggers = [logger]
            
            for logger in loggers:
                if toggle is None:
                    new = logger.level == logging.NOTSET
                else:
                    new = toggle
                
                if new:
                    logger.level = logging.DEBUG
                    print( "~~~~ {} on".format( logger.name ), file = sys.stderr )
                else:
                    logger.level = logging.NOTSET
                    print( "~~~~ {} off".format( logger.name ), file = sys.stderr )


_itl = namedtuple( "_itl", ["name", "logger", "level_name", "level", "handlers", "description", "mh_logger"] )


def iterate_loggers() -> List[_itl]:
    manager = getattr( logging.Logger, "manager" )
    
    r = []
    
    for name, logger in manager.loggerDict.items():
        if isinstance( logger, logging.Logger ):
            h = ""
            ml = None
            
            for x in logger.handlers:
                if isinstance( x, Handler ) and x.logger is not None:
                    l: Logger = x.logger
                    h += l.comment
                    assert ml is None or ml is x.logger
                    ml = x.logger
            
            r.append( _itl( name,
                            logger,
                            logging.getLevelName( logger.level ),
                            logger.level,
                            logger.handlers,
                            h,
                            ml ) )
        else:
            r.append( _itl( name,
                            None,
                            "MISSING",
                            -1,
                            (),
                            "",
                            None ) )
    
    return r
