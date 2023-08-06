from collections import Counter
from enum import Enum, Flag

from mhelper.unittests._test_base import test, testing
from mhelper import string_helper as s


@test
def array_to_string():
    testing( s.array_to_string( [1, 2, 3] ) ).EQUALS( "1, 2, 3" )
    testing( s.array_to_string( [1, 2, 3], delimiter = "|" ) ).EQUALS( "1|2|3" )
    testing( s.array_to_string( [1, 2, 3], last_delimiter = "|" ) ).EQUALS( "1, 2|3" )
    testing( s.array_to_string( [1, 3, 2], sort = True ) ).EQUALS( "1, 2, 3" )
    testing( s.array_to_string( [1, 2, 3], format = "s{}e" ) ).EQUALS( "s1e, s2e, s3e" )
    testing( s.array_to_string( [1, 2, 3], format = lambda x: "s{}e".format( x ) ) ).EQUALS( "s1e, s2e, s3e" )
    testing( s.array_to_string( [1, 2, 3, 4, 5], limit = 3 ) ).EQUALS( "1, 2, 3, ..." )
    testing( s.array_to_string( [1, 2, 3, 4, 5], limit = 3, ellipsis = "?" ) ).EQUALS( "1, 2, 3, ?" )
    testing( s.array_to_string( [] ) ).EQUALS( "∅" )
    testing( s.array_to_string( [], empty = "X" ) ).EQUALS( "X" )
    testing( s.array_to_string( [1, 2, 3, 8, 9, 10, 15], autorange = True ) ).EQUALS( "1-3, 8-10, 15" )


@test
def as_delta():
    testing( s.as_delta( 5 ) ).EQUALS( "+5" )
    testing( s.as_delta( -5 ) ).EQUALS( "-5" )
    testing( s.as_delta( 0 ) ).EQUALS( "±0" )


@test
def assert_unicode():
    s.assert_unicode()


@test
def bracketed_split():
    testing( s.bracketed_split( "(1,2),(3,4,5),6,7,(8)", ",", "(", ")" ) ).EQUALS( ["1,2", "3,4,5", "6", "7", "8"] )
    testing( s.bracketed_split( "1,2,(3,4,5),6,7,8", ",", "(", ")" ) ).EQUALS( ["1", "2", "3,4,5", "6", "7", "8"] )


@test
def bulk_replace():
    testing( s.bulk_replace( "value <one> and <two> <two> two", one = "alpha", two = "beta" ) ).EQUALS( "value alpha and beta beta two" )
    testing( s.bulk_replace( "value +one and +two <two> two", format = "+*", one = "alpha", two = "beta" ) ).EQUALS( "value alpha and beta <two> two" )


@test
def capitalise_first():
    testing( s.capitalise_first( "hello, world" ) ).EQUALS( "Hello, world" )
    testing( s.capitalise_first( "HELLO, WORLD" ) ).EQUALS( "HELLO, WORLD" )


@test
def capitalise_first_and_fix():
    testing( s.capitalise_first_and_fix( "hello,_world" ) ).EQUALS( "Hello, world" )
    testing( s.capitalise_first_and_fix( "HELLO,_WORLD" ) ).EQUALS( "HELLO, WORLD" )


@test
def centre_align():
    # Deprecated
    pass


@test
def cjust():
    testing( s.cjust( "lemon", 10 ) ).EQUALS( "  lemon   " )
    testing( s.cjust( "lemons", 10 ) ).EQUALS( "  lemons  " )
    testing( s.cjust( "lemon sherbet", 10 ) ).EQUALS( "lemon sherbet" )


@test
def counter_to_str():
    counter = Counter( { "a": 10, "b": 20, "c": 30 } )
    testing( s.counter_to_str( counter, format = "x" ) ).EQUALS( "30xc, 20xb, 10xa" )


@test
def current_time():
    s.current_time()


@test
def curtail():
    testing( s.curtail( "hello, world", start = "hello" ) ).EQUALS( ", world" )
    testing( s.curtail( "hello, world", end = "world" ) ).EQUALS( "hello, " )
    testing( s.curtail( "hello, world", start = "hello", end = "world" ) ).EQUALS( ", " )


@test
def dump_data():
    # Deprecated
    pass


@test
def enum_to_string():
    testing( s.enum_to_string( MyEnum.alpha ) ).EQUALS( "alpha" )
    testing( s.enum_to_string( MyEnum.beta ) ).EQUALS( "beta" )


@test
def EnumMap():
    # Deprecated
    pass


@test
def find():
    testing( s.find( source = ["alpha", "beta", "gamma"], search = "alpha" ) ).EQUALS( "alpha" )
    testing( s.find( source = ["alpha", "beta", "gamma"], search = "alpha", detail = "foo" ) ).EQUALS( "alpha" )
    testing( s.find( source = ["alpha", "beta", "gamma"], search = "x_alpha", namer = lambda x: "x_{}".format( x ) ) ).EQUALS( "alpha" )
    testing( s.find( source = ["alpha", "beta", "gamma"], search = "alp", fuzzy = True ) ).EQUALS( "alpha" )
    testing( s.find( source = ["alpha", "beta", "gamma"], search = "bar", default = "zero" ) ).EQUALS( "zero" )
    testing( s.find( source = ["alpha", "beta", "gamma"], search = "Alpha", default = "zero" ) ).EQUALS( "alpha" )
    testing( s.find( source = ["alpha", "beta", "gamma"], search = "Alpha", default = "zero", case = True ) ).EQUALS( "zero" )
    
    try:
        s.find( source = ["alpha", "beta", "gamma"], search = "blah" )
        assert False
    except s.FindError:
        assert True


@test
def FindError():
    s.FindError( "This is not an error." )


@test
def first_line():
    testing( s.first_line( "hello, world\ntoday is a good day" ) ).EQUALS( "hello, world" )


@test
def first_word():
    testing( s.first_word( "hello, world\ntoday is a good day" ) ).EQUALS( "hello" )


@test
def first_words():
    testing( s.first_words( "hello, world\ntoday is a good day" ) ).EQUALS( "hello day" )


@test
def fix_indents():
    testing( s.fix_indents( """
                            This is some text
                                and this is indented
                            """ ) ).EQUALS(
            "\nThis is some text\n    and this is indented\n" )


@test
def fix_width():
    testing( s.fix_width( "hello, world", 10 ) ).EQUALS( "hello, wo…" )
    testing( s.fix_width( "hello", 10, char = "-", justify = -1 ) ).EQUALS( "hello-----" )
    testing( s.fix_width( "hello", 10, char = "-", justify = 0 ) ).EQUALS( "--hello---" )
    testing( s.fix_width( "hello", 10, char = "-", justify = 1 ) ).EQUALS( "-----hello" )


@test
def flag_to_string():
    class MyFlag( Flag ):
        alpha = 1
        beta = 2
    
    
    testing( s.flag_to_string( MyFlag.alpha ) ).EQUALS( "alpha" )
    testing( s.flag_to_string( MyFlag.alpha | MyFlag.beta ) ).EQUALS( "alpha|beta" )
    testing( s.flag_to_string( MyFlag.alpha | MyFlag.beta, delimiter = ", " ) ).EQUALS( "alpha, beta" )


@test
def format_array():
    # Deprecated
    pass


@test
def format_size():
    testing( s.format_size( 1 ) ).EQUALS( "1.0b" )
    testing( s.format_size( 1 * 1024 ) ).EQUALS( "1.0kb" )
    testing( s.format_size( 1 * 1024 * 1024 ) ).EQUALS( "1.0Mb" )
    testing( s.format_size( 1 * 1024 * 1024 * 1024 ) ).EQUALS( "1.0Gb" )
    testing( s.format_size( 2 ) ).EQUALS( "2.0b" )
    testing( s.format_size( 2 * 1024 ) ).EQUALS( "2.0kb" )
    testing( s.format_size( 2 * 1024 * 1024 ) ).EQUALS( "2.0Mb" )
    testing( s.format_size( 2 * 1024 * 1024 * 1024 ) ).EQUALS( "2.0Gb" )


@test
def get_indent():
    testing( s.get_indent( "hello" ) ).EQUALS( 0 )
    testing( s.get_indent( "    hello" ) ).EQUALS( 4 )
    testing( s.get_indent( "        hello" ) ).EQUALS( 8 )


# noinspection SpellCheckingInspection
@test
def highlight_quotes():
    testing( s.highlight_quotes( "once 'upon' a time there 'was' a bear", "'", "'", colour = "X", normal = "Y" ) ).EQUALS( "once XuponY a time there XwasY a bear" )
    testing( s.highlight_quotes( "once 'upon' a time there 'was' a bear", "'", "'", colour = "X", normal = "Y", count = 1 ) ).EQUALS( "once XuponY a time there 'was' a bear" )
    testing( s.highlight_quotes( "once 'upon' a time there [was] a bear", "[", "]", colour = "X", normal = "Y" ) ).EQUALS( "once 'upon' a time there XwasY a bear" )


@test
def highlight_regex():
    testing( s.highlight_regex( "once upon a time", "u([po]+)n", "X", "Y" ) ).EQUALS( "once uXpoYn a time" )


@test
def highlight_words():
    # Deprecated
    pass


@test
def is_int():
    testing( s.is_int( "1" ) ).EQUALS( True )
    testing( s.is_int( "100" ) ).EQUALS( True )
    testing( s.is_int( "-100" ) ).EQUALS( True )
    testing( not s.is_int( "hello" ) ).EQUALS( True )
    testing( not s.is_int( "1.2" ) ).EQUALS( True )
    testing( not s.is_int( "-1.2" ) ).EQUALS( True )


@test
def join_ex():
    # Deprecated
    pass


@test
def just():
    testing( s.just( 0, "lemon", 10, " " ) ).EQUALS( "  lemon   " )
    testing( s.just( 0, "lemons", 10, " " ) ).EQUALS( "  lemons  " )
    testing( s.just( 0, "lemon sherbet", 10, " " ) ).EQUALS( "lemon sherbet" )
    testing( s.just( 1, "lemon", 10, " " ) ).EQUALS( "     lemon" )
    testing( s.just( 1, "lemons", 10, " " ) ).EQUALS( "    lemons" )
    testing( s.just( 1, "lemon sherbet", 10, " " ) ).EQUALS( "lemon sherbet" )
    testing( s.just( -1, "lemon", 10, " " ) ).EQUALS( "lemon     " )
    testing( s.just( -1, "lemons", 10, " " ) ).EQUALS( "lemons    " )
    testing( s.just( -1, "lemon sherbet", 10, " " ) ).EQUALS( "lemon sherbet" )


@test
def ljust():
    testing( s.ljust( "lemon", 10, " " ) ).EQUALS( "lemon     " )
    testing( s.ljust( "lemons", 10, " " ) ).EQUALS( "lemons    " )
    testing( s.ljust( "lemon sherbet", 10, " " ) ).EQUALS( "lemon sherbet" )


@test
def make_name():
    testing( s.make_name( "py/things/bar" ) ).EQUALS( "py_things_bar" )
    testing( s.make_name( "c:\\blah\\foo" ) ).EQUALS( "c__blah_foo" )


@test
def max_width():
    testing( s.max_width( "hello, world", 10 ) ).EQUALS( "hello, wo…" )
    testing( s.max_width( "hello", 10 ) ).EQUALS( "hello" )


@test
def name_index():
    testing( s.name_index( ["alpha", "beta", "gamma"], "beta" ) ).EQUALS( 1 )
    testing( s.name_index( ["alpha", "beta", "gamma"], "1" ) ).EQUALS( 1 )
    testing( s.name_index( ["alpha", "beta", "gamma"], 1 ) ).EQUALS( 1 )


@test
def no_emoji():
    s.no_emoji( "😃" )


@test
def object_to_string():
    testing( s.object_to_string( "1" ) ).EQUALS( "1" )
    testing( s.object_to_string( 1 ) ).EQUALS( "1" )
    testing( s.object_to_string( 1.1 ) ).EQUALS( "1.1" )
    testing( s.object_to_string( True ) ).EQUALS( "True" )
    testing( s.object_to_string( MyEnum.alpha ) ).EQUALS( "alpha" )
    testing( s.object_to_string( MyFlags.alpha ) ).EQUALS( "alpha" )


@test
def ordinal():
    testing( s.ordinal( 0 ) ).EQUALS( "0th" )
    testing( s.ordinal( 1 ) ).EQUALS( "1st" )
    testing( s.ordinal( 2 ) ).EQUALS( "2nd" )
    testing( s.ordinal( 3 ) ).EQUALS( "3rd" )
    testing( s.ordinal( 4 ) ).EQUALS( "4th" )
    testing( s.ordinal( 5 ) ).EQUALS( "5th" )
    testing( s.ordinal( 10 ) ).EQUALS( "10th" )
    testing( s.ordinal( 11 ) ).EQUALS( "11th" )
    testing( s.ordinal( 12 ) ).EQUALS( "12th" )
    testing( s.ordinal( 13 ) ).EQUALS( "13th" )
    testing( s.ordinal( 14 ) ).EQUALS( "14th" )
    testing( s.ordinal( 20 ) ).EQUALS( "20th" )
    testing( s.ordinal( 21 ) ).EQUALS( "21st" )
    testing( s.ordinal( 22 ) ).EQUALS( "22nd" )
    testing( s.ordinal( 23 ) ).EQUALS( "23rd" )
    testing( s.ordinal( 24 ) ).EQUALS( "24th" )
    testing( s.ordinal( 25 ) ).EQUALS( "25th" )


@test
def percent():
    testing( s.percent( 0.5 ) ).EQUALS( "50%" )
    testing( s.percent( 50, 100 ) ).EQUALS( "50 (50%)" )
    testing( s.percent( 50, q = 0.5 ) ).EQUALS( "50 (50%)" )
    testing( s.percent( 50, q = 0.5 ) ).EQUALS( "50 (50%)" )
    testing( s.percent( 50, d = 100, q = 0.5 ) ).EQUALS( "50/100 (50%)" )


# noinspection SpellCheckingInspection
@test
def prefix_lines():
    testing( s.prefix_lines( "hello\nworld", "A", "B" ) ).EQUALS( "AhelloB\nAworldB" )


# noinspection SpellCheckingInspection
@test
def regex_extract():
    testing( s.regex_extract( "abc(.+)ghi", "hello abcdefghi world" ) ).EQUALS( "def" )


@test
def remove_indent():
    testing( s.remove_indent( 4, "        hello" ) ).EQUALS( "    hello" )
    testing( s.remove_indent( 4, "  hello" ) ).EQUALS( "hello" )


@test
def remove_prefix():
    # Deprecated
    pass


@test
def rjust():
    testing( s.rjust( "lemon", 10, " " ) ).EQUALS( "     lemon" )
    testing( s.rjust( "lemons", 10, " " ) ).EQUALS( "    lemons" )
    testing( s.rjust( "lemon sherbet", 10, " " ) ).EQUALS( "lemon sherbet" )


@test
def shrink_space():
    testing( s.shrink_space( "hello   ,     world" ) ).EQUALS( "hello , world" )


@test
def special_to_symbol():
    testing( s.special_to_symbol( "hello\r\n\tworld" ) ).EQUALS( "hello␍␊␉world" )


@test
def split_strip():
    testing( s.split_strip( " hello , world", ",", -1 ) ).EQUALS( ["hello", "world"] )


@test
def string_to_bool():
    testing( s.string_to_bool( "true" ) ).EQUALS( True )
    testing( s.string_to_bool( "false" ) ).EQUALS( False )
    testing( s.string_to_bool( "TRUE" ) ).EQUALS( True )
    testing( s.string_to_bool( "FALSE" ) ).EQUALS( False )


@test
def string_to_enum():
    testing( s.string_to_enum( MyEnum, "alpha" ) ).EQUALS( MyEnum.alpha )
    testing( s.string_to_enum( MyEnum, "beta" ) ).EQUALS( MyEnum.beta )


@test
def string_to_flag():
    testing( s.string_to_flag( MyFlags, "alpha" ) ).EQUALS( MyFlags.alpha )
    testing( s.string_to_flag( MyFlags, "beta" ) ).EQUALS( MyFlags.beta )
    testing( s.string_to_flag( MyFlags, "alpha|beta" ) ).EQUALS( MyFlags.alpha | MyFlags.beta )


@test
def string_to_int():
    testing( s.string_to_int( "1" ) ).EQUALS( 1 )
    testing( s.string_to_int( "5" ) ).EQUALS( 5 )
    testing( s.string_to_int( "5.5" ) ).EQUALS( None )
    testing( s.string_to_int( "foo" ) ).EQUALS( None )
    testing( s.string_to_int( "foo", "bar" ) ).EQUALS( "bar" )


# noinspection PyTypeChecker
@test
def string_to_object():
    testing( s.string_to_object( bool, "true" ) ).EQUALS( True )
    testing( s.string_to_object( bool, "false" ) ).EQUALS( False )
    testing( s.string_to_object( bool, "TRUE" ) ).EQUALS( True )
    testing( s.string_to_object( bool, "FALSE" ) ).EQUALS( False )
    testing( s.string_to_object( int, "1" ) ).EQUALS( 1 )
    testing( s.string_to_object( int, "5" ) ).EQUALS( 5 )
    testing( s.string_to_object( MyEnum, "alpha" ) ).EQUALS( MyEnum.alpha )
    testing( s.string_to_object( MyEnum, "beta" ) ).EQUALS( MyEnum.beta )
    testing( s.string_to_object( MyFlags, "alpha" ) ).EQUALS( MyFlags.alpha )
    testing( s.string_to_object( MyFlags, "beta" ) ).EQUALS( MyFlags.beta )
    testing( s.string_to_object( MyFlags, "alpha|beta" ) ).EQUALS( MyFlags.alpha | MyFlags.beta )


# noinspection SpellCheckingInspection
@test
def StringBuilder():
    s = s.StringBuilder()
    s( "one" )
    s( "two" )( "three" )( "four" )
    s( "{}", "five" )
    testing( str( s ) ).EQUALS( "one\ntwothreefour\nfive\n" )


@test
def strip_lines():
    testing( s.strip_lines( "  hello  \n    world   " ) ).EQUALS( "hello  \nworld   " )


@test
def summarised_join():
    # Deprecated
    pass


@test
def time_now():
    # Deprecated
    pass


@test
def time_to_string():
    # Deprecated
    pass


@test
def time_to_string_short():
    # Deprecated
    pass


@test
def timedelta_to_string():
    s = lambda x: x
    m = lambda x: x * 60
    h = lambda x: x * 60 * 60
    d = lambda x: x * 60 * 60 * 24
    testing( s.timedelta_to_string( s( 5 ) ) ).EQUALS( "00:05" )
    testing( s.timedelta_to_string( m( 1 ) ) ).EQUALS( "01:00" )
    testing( s.timedelta_to_string( m( 2 ) + s( 3 ) ) ).EQUALS( "02:03" )
    testing( s.timedelta_to_string( h( 2 ) + m( 3 ) + s( 4 ) ) ).EQUALS( "2:03:04" )
    testing( s.timedelta_to_string( h( 20 ) + m( 3 ) + s( 4 ) ) ).EQUALS( "20:03:04" )
    testing( s.timedelta_to_string( d( 5 ) + h( 2 ) + m( 3 ) + s( 4 ) ) ).EQUALS( "5 days, 2:03:04" )


@test
def to_bool():
    # Deprecated
    pass


@test
def to_int():
    # Deprecated
    pass


@test
def type_name():
    testing( s.type_name( MyEnum.alpha ) ).EQUALS( "MyEnum" )
    testing( s.type_name( MyFlags.alpha ) ).EQUALS( "MyFlags" )
    testing( s.type_name( object() ) ).EQUALS( "object" )


@test
def undo_camel_case():
    testing( s.undo_camel_case( "OneTwoThree" ) ).EQUALS( "One Two Three" )


# noinspection SpellCheckingInspection
@test
def unescape():
    testing( s.unescape( "one\\ntwo\\tthree" ) ).EQUALS( "one\ntwo\tthree" )


@test
def wrap():
    testing( list( s.wrap( "hello, world", 10 ) ) ).EQUALS( ["hello,", "world"] )


class MyEnum( Enum ):
    alpha = 1
    beta = 2


class MyFlags( Flag ):
    alpha = 1
    beta = 2
