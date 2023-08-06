"""
Contains functions for printing error tracebacks to an ANSI terminal using
colour highlighting, as well as a function to replace the default Python handler
with a colour version.
"""
import sys
import warnings
from typing import Union

from mhelper import ansi, exception_helper


def print_traceback( ex = None, **kwargs ) -> None:
    """
    `print`s the result of `format_traceback_ex`. 
    """
    try:
        print( format_traceback_ex( ex, **kwargs ) )
    except Exception as ex:
        print( str( ex ) )


def install_error_hook( *, pause = False ):
    """
    Adds `print_traceback` to the system exception hook.
    """
    sys.excepthook = __my_error_hook( sys.excepthook, pause = pause )
    warnings.showwarning = __my_warning_hook( warnings.showwarning, pause = pause )


def format_traceback_ex( exception: Union[BaseException, str] = None,
                         *,
                         wordwrap: int = 0,
                         warning: bool = False,
                         message: str = None ) -> str:
    """
    Pretty formats a traceback using ANSI escape codes.
    
    :param exception:       Exception to print the traceback for. 
    :param wordwrap:        Length of wrapping for lines. 0 assumes a default. 
    :param warning:         When set, uses "warning" colours instead of "error" colours. 
    :param message:         Optional message to include at the end of the traceback. 
    :return: The formatted traceback, as a `str`.
    """
    
    from mhelper.string_helper import highlight_quotes
    
    
    p = _Palette( wordwrap, warning )
    
    tb_co = exception_helper.get_traceback_ex( exception )
    
    # Format: Traceback
    for tb_ex in tb_co.exceptions:
        # Format: Title...
        if tb_ex.index == 0:
            p.write_tbar()
        else:
            p.write_hbar()
        p.write_message( message = p.title_bold_colour + tb_ex.type + p.title_colour + ": " + tb_ex.message,
                         colour = p.title_colour )
        p.write_hbar()
        # ...end
        
        for tb_fr in tb_ex.frames:
            # Format: Location...
            if "site-packages" in tb_fr.file_name or "lib/" in tb_fr.file_name:
                fc = p.outside_file_colour
                fbc = p.outside_file_bold_colour
            else:
                fc = p.file_colour
                fbc = p.file_bold_colour
            # File "/home/mjr/work/mhelper/mhelper/string_helper.py", line 792, in wrap
            p.write_message( message = "E{exception} F{frame} File \"{file}\", line {line} in {function}" \
                             .format( exception = tb_ex.index,
                                      frame = tb_fr.index,
                                      file = fbc + tb_fr.file_name + fc,
                                      line = fbc + str( tb_fr.line_no ) + fc,
                                      function = fbc + tb_fr.function + fc ),
                             colour = fc )
            # ...end
            
            # Format: Context
            p.write_message( message = (tb_fr.code_context.replace( tb_fr.next_function,
                                                                    p.code_bold_colour + tb_fr.next_function + p.code_colour )
                                        if tb_fr.next_function
                                        else tb_fr.code_context),
                             colour = p.code_colour )
            
            # Format: Locals
            for lo in tb_fr.locals:
                p.write_message( message = ">{name} = {value}".format( name = p.locals_bold_colour + lo.name + p.locals_colour,
                                                                       value = lo.repr ),
                                 colour = p.code_colour,
                                 colour2 = p.locals_colour,
                                 justify = 1 )
    
    p.write_hbar()
    
    # Format: Exception text
    for tb_ex in tb_co.exceptions:
        # "caused by"
        if tb_ex.index != 0:
            p.write_message( message = ansi.DIM + ansi.ITALIC + "caused by",
                             colour = p.error_colour,
                             justify = 0 )
        
        # Type
        p.write_message( message = ansi.UNDERLINE + tb_ex.type,
                         colour = p.error_colour,
                         justify = -1 )
        
        # Message
        p.write_message( message = highlight_quotes( tb_ex.message, "«", "»", p.error_bold_colour, p.error_colour ),
                         colour = p.error_colour,
                         justify = -1 )
    
    # Format caller message if present
    if message is not None:
        p.write_hbar()
        p.write_message( message = "The {} trace has been printed because {}.".format( "stack" if warning else "exception", message ),
                         colour = p.error_colour,
                         justify = -1 )
    
    p.write_bbar()
    
    return "\n".join( p.output ) + ("" if warning else "\a")


class __my_error_hook:
    def __init__( self, original, pause ):
        self.original = original
        self.pause = pause
    
    
    def __call__( self, exctype, value, traceback ):
        print_traceback( value,
                         message = "the global error hook, __my_error_hook, was notified about the exception. "
                                   "The original handler will now be called." )
        if self.pause:
            input( "Press enter to continue . . . " )
        self.original( exctype, value, traceback )


class __my_warning_hook:
    def __init__( self, original, pause ):
        self.original = original
        self.pause = pause
    
    
    def __call__( self, message, category, filename, lineno, file = None, line = None ):
        print_traceback( message,
                         warning = True,
                         message = "the global warning hook, __my_warning_hook, was notified about the exception. "
                                   "The original handler will now be called. "
                                   "Extra data follows: {}".format( dict( category = category, filename = filename, lineno = lineno, file = file, line = line ) ) )
        if self.pause:
            input( "Press enter to continue . . . " )
        self.original( message, category, filename, lineno, file, line )


class _Palette:
    def __init__( self, wordwrap, warning ):
        self.output = []
        self.wordwrap = wordwrap or 140  # Total size of box
        self.fwidth = self.wordwrap - 2  # Size of box without borders
        self.width = self.wordwrap - 4  # Size of box without borders and margins
        self.reset_colour = ansi.RESET
        self.vbar, self.tl_bar, self.hbar, self.tr_bar, self.vl_bar, self.vr_bar, self.bl_bar, self.br_bar = "│┌─┐├┤└┘"
        self.error_colour = ansi.RESET + ansi.BACK_WHITE + (ansi.FORE_YELLOW if warning else ansi.FORE_RED)  # Error text colour
        self.error_bold_colour = ansi.RESET + ansi.BACK_WHITE + ansi.FORE_BLACK + ansi.ITALIC  # Error text quotes
        self.locals_colour = ansi.RESET + ansi.BACK_BRIGHT_BLACK + ansi.FORE_BLACK  # Locals colour
        self.locals_bold_colour = ansi.RESET + ansi.BACK_BRIGHT_BLACK + ansi.FORE_YELLOW  # Locals colour
        self.border_colour = ansi.RESET + ansi.FORE_WHITE + (ansi.BACK_YELLOW if warning else ansi.BACK_RED)  # Border colour
        self.code_colour = ansi.RESET + ansi.BACK_BLUE + ansi.FORE_WHITE  # Code extracts
        self.code_bold_colour = ansi.RESET + ansi.BACK_BLUE + ansi.FORE_YELLOW  # Function name
        self.file_colour = ansi.RESET + ansi.BACK_BRIGHT_YELLOW + ansi.FORE_BLACK + ansi.DIM  # File lines
        self.file_bold_colour = ansi.RESET + ansi.BACK_BRIGHT_YELLOW + ansi.FORE_BLUE + ansi.BOLD  # File names, line numbers
        self.outside_file_colour = ansi.RESET + ansi.BACK_CYAN + ansi.FORE_BLACK + ansi.DIM  # File lines
        self.outside_file_bold_colour = ansi.RESET + ansi.BACK_CYAN + ansi.FORE_BLUE + ansi.BOLD  # File names, line numbers
        self.title_colour = ansi.RESET + (ansi.BACK_YELLOW if warning else ansi.BACK_RED) + ansi.FORE_WHITE
        self.title_bold_colour = ansi.RESET + ((ansi.BACK_YELLOW + ansi.FORE_RED) if warning else (ansi.BACK_RED + ansi.FORE_YELLOW))
        
        self.left_margin = self.border_colour + self.vbar
        self.right_margin = self.border_colour + self.vbar + ansi.RESET
    
    
    def write_hbar( self ):
        self.output.append( self.border_colour + self.vl_bar + self.hbar * self.fwidth + self.vr_bar + self.reset_colour )
    
    
    def write_tbar( self ):
        self.output.append( self.border_colour + self.tl_bar + self.hbar * self.fwidth + self.tr_bar + self.reset_colour )
    
    
    def write_bbar( self ):
        self.output.append( self.border_colour + self.bl_bar + self.hbar * self.fwidth + self.br_bar + self.reset_colour )
    
    
    def write_message( self, *, message, colour, justify = -1, colour2 = "" ):
        from mhelper.ansi_helper import wrap
        
        message += colour
        
        for l in wrap( message, self.width, justify = justify ):
            self.output.append( self.left_margin + colour + " " + colour2 + l + colour + " " + self.right_margin )
