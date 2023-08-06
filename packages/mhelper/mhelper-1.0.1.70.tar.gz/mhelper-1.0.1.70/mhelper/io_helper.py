"""
Helper functions for reading and writing.
"""
import os
import sys
import platform
import tempfile
import time
import warnings
from typing import Dict, Optional, TextIO, Type, TypeVar, Union, cast, BinaryIO, List, Tuple, Sequence
from itertools import count

from mhelper import file_helper
from mhelper.comment_helper import abstract, override, virtual
from mhelper.special_types import NOT_PROVIDED
from mhelper.exception_helper import SwitchError


T = TypeVar( "T" )
U = TypeVar( "U" )
TIniSection = Dict[str, str]
TIniData = Dict[str, TIniSection]


def load_npy( file_name ):
    """
    Loads an NPY file. If it is an NPZ this extracts the `data` value automatically.
    Requires the :library:`numpy`.
    """
    # noinspection PyPackageRequirements
    import numpy
    result = numpy.load( file_name, allow_pickle = False, fix_imports = False )
    
    if file_name.upper().endswith( ".NPZ" ):
        result = result["data"]
    
    return result


def load_npz( file_name ):
    """
    Loads an NPZ file and returns the `data` value.
    Requires the :library:`numpy`.
    """
    
    # noinspection PyPackageRequirements
    import numpy
    result = numpy.load( file_name, allow_pickle = False, fix_imports = False )
    result = result["data"]
    
    return result


def save_bitarray( file_name: str, value ) -> None:
    """
    Saves a bit array.
    Requires the :library:`bitarray`.
    
    :type value: bitarray
    
    :param file_name: File name
    :param value: Value to save
    """
    try:
        # noinspection PyPackageRequirements
        from bitarray import bitarray
    except ImportError as ex:
        raise ImportError("save_bitarray requires the bitarray package.") from ex
        
    from mhelper import exception_helper, file_helper
    
    exception_helper.assert_instance( "save_bitarray::value", value, bitarray )
    assert isinstance( value, bitarray )
    
    try:
        with open( file_name, "wb" ) as file_out:
            value.tofile( file_out )
    except TypeError:
        # Stupid "open file expected" error on OSX (due to bug writing large files - fallback to manual implementation)
        _save_bytes_manually( file_name, value.tobytes() )
    except Exception as ex:
        raise ValueError( "Failed to write bitarray of length {} to «{}».".format( len( value ), file_name ) ) from ex
    
    size = float( file_helper.file_size( file_name ) )
    expected = len( value )
    
    if size < expected / 8.0:
        raise ValueError( "Saved file is shorter ({} bytes or {} bits) than the originating bitarray ({} bytes or {} bits).".format( size, size * 8, expected / 8, expected ) )


def _save_bytes_manually( file_name: str, value: bytes ):
    """
    Fallback function used by :func:`save_bitarray`.
    """
    warnings.warn( "Save bitarray failed. This is probably due to an error in your `bitarray` library. The file will be saved incrementally but this will take longer.", UserWarning )
    BATCH_SIZE = 100000
    cursor = 0
    length = len( value )
    
    with open( file_name, "wb" ) as file_out:  # note that writing large arrays on OSX is probably the problem, we can't just dump the bytes
        while cursor < length:
            next = min( cursor + BATCH_SIZE, length )
            slice = value[cursor:next]
            file_out.write( slice )
            cursor = next


def _read_bytes_manually( file_name: str ) -> bytes:
    BATCH_SIZE = 100000
    b = bytearray()
    
    with open( file_name, "rb" ) as file_in:
        while True:
            buf = file_in.read( BATCH_SIZE )
            
            if len( buf ) == 0:
                break
            
            b.extend( buf )
    
    return bytes( b )


def load_bitarray( file_name: str ):
    """
    Loads a bitarray
    :param file_name: File to read 
    :return: bitarray. Note this may be padded with missing bits. 
    """
    try:
        # noinspection PyPackageRequirements
        from bitarray import bitarray
    except ImportError as ex:
        raise ImportError("save_bitarray requires the bitarray package.") from ex
    
    result = bitarray()
    
    try:
        with open( file_name, 'rb' ) as file_in:
            result.fromfile( file_in )
    except SystemError:  # OSX error
        result = bitarray()
        result.frombytes( _read_bytes_manually( file_name ) )
        assert len( result ) != 0
    
    return result


def save_npy( file_name, value ):
    # noinspection PyPackageRequirements
    import numpy
    
    numpy.save( file_name, value, allow_pickle = False, fix_imports = False )


def save_npz( file_name, value ):
    # noinspection PyPackageRequirements
    import numpy
    
    numpy.savez_compressed( file_name, data = value )


def load_binary( file_name: str,
                 *,
                 type_: Optional[Union[Type[T], Sequence]] = None,
                 default: U = NOT_PROVIDED,
                 delete_on_fail = False,
                 values: int = 0,
                 lock: bool = False ) -> Union[T, U]:
    """
    Loads a binary file
    
    :param delete_on_fail:  Show a warning and recycle the file if *any* value
                            cannot be retrieved.
    :param file_name:       Filename to load  
    :param type_:           Type or sequence of type(s) to expect (if `None`
                            then no check is performed).
    :param default:         Default or defaults to use.
                            `NOT_PROVIDED` causes an error to be raised. 
    :param values:          Number of values to deserialise. If this is non-zero
                            then the result will be a list. This does not need
                            to be specified if `type_` is a sequence.
    :param lock:            Lock the file for read/write during the loading.
                            
    :return: Loaded data, or a sequence of loaded data. 
    """
    
    if isinstance( type_, list ) or isinstance( type_, tuple ):
        types = type_
        
        if values == 0:
            values = len( types )
        
        one = False
    elif values:
        types = [type_] * values
        one = False
    else:
        values = 1
        types = [type_]
        one = True
    
    assert values == len( types )
    
    if not isinstance( default, list ) and not isinstance( default, tuple ):
        default = [default] * values
    
    import pickle
    
    result = []
    
    delete_ex = None
    
    try:
        with with_lock( open( file_name, "rb" ), _enabled = lock ) as file:
            for index, type__, default_ in zip( count(), types, default ):
                try:
                    v = pickle.load( file, fix_imports = False )
                    
                    if type__ is not None:
                        assert isinstance( type__, type )
                        
                        if not isinstance( v, type__ ):
                            raise ValueError( "Deserialised object #{} from file «{}» was expected to be of type «{}» but it's not, its of type «{}» with a value of «{}».".format( index, file_name, type__, type( result ), result ) )
                except Exception as ex:
                    if delete_on_fail:
                        delete_ex = ex
                    
                    if default_ is NOT_PROVIDED:
                        raise
                    
                    v = default_
                
                result.append( v )
            if one:
                result = next( iter( result ) )
            
            return result
    except Exception as ex:
        if delete_on_fail:
            delete_ex = ex
        
        if one:
            return next( iter( default ) )
        else:
            return default
    finally:
        if delete_ex is not None:
            file_helper.recycle_file( file_name )
            warnings.warn( "\n"
                           "************************************************************\n"
                           "* Failed to load binary file due to an error:              *\n"
                           "************************************************************\n"
                           "* This is probably due to a version incompatibility        *\n"
                           "* You may need to recreate this file.                      *\n"
                           "* The problematic file has been sent to the recycle bin.   *\n"
                           "* If it is important, please retrieve it now.              *\n"
                           "************************************************************\n"
                           "* Error: {} : {}\n"
                           "* File : {}\n"
                           .format( type( delete_ex ).__name__, delete_ex, file_name ), UserWarning )


def save_binary( file_name: Optional[str], value = None, *, values = None, lock = False ) -> Optional[bytes]:
    """
    Saves a binary file.
        
    :param file_name:       Target file. If this is `None` the bytes are returned instead of being
                            saved.
    :param value:           Value to store 
    :param values:          Alternative to `value` that. This should be a list or tuple indicating 
                            a series of values to store sequentially. 
    :param lock:            Lock the file for read/write during the save.
    :return:                Bytes if `file_name` is `None`, else `None`.
    """
    import pickle
    
    if values is None:
        values = [value]
    elif value is not None:
        raise ValueError( "Cannot specify both `value` and `values`." )
    
    if file_name is None:
        try:
            return pickle.dumps( value, protocol = -1, fix_imports = False )
        except Exception as ex:
            raise IOError( "Error saving data to bytes. Data = «{}».".format( value ) ) from ex
    
    with with_lock( open( file_name, "wb" ), _enabled = lock ) as file:
        for value in values:
            try:
                pickle.dump( value, file, protocol = -1, fix_imports = False )
            except Exception as ex:
                raise IOError( "Error saving data to binary file. Filename = «{}». Data = «{}».".format( file_name, value ) ) from ex
    
    return None


def with_lock( handle, _enabled = True ):
    from mhelper.disposal_helper import ManagedWith
    
    if _enabled:
        return ManagedWith( handle, on_enter = lambda _: _lock( handle ), on_exit = lambda _: _unlock( handle ) )
    else:
        return ManagedWith( handle )


_lock_warning = True


def _lock( handle ):
    import fcntl, errno
    
    while True:
        try:
            fcntl.flock( handle, fcntl.LOCK_EX | fcntl.LOCK_NB )
            break
        except IOError as e:
            # raise on unrelated IOErrors
            if e.errno != errno.EAGAIN:
                raise
            else:
                global _lock_warning
                
                if _lock_warning:
                    warnings.warn( "Failed to obtain file lock '{}'. Trying again in 0.1s.".format( handle.name ), UserWarning )
                    _lock_warning = False
                
                time.sleep( 0.1 )


def _unlock( handle ):
    import fcntl
    fcntl.flock( handle, fcntl.LOCK_UN )


def load_json_data( file_name ):
    import json
    
    with open( file_name, "r" ) as file_in:
        return json.load( file_in )


def save_json_data( file_name, value ):
    import json
    
    with open( file_name, "w" ) as file_out:
        return json.dump( value, file_out, separators = (',', ':') )


def load_json_pickle( file_name, keys = True, default = NOT_PROVIDED ):
    from mhelper.file_helper import read_all_text
    import jsonpickle
    
    if default is not NOT_PROVIDED and not os.path.isfile( file_name ):
        return default
    
    text = read_all_text( file_name )
    
    return jsonpickle.decode( text, keys = keys )


def save_json_pickle( file_name, value, keys = True ):
    from mhelper.file_helper import write_all_text
    import jsonpickle
    
    write_all_text( file_name, jsonpickle.encode( value, keys = keys ) )


def default_values( target: T, default: Optional[Union[T, type]] = None ) -> T:
    if default is None:
        if target is None:
            raise ValueError( "Cannot set the defaults for the value because both the value and the defaults are `None`, so neither can be inferred." )
        
        default = type( target )
    
    if isinstance( default, type ):
        default = default()
    
    if target is None:
        return default
    
    if isinstance( target, list ):
        # noinspection PyTypeChecker
        return cast( T, target )
    
    if type( target ) is not type( default ):
        raise ValueError( "Attempting to set the defaults for the value «{}», of type «{}», but the value provided, «{}», of type «{}», is not compatible with this.".format( target, type( target ), default, type( default ) ) )
    
    for k, v in default.__dict__.items():
        if k.startswith( "_" ):
            continue
        
        if k not in target.__dict__:
            target.__dict__[k] = v
    
    to_delete = []
    
    for k in target.__dict__.keys():
        if k not in default.__dict__:
            to_delete.append( k )
    
    for k in to_delete:
        del target.__dict__[k]
    
    return target


TBStr = Union[str, bytes]


@abstract
class WriterBase:
    """
    Base class for writers.
    
    The derived class should implement:
        * (optional) A constructor
        * (optional) on_close
        * (optional) write
        * on_describe
        
    :ivar extension: Extension of the file.
    :ivar closed:    `True` once the file has been closed.
    """
    
    
    def __init__( self, *, extension = None, mode = str ):
        """
        CONSTRUCTOR
        The derived class should pass any and all `**kwargs` to the base class.
        Other `**kwargs` may be added later.
        `*args` are not used and may be passed or not.
        :param extension: Extension of the file
        """
        self.extension = extension
        self.type = mode
        self.closed = False
    
    
    def __enter__( self ):
        return self
    
    
    def __exit__( self, exc_type, exc_val, exc_tb ):
        self.close()
    
    
    def close( self ) -> None:
        if self.closed:
            return
        
        self.on_close()
        
        self.closed = True
    
    
    def write( self, text: TBStr ) -> None:
        self.on_write( text )
    
    
    @virtual
    def on_close( self ):
        pass
    
    
    @virtual
    def on_write( self, text: TBStr ) -> None:
        pass


@abstract
class BufferedWriter( WriterBase ):
    """
    Buffers all the output data to `self.lines` (currently just in memory).
    
    The derived class should commit the data when `on_close` is called.
    """
    
    
    def __init__( self, *args, **kwargs ) -> None:
        super().__init__( *args, **kwargs )
        self.lines: List[TBStr] = []
    
    
    @override
    def on_write( self, text: TBStr ) -> None:
        if self.closed:
            raise ValueError( "The virtual stream has already been closed." )
        
        self.lines.append( text )
    
    
    def __repr__( self ):
        return self.__class__.__name__
    
    
    def set_extension( self, value: TBStr ) -> None:
        pass


class StdOutWriter( BufferedWriter ):
    """
    Dumps all the data to std-out (`sys.__stdout__`) when the stream is closed.
    
    Note that only string data is written. Binary data is ignored.
    """
    
    
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        
        if self.type is not str:
            raise ValueError( "The `{}` only supports `str` output (not `{}`).".format( type( self ).__name__, type( self.type ).__name__ ) )
    
    
    def on_close( self ):
        assert self.type is str
        
        for line in self.lines:
            sys.__stdout__.write( line )


orig_stdout = sys.stdout


class TerminalWriter( BufferedWriter ):
    """
    Dumps all the data to the terminal (`sys.stdout`) when the stream is closed.
    This may or may not be the same as stdout, depending on whether `sys.stdout` has been redirected.
    
    Note that only string data is written. Binary data is ignored.
    """
    
    
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        
        if self.type is not str:
            raise ValueError( "The `{}` only supports `str` output (not `{}`).".format( type( self ).__name__, type( self.type ).__name__ ) )
    
    
    def on_close( self ):
        assert self.type is str
        
        for line in self.lines:
            sys.stdout.write( line )


class OpeningWriter( WriterBase ):
    """
    Writes all data to a temporary file.
    Opens the file in the default GUI when the stream is closed..
    The file itself is queued for delete when the program closes.
    """
    
    
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        
        if self.type is bytes:
            mode = "wb"
        else:
            mode = "w"
        
        self.file = tempfile.NamedTemporaryFile( mode, delete = False, suffix = self.extension )
        self.name = self.file.name
        queue_delete( self.name )
    
    
    def on_write( self, text: str ):
        self.file.write( text )
    
    
    def on_close( self ):
        self.file.close()
        system_open( self.name )


class MemoryWriter( BufferedWriter ):
    """
    Writes to RAM.
    * For programmatic use only.
    * Data can be retrieved via :method:`mhelper.io_helper.MemoryWriter.retrieve`
    * Does not support multiple threads.
    """
    __LAST = None
    
    
    @classmethod
    def retrieve( cls ):
        if cls.__LAST is None:
            raise ValueError( "Nothing to retrieve." )
        
        r = "\n".join( cls.__LAST )
        cls.__LAST = None
        return r
    
    
    def on_close( self ):
        type( self ).__LAST = self.lines


class ClipboardWriter( BufferedWriter ):
    """
    Dumps all the data to the clipboard when the stream is closed.
    """
    
    
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        
        # Test now
        try:
            import pyperclip
        except ImportError as ex:
            raise ValueError( "Cannot use ClipboardWriter without first installing the `pyperclip` package." ) from ex
    
    
    def on_close( self ):
        try:
            import pyperclip
        except ImportError as ex:
            raise ValueError( "Cannot use ClipboardWriter without first installing the `pyperclip` package." ) from ex
        
        if self.type is str:
            pyperclip.copy( "".join( self.lines ) )
        else:
            pyperclip.copy( b"".join( self.lines ) )


class NowhereWriter( WriterBase ):
    """
    Doesn't write anything.
    """
    pass


open_write_opts = { "stdout"  : StdOutWriter,
                    "terminal": TerminalWriter,
                    ""        : TerminalWriter,
                    "clip"    : ClipboardWriter,
                    "null"    : NowhereWriter,
                    "open"    : OpeningWriter,
                    "memory"  : MemoryWriter }


def open_write( file_name: str, extension: str = "", mode: type = str ) -> Union[WriterBase, TextIO, BinaryIO]:
    """
    Opens a file for writing, accepts any of the special values in the global :variable:`open_write_opts: as the filename.
    
    :param file_name:   Name of the file *or* one of the special handlers listed in `open_write_opts`.
                        `None` is treated the same as `""`.
    :param extension:   Extension (file-type) of the file. This is used by some special handlers.
    :param mode:        Mode of operation.
                        This should be either `str` or `bytes`.
    :return:            A file object *or* a file-like object (:class:`WriterBase`), which should have the following methods:
                            * write
                            * __enter__, __exit__, close
    :exception UserWarning: If a special handler is specified and it cannot be initialised due to an error, this warning
                            is raised. No error is raised and a `MemoryWriter` is returned instead. 
    """
    if file_name is None:
        file_name_lower = ""
    else:
        file_name_lower = file_name.lower()
    
    mapped: Type[BufferedWriter] = open_write_opts.get( file_name_lower )
    
    if mapped is not None:
        try:
            return mapped( extension = extension, mode = mode )
        except Exception as ex:
            warnings.warn( "Failed to initialise the writer due to `{}` '{}'. I am using a `MemoryWriter` instead.".format( type( ex ).__name__, ex ), UserWarning )
            return MemoryWriter( extension = extension, mode = mode )
    
    file_name = os.path.abspath( file_name )
    directory_name = file_helper.get_directory( file_name )
    assert directory_name, file_name
    file_helper.create_directory( directory_name )
    
    if mode is str:
        return open( file_name, "w" )
    elif mode is bytes:
        return open( file_name, "wb" )
    else:
        raise SwitchError( "type_", mode )


def load_ini( file_name: str, comments: str = (";", "#", "//"), stop: Tuple[str, str] = None ) -> Dict[str, Dict[str, str]]:
    """
    Loads an INI file.
    
    :param stop:            When this section and key are encountered, reading the INI stops with
                            whatever has been loaded so far.
    :param file_name:       File to load 
    :param comments:        Comment lines 
    :return:                INI data:
                                str - Section name ("" contains the data from any untitled section or sections with no name `[]`)
                                dict - Section data:
                                    str - Field key
                                    str - field value
    """
    r = { }
    unsectioned = { }
    section = unsectioned
    section_name = ""
    
    for line in open( file_name, "r" ):
        line = line.strip()
        
        if any( line.startswith( x ) for x in comments ):
            continue
        
        if line.startswith( "[" ) and line.endswith( "]" ):
            section = { }
            section_name = line[1:-1]
            r[section_name] = section
        elif "=" in line:
            k, v = line.split( "=", 1 )
            section[k.strip()] = v.strip()
            
            if stop is not None and stop[0] == section_name and stop[1] == k:
                break
    
    if unsectioned:
        if "" in r:
            unsectioned.update( r[""] )
        
        r[""] = unsectioned
    
    return r


def save_ini( file_name: str, data: Dict[str, Dict[str, str]] ) -> None:
    with open( file_name, "w" ) as file:
        if "" in data:
            __write_ini_section( data[""], file )
        
        for section, fields in data.items():
            if section:
                file.write( "[{}]\n".format( section ) )
                __write_ini_section( fields, file )


def __write_ini_section( fields, file ):
    for name, value in fields.items():
        file.write( "{}={}\n".format( name, value ) )
    file.write( "\n" )


class queue_delete:
    """
    The file will be deleted when the program closes.
    
    If the program force-closes then the file is not deleted.
    
    :remarks:           Class masquerading as function.
                        
                        Example usage:
                            ```
                            queue_delete( "c:\my_temporary_file.txt" )
                            ```    
    
    :cvar queued:       Gets the list of files to be deleted.
                        Acts to keep the references alive until the program closes.
    :ivar file_name:    Name of the file
    """
    
    queued = []
    
    
    def __init__( self, file_name: str ) -> None:
        """
        CONSTRUCTOR
        Automatically adds the reference to the queue, keeping it alive
        until the program closes.
        
        :param file_name: Name of the file
        """
        self.file_name = file_name
        self.queued.append( self )
    
    
    def __del__( self ) -> None:
        """
        !OVERRIDE
        On deletion, removes the file.
        """
        os.remove( self.file_name )


class with_delete:
    """
    The file will be deleted when the with block ends
    """
    
    
    def __init__( self, file_name: str = None, *, condition: bool = True ):
        """
        Names a file that is deleted when the with block ends.
        
        :param file_name:   A filename (not starting `.`), an extension of a new temporary file (starting `.`), or `None`, for an extension-less temporary file. 
        """
        if not file_name or file_name.startswith( "." ):
            file_name = tempfile.NamedTemporaryFile( "w", delete = False, suffix = file_name )
        
        self.file_name = file_name
        self.condition = condition
    
    
    def __enter__( self ):
        """
        `with` returns the filename.
        """
        return self.file_name
    
    
    def __exit__( self, exc_type, exc_val, exc_tb ):
        """
        End of `with` deletes the file.
        """
        if self.condition:
            try:
                os.remove( self.file_name )
            except FileNotFoundError as ex:
                raise FileNotFoundError( "Failed to delete file '{}'.".format( self.file_name ) ) from ex


class ESystem:
    UNKNOWN = 0
    WINDOWS = 1
    MAC = 2
    LINUX = 3


def get_system():
    s = platform.system()
    if s == "Windows":
        return ESystem.WINDOWS
    elif s == "Darwin":
        return ESystem.MAC
    elif s == "Linux":
        return ESystem.LINUX
    else:
        return ESystem.UNKNOWN


def system_open( file_name: str ):
    """
    Opens the file with the default editor.
    (Only works on Windows, Mac and GUI GNU/Linuxes)
    """
    s = platform.system()
    if s == "Windows":
        os.system( file_name )
    elif s == "Darwin":
        os.system( "open \"" + file_name + "\"" )
    elif s == "Linux":
        os.system( "xdg-open \"" + file_name + "\"" )
    else:
        warnings.warn( "I don't know how to open files with the default editor on your platform '{}'.".format( s ) )


def system_select( file_name: str ):
    """
    Selects the file with the default file explorer.
    (Only works on Windows, Mac and GUI Linuxes)
    """
    s = platform.system()
    if s == "Windows":
        os.system( "explorer.exe /select,\"{}\"".format( file_name ) )
    elif s == "Darwin":
        os.system( "open -R \"{}\"".format( file_name ) )
    elif s == "Linux":
        # Just open the parent directory on Linux
        file_name = os.path.split( file_name )[0]
        os.system( "xdg-open \"{}\"".format( file_name ) )
    else:
        warnings.warn( "I don't know how to open files with the default editor on your platform '{}'.".format( s ) )


def hash_file( file_name: str, algorithm = "sha1" ) -> str:
    import hashlib
    sha1 = getattr( hashlib, algorithm )()
    BUF_SIZE = 10000
    
    with open( file_name, 'rb' ) as f:
        while True:
            data = f.read( BUF_SIZE )
            if not data:
                break
            sha1.update( data )
    
    return sha1.hexdigest()


def system_cls():
    """
    Clears the terminal display.
    
    .. note::
    
        The proper way is to send the correct ANSI sequence, however in practice this produces odd results.
        So we just use the specific system commands.
        Note that we send two ``clear``s for Unix - once doesn't fully clear the display. 
    """
    if sys.platform.lower() == "windows":
        os.system( "cls" )
    else:
        os.system( "clear ; clear" )


def ungzip( in_file_name, out_file_name = None ):
    """
    Un-Gzips a file.
    
    :param in_file_name:    Input file. This is not deleted. 
    :param out_file_name:   Output file. If `None` then `in_file_name` is used, minus its `.gz` extension. 
    :return:                Output file name. 
    """
    if out_file_name is None:
        if file_helper.get_extension( in_file_name ).lower() != ".gz":
            raise ValueError( "Cannot generate the out_file_name from an in_file_name ('{}') not ending in '.gz'.".format( in_file_name ) )
        
        out_file_name = file_helper.get_full_filename_without_extension( in_file_name )
    
    import gzip
    import shutil
    with gzip.open( in_file_name, "rb" ) as f_in:
        with open( out_file_name, "wb" ) as f_out:
            shutil.copyfileobj( f_in, f_out )
    
    return out_file_name


# region Deprecated

def load_json( file_name, keys = True, default = NOT_PROVIDED ):
    warnings.warn( "Ambiguous - use load_json_data or `load_json_pickle`", DeprecationWarning )
    return load_json_pickle( file_name, keys = keys, default = default )


def save_json( file_name, value, keys = True ):
    warnings.warn( "Ambiguous - use save_json_data or `save_json_pickle`", DeprecationWarning )
    return save_json_pickle( file_name, value, keys = keys )

# endregion
