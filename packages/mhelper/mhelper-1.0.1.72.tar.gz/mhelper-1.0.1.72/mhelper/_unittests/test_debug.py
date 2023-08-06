from mhelper import debug_helper as d, ansi_format_helper


class Foo:
    """
    Documentation goes here.
    """
    pass


class Bar:
    """
    Documentation goes here.
    """
    __slots__ = "x", "y"
    
    
    def __init__( self ):
        self.x = 1
        self.y = "y"


class Baz:
    """
    Documentation goes here.
    """
    
    
    def __init__( self ):
        self.x = Foo()
        self.y = Bar()
    
    
    def baz_function( self ):
        """
        My baz function is here.
        :return: 
        """
        pass
    
    
    def another_baz_function( self ):
        pass


def my_fun( x: Bar, y: Baz = 2, z = 3 ) -> str:
    """
    Documentation goes here.
    :param x:   This is X 
    :param y:   This is Y 
    :param z:   This is Z 
    :return:    This is the return value 
    """
    return str( [x, y, z] )


ansi_format_helper.install_error_hook()

d.view( 1 )
d.view( Foo() )
d.view( Foo )
d.view( Bar() )
d.view( Baz() )
d.view( Baz )
d.view( my_fun )
d.view( None )

if not input( "did the test pass? " ).lower().startswith( "y" ):
    raise RuntimeError( "test failed or no input provided" )
