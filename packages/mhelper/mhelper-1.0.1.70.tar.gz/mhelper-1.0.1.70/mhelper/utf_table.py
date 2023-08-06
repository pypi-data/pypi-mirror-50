"""
This is a package for drawing ASCII boxes and tables.

A variety of box drawing character sets are specified, and table drawing
supports wrapping and text spanning multiple columns.

Unlike most other available tools, the direction of lines is honoured and
UTF characters can be used.

Usage
-----

To draw a table, please see the `TextTable` class documentation.
"""
import itertools
from typing import Sequence, Optional, Union, List, Tuple, Iterable


class BoxChars:
    """
    Describes the characters used to draw a box as text, providing several
    predefined sets.
    
    :cvar SINGLE:       Single lined (UTF)
    :cvar DOUBLE:       Double lined (UTF) 
    :cvar DOTTED:       Dotted lined (UTF)
    :cvar BOLD:         Bold lined (UTF)
    :cvar BLANK:        Made of spaces (ASCII)
    :cvar ASCII:        ASCII characters only (ASCII)
    :cvar CURVED:       Single lined, curved corners (UTF)
    :cvar BLOCK:        Half-block outlines (UTF)
    :cvar SOLID:        Full-block outlines (UTF)
    
    :ivar ts: Defines the character for ``▀`` "top straight across"
    :ivar hs: Defines the character for ``━`` "horizontal_middle straight across" 
    :ivar bs: Defines the character for ``▄`` "bottom straight across"
    :ivar ls: Defines the character for `` │`` "left straight down" 
    :ivar vs: Defines the character for `` │ `` "vertical_middle straight down"
    :ivar rs: Defines the character for ``│ `` "right straight down"
    :ivar tl: Defines the character for ``┌┄`` "top-left corner"
    :ivar tr: Defines the character for ``┄┐`` "top-right corner"
    :ivar bl: Defines the character for ``└┄`` "bottom-left corner"
    :ivar br: Defines the character for ``┄┘`` "bottom-right corner"
    :ivar tm: Defines the character for ``┄┬┄`` "top-vertical_middle join"
    :ivar bm: Defines the character for ``┄┴┄`` "bottom-vertical_middle join"
    :ivar lm: Defines the character for ``├┄`` "left-horizontal_middle join"
    :ivar rm: Defines the character for ``┄┤`` "right-horizontal_middle join"
    :ivar mm: Defines the character for ``┄┼┄`` "horizontal_middle-vertical_middle join (up and down)"
    :ivar md: Defines the character for ``┄┬┄`` "horizontal_middle-vertical_middle join (down only)" 
    :ivar mu: Defines the character for ``┄┴┄`` "horizontal_middle-vertical_middle join (up only)"
    """
    SINGLE: "BoxChars" = None
    DOUBLE: "BoxChars" = None
    DOTTED: "BoxChars" = None
    BOLD: "BoxChars" = None
    BLANK: "BoxChars" = None
    ASCII: "BoxChars" = None
    CURVED: "BoxChars" = None
    BLOCK: "BoxChars" = None
    SOLID: "BoxChars" = None
    
    __slots__ = ("__in",
                 "ts",
                 "hs",
                 "bs",
                 "ls",
                 "vs",
                 "rs",
                 "tl",
                 "tr",
                 "bl",
                 "br",
                 "tm",
                 "bm",
                 "lm",
                 "rm",
                 "mm",
                 "md",
                 "mu",
                 "em",
                 "__padded")
    
    
    def __init__( self, x = None ):
        """
        CONSTRUCTOR
        
        :param x:   An optional character array to read in.
                    The order of the characters is that used for BoxChars.SINGLE
                    and is not repeated here.
                    If this value is `None` the object remains empty until it is
                    populated manually.
        """
        if not x:
            return
        
        self.__in = x
        (self.ts,  # ^ ─── top straight across
         self.hs,  # ~ ─── horizontal_middle straight across 
         self.bs,  # v ─── bottom straight across
        
         self.ls,  # - │.  left straight down
         self.vs,  # - .│. vertical_middle straight down
         self.rs,  # -  .│ right straight down
        
         self.tl,  # ^ ┌── top-left corner
         self.tr,  # ^ ──┐ top-right corner
        
         self.bl,  # v └── bottom-left corner
         self.br,  # v ──┘ bottom-right corner
        
         self.tm,  # ^ ─┬─ top-vertical_middle join
         self.bm,  # v ─┴─ bottom-vertical_middle join
        
         self.lm,  # ~ ├── left-horizontal_middle join
         self.rm,  # ~ ──┤ right-horizontal_middle join
        
         self.mm,  # ~ ─┼─ horizontal_middle-vertical_middle join (up and down)
         self.md,  # ~ ─┬─ horizontal_middle-vertical_middle join (down only) 
         self.mu,  # ~ ─┴─ horizontal_middle-vertical_middle join (up only)
         ) = x
        
        self.em = " "  # empty space
        
        self.__padded = None
    
    
    def pad( self ) -> "BoxChars":
        """
        Obtains a version of the box width 1 character margins around the 
        inside columns.
        """
        if self.__padded is None:
            r = BoxChars()
            r.ts = self.ts
            r.hs = self.hs
            r.bs = self.bs
            r.ls = self.ls + " "
            r.vs = " " + self.vs + " "
            r.rs = " " + self.rs
            r.tl = self.tl + self.ts
            r.tr = self.ts + self.tr
            r.bl = self.bl + self.bs
            r.br = self.bs + self.br
            r.tm = self.ts + self.tm + self.ts
            r.bm = self.bs + self.bm + self.bs
            r.lm = self.lm + self.hs
            r.rm = self.hs + self.rm
            r.mm = self.hs + self.mm + self.hs
            r.mu = self.hs + self.mu + self.hs
            r.md = self.hs + self.md + self.hs
            self.__padded = r
        
        return self.__padded
    
    
    def format( self, prefix, suffix ):
        return BoxChars( "".join( "{}{}{}".format( prefix, char, suffix ) for char in self.__in ) )
    
    
    def hline( self, pos: int, widths: Union[int, Sequence[int]], dirs = None ) -> str:
        """
        Returns a horizontal box line.
        
        :param pos:     Vertical position (-1 = top, 0 = middle, 1 = bottom)
        :param widths:  Widths or content of column(s). If widths lines
        :param dirs:    Optional vector of same length as `widths`.
                        Controls the direction of joins (2 = up, 3 = both, 1 = down, 0 = none).
                        Will not work if `pos` is not `0`. 
        :return:        The line as a string 
        """
        if pos == -1:
            return self.__hline( widths, self.ts, self.tl, self.tm, self.tr, dirs )
        elif pos == 0:
            return self.__hline( widths, self.hs, self.lm, self.mm, self.rm, dirs )
        elif pos == 1:
            return self.__hline( widths, self.bs, self.bl, self.bm, self.br, dirs )
    
    
    def hcontent( self, *args, **kwargs ):
        from mhelper import string_helper
        return string_helper.format_row( *args, **kwargs, left = self.ls, right = self.rs, centre = self.vs )
    
    
    def __hline( self, widths, s, l, m, rx, dirs ):
        r = []
        
        if dirs is None:
            dirs = [0] * len( widths )
        
        for i, (dir, width) in enumerate( zip( dirs, widths ) ):
            if i == 0:
                r.append( l )
            else:
                if dir == 3:
                    r.append( m )
                elif dir == 2:
                    r.append( self.mu )
                elif dir == 1:
                    r.append( self.md )
                elif dir == 0:
                    r.append( s * len( self.mm ) )
                else:
                    raise ValueError( "Invalid `dir` {}.".format( dir ) )
            
            r.append( s * width )
        
        r.append( rx )
        
        return "".join( r )


BoxChars.SINGLE = BoxChars( "───│││┌┐└┘┬┴├┤┼┬┴" )
BoxChars.DOUBLE = BoxChars( "═══║║║╔╗╚╝╦╩╠╣╬╦╩" )
BoxChars.DOTTED = BoxChars( "┄┄┄┆┆┆┌┐└┘┬┴├┤┼┬┴" )
BoxChars.BOLD = BoxChars( "━━━┃┃┃┏┓┗┛┳┻┣┫╋┳┻" )
BoxChars.BLANK = BoxChars( "                 " )
BoxChars.ASCII = BoxChars( r"---|||/\\/+++++++" )
BoxChars.CURVED = BoxChars( "───│││╭╮╰╯┬┴├┤┼┬┴" )
BoxChars.BLOCK = BoxChars( "▀▀▄▌▌▐▛▜▙▟▛▙▛▜▙▛▀" )
BoxChars.SOLID = BoxChars( "█████████████████" )


class _RowInfo:
    def __init__( self, cur: Sequence[Optional[str]], table: "TextTable" ):
        txt = []
        wid = []
        msk = [True] * len( table._col_widths )
        
        for i, x in enumerate( cur ):
            if x is None:
                wid[-1] += table._col_widths[i] + table._box_width
                msk[i] = False
            else:
                txt.append( x )
                wid.append( table._col_widths[i] )
        
        self.text = txt
        self.width = wid
        self.mask = msk


class TextTable:
    """
    Class that renders tables as text.
    
    :ivar _col_widths:  Widths of columns.
                        The length of this array defines the number of columns. 
    :ivar _box:         Set of characters to use for the outlines.
    :ivar _box_width:   Space the column dividers take up.
    :ivar _data:        Array of rows.
    """
    
    __slots__ = ("_col_widths",
                 "_box",
                 "_box_width",
                 "_data")
    
    
    def __init__( self, col_widths, *, box = None ):
        """
        Initialises the table.
        
        :param col_widths:  Widths of columns.
                            The length of this array defines the number of columns. 
        :param box:         Set of characters to use for the outlines.
                            The SINGLE box, padded, is used if `None`. 
        """
        self._col_widths: Tuple[int, ...] = tuple( col_widths )
        self._box: BoxChars = box or BoxChars.SINGLE.pad()
        self._box_width: int = len( box.mm )
        self._data: List[Optional[_RowInfo]] = []
    
    
    @staticmethod
    def from_table( rows: Sequence[Optional[Sequence[str]]], no_span = True, box = None ) -> "TextTable":
        """
        Creates a new `TextTable` from a sequence of rows.
        The column widths are taken from the longest cell for each column.
        
        :param rows:            Series of rows.
                                Use `None` to insert horizontal lines. 
        :param no_span:         When set, `None` or missing values are converted
                                to empty cells, preventing `TextTable` from
                                rendering them as multi-column cells. 
        :param box:             Passed to the `TextTable` constructor. 
        :return:                A new `TextTable` object. 
        """
        lens = []
        
        for row in rows:
            if row is not None:
                for col, cell in enumerate( row ):
                    if len( lens ) <= col:
                        lens.append( len( cell ) )
                    elif lens[col] < len( cell ):
                        lens[col] = len( cell )
        
        r = TextTable( lens, box = box )
        
        for row in rows:
            if no_span and row is not None:
                row = [cell if cell is not None else "" for cell in row]
                
                if len( row ) < len( lens ):
                    row += [""] * (len( lens ) - len( row ))
            
            r.add( row )
        
        return r
    
    
    def add( self, row: Sequence[Optional[str]], *, wrap = False ):
        """
        Adds a row to the table.
        
        
        :param row: A list of values.
                    Use `None` to have the previous value span multiple columns.
                    Missing values will be assumed to be `None`.
                    The list may not contain more values than columns.
        :param wrap: When set, behaves the same as `add_wrapped`, otherwise
                     text larger than the row width will be truncated. 
        """
        if wrap:
            self.add_wrapped( row )
            return
        
        row = self.__check_row_size( row )
        self._data.append( _RowInfo( row, self ) )
    
    
    def __check_row_size( self, row ):
        if isinstance( row, str ):
            raise RuntimeError( "Row is `str`, this is probably a mistake. Did you mean to use `[x]` instead of `x`?" )
        
        if len( row ) < len( self._col_widths ):
            row = list( row ) + ([None] * (len( self._col_widths ) - len( row )))
            
        if len( row ) != len( self._col_widths ):
            raise RuntimeError( "More values than {} columns: {}".format( len( self._col_widths ), row ) )
        
        return row
    
    
    def add_wrapped( self, row ):
        """
        Generates multiple rows to account for long text.
        
        :param row: A list of values.
                    Use `None` to have the previous value span multiple columns. 
        """
        row = self.__check_row_size( row )
        row_info = _RowInfo( row, self )
        width_iter = iter( row_info.width )
        widths = [next( width_iter ) if txt else 0 for txt in row]
        from mhelper import string_helper
        row_lines = [string_helper.wrap( cell, width ) if cell is not None else [] for cell, width in zip( row, widths )]
        
        for new_row in itertools.zip_longest( *row_lines ):
            new_row = [(new_cell or "") if orig_cell is not None else None for new_cell, orig_cell in zip( new_row, row )]
            self.add( new_row )
    
    
    def add_line( self ):
        """
        Adds a line to the table.
        
        If called multiple times in succession then the superfluous calls are ignored.
        """
        if self._data and self._data[-1] is None:
            return
        
        self._data.append( None )
    
    
    def to_string( self ) -> str:
        """
        Renders the table as a string.
        """
        from mhelper import array_helper
        
        r = []
        last = len( self._data ) - 1
        
        for index, (prev, cur, next) in enumerate( array_helper.lagged_iterate_3( self._data ) ):
            if cur is None:
                pos = -1 if index == 0 else 1 if index == last else 0
                
                if next:
                    mask_next = next.mask
                else:
                    mask_next = [False] * len( self._col_widths )
                
                if prev:
                    mask_prev = prev.mask
                else:
                    mask_prev = [False] * len( self._col_widths )
                
                dirs = [(1 if n else 0) | (2 if p else 0) for n, p in zip( mask_next, mask_prev )]
                r.append( self._box.hline( pos, self._col_widths, dirs ) )
            else:
                r.append( self._box.hcontent( cur.text, cur.width ) )
        
        return "\n".join( r )
