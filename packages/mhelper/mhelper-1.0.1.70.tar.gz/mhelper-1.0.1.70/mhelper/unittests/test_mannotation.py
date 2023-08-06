from typing import Generic, TypeVar, List, Optional, Sequence, Tuple, Union

from ._test_base import test, testing
from mhelper import mannotation as ma


T = TypeVar( "T" )
U = TypeVar( "U" )


class MyMannotation( ma.MAnnotation ):
    pass


class MyGeneric( Generic[T, U] ):
    pass


class MyGenericInst( MyGeneric[int, bool] ):
    pass


class MyGeneric2( Generic[T] ):
    pass


class MyGenericInst2( MyGeneric2[int] ):
    pass


class MyOtherGeneric( Generic[T, U] ):
    pass


class MyOtherGenericInst( MyOtherGeneric[int, bool] ):
    pass


class MyAlpha:
    pass


class MyBeta( MyAlpha ):
    pass


class MyGamma( MyBeta ):
    pass


class MyDelta( MyGamma ):
    pass


class MyEpsilon( MyDelta ):
    pass


@test
def is_derived_from():
    x = MyMannotation( int, "hello" )
    y = x["world"]
    z = MyMannotation( int, "spam" )
    testing( y.is_derived_from( x ) ).EQUALS( True )
    testing( z.is_derived_from( x ) ).EQUALS( False )


@test
def predefined():
    def spam( a: ma.isOptionList = None,
              b: ma.isFilename = None,
              c: ma.isDirname = None,
              d: ma.isOptional = None,
              e: ma.isUnion = None,
              f: ma.isReadonly = None,
              g: ma.isPassword = None ):
        _ = a, b, c, d, e, f, g
    
    
    spam()


@test
def generic_arg():
    testing( lambda: ma.AnnotationInspector( MyGenericInst ).generic_arg ).ERRORS()
    testing( ma.AnnotationInspector( MyGenericInst2 ).generic_arg ).EQUALS( int )


@test
def generic_args():
    x = ma.AnnotationInspector( MyGenericInst )
    testing( x.generic_args ).EQUALS( (int, bool) )


# noinspection PyDeprecation
@test
def generic_list_type():
    testing( ma.AnnotationInspector( List[int] ).generic_list_type ).EQUALS( int )


@test
def get_direct_subclass():
    testing( ma.AnnotationInspector( MyBeta ).get_direct_subclass( MyAlpha ) ).EQUALS( MyBeta )


@test
def get_direct_superclass():
    testing( ma.AnnotationInspector( MyBeta ).get_direct_superclass( MyGamma ) ).EQUALS( MyBeta )


@test
def get_indirect_subclass():
    testing( ma.AnnotationInspector( MyEpsilon ).get_indirect_subclass( MyBeta ) ).EQUALS( MyEpsilon )


@test
def get_indirect_superclass():
    testing( ma.AnnotationInspector( MyEpsilon ).get_indirect_subclass( MyGamma ) ).EQUALS( MyEpsilon )


@test
def get_type_name():
    testing( ma.AnnotationInspector.get_type_name( MyEpsilon ) ).EQUALS( "MyEpsilon" )


@test
def is_direct_subclass_of():
    testing( ma.AnnotationInspector( MyEpsilon ).is_direct_subclass_of( MyBeta ) ).EQUALS( True )


@test
def is_direct_subclass_of_or_optional():
    testing( ma.AnnotationInspector( MyEpsilon ).is_direct_subclass_of_or_optional( MyBeta ) ).EQUALS( True )
    testing( ma.AnnotationInspector( Optional[MyEpsilon] ).is_direct_subclass_of_or_optional( MyBeta ) ).EQUALS( True )
    testing( ma.AnnotationInspector( ma.isOptional[MyEpsilon] ).is_direct_subclass_of_or_optional( MyBeta ) ).EQUALS( True )


@test
def is_direct_superclass_of():
    testing( ma.AnnotationInspector( MyGamma ).is_direct_superclass_of( MyEpsilon ) ).EQUALS( True )
    testing( ma.AnnotationInspector( Optional[MyGamma] ).is_direct_superclass_of( MyEpsilon ) ).EQUALS( False )
    testing( ma.AnnotationInspector( ma.isOptional[MyGamma] ).is_direct_superclass_of( MyEpsilon ) ).EQUALS( False )


@test
def is_generic():
    testing( ma.AnnotationInspector( MyGeneric ).is_generic ).EQUALS( True )
    testing( ma.AnnotationInspector( MyGenericInst ).is_generic ).EQUALS( True )
    testing( ma.AnnotationInspector( MyAlpha ).is_generic ).EQUALS( False )


# noinspection PyDeprecation
@test
def is_generic_list():
    testing( ma.AnnotationInspector( MyGeneric ).is_generic_list ).EQUALS( False )
    testing( ma.AnnotationInspector( list ).is_generic_list ).EQUALS( False )
    testing( ma.AnnotationInspector( tuple ).is_generic_list ).EQUALS( False )
    testing( ma.AnnotationInspector( List[str] ).is_generic_list ).EQUALS( True )
    testing( ma.AnnotationInspector( Sequence[str] ).is_generic_list ).EQUALS( False )
    testing( ma.AnnotationInspector( Tuple[str, ...] ).is_generic_list ).EQUALS( False )


# noinspection PyDeprecation
@test
def is_generic_sequence():
    testing( ma.AnnotationInspector( MyGeneric ).is_generic_sequence ).EQUALS( False )
    testing( ma.AnnotationInspector( list ).is_generic_sequence ).EQUALS( False )
    testing( ma.AnnotationInspector( tuple ).is_generic_sequence ).EQUALS( False )
    testing( ma.AnnotationInspector( List[str] ).is_generic_sequence ).EQUALS( False )
    testing( ma.AnnotationInspector( Sequence[str] ).is_generic_sequence ).EQUALS( True )
    testing( ma.AnnotationInspector( Tuple[str, ...] ).is_generic_sequence ).EQUALS( False )


@test
def is_generic_u_of_t():
    testing( ma.AnnotationInspector( MyGenericInst ).is_generic_u_of_t( MyGeneric ) ).EQUALS( True )
    testing( ma.AnnotationInspector( MyGenericInst ).is_generic_u_of_t( MyOtherGeneric ) ).EQUALS( False )


@test
def is_indirect_subclass_of():
    testing( ma.AnnotationInspector( MyDelta ).is_indirect_subclass_of( MyAlpha ) ).EQUALS( True )
    testing( ma.AnnotationInspector( Optional[MyDelta] ).is_indirect_subclass_of( MyAlpha ) ).EQUALS( True )
    testing( ma.AnnotationInspector( Union[str, MyDelta] ).is_indirect_subclass_of( MyAlpha ) ).EQUALS( True )
    testing( ma.AnnotationInspector( MyDelta ).is_indirect_subclass_of( MyEpsilon ) ).EQUALS( False )
    testing( ma.AnnotationInspector( Optional[MyDelta] ).is_indirect_subclass_of( MyEpsilon ) ).EQUALS( False )
    testing( ma.AnnotationInspector( Union[str, MyDelta] ).is_indirect_subclass_of( MyEpsilon ) ).EQUALS( False )
    testing( ma.AnnotationInspector( Union[str, MyDelta] ).is_indirect_subclass_of( int ) ).EQUALS( False )


@test
def is_indirectly_superclass_of():
    testing( ma.AnnotationInspector( MyDelta ).is_indirectly_superclass_of( MyAlpha ) ).EQUALS( False )
    testing( ma.AnnotationInspector( Optional[MyDelta] ).is_indirectly_superclass_of( MyAlpha ) ).EQUALS( False )
    testing( ma.AnnotationInspector( Union[str, MyDelta] ).is_indirectly_superclass_of( MyAlpha ) ).EQUALS( False )
    testing( ma.AnnotationInspector( MyDelta ).is_indirectly_superclass_of( MyEpsilon ) ).EQUALS( True )
    testing( ma.AnnotationInspector( Optional[MyDelta] ).is_indirectly_superclass_of( MyEpsilon ) ).EQUALS( True )
    testing( ma.AnnotationInspector( Union[str, MyDelta] ).is_indirectly_superclass_of( MyEpsilon ) ).EQUALS( True )
    testing( ma.AnnotationInspector( Union[str, MyDelta] ).is_indirectly_superclass_of( int ) ).EQUALS( False )


# noinspection PyDeprecation
@test
def is_mannotation():
    testing( ma.AnnotationInspector( MyDelta ).is_mannotation ).EQUALS( False )
    testing( ma.AnnotationInspector( str ).is_mannotation ).EQUALS( False )
    testing( ma.AnnotationInspector( ma.isFilename ).is_mannotation ).EQUALS( True )
    testing( ma.AnnotationInspector( ma.isFilename[".csv", "R"] ).is_mannotation ).EQUALS( True )
    testing( ma.AnnotationInspector( ma.MAnnotation( "foo" ) ).is_mannotation ).EQUALS( True )


# noinspection PyDeprecation
@test
def is_mannotation_of():
    testing( ma.AnnotationInspector( MyDelta ).is_mannotation_of( ma.isFilename ) ).EQUALS( False )
    testing( ma.AnnotationInspector( str ).is_mannotation_of( ma.isFilename ) ).EQUALS( False )
    testing( ma.AnnotationInspector( ma.isFilename ).is_mannotation_of( ma.isFilename ) ).EQUALS( True )
    testing( ma.AnnotationInspector( ma.isFilename[".csv", "R"] ).is_mannotation_of( ma.isFilename ) ).EQUALS( True )
    testing( ma.AnnotationInspector( ma.MAnnotation( "foo" ) ).is_mannotation_of( ma.isFilename ) ).EQUALS( False )


@test
def is_multi_optional():
    testing( ma.AnnotationInspector( Optional[Union[str, int]] ).is_multi_optional ).EQUALS( True )
    testing( ma.AnnotationInspector( Union[str, int, None] ).is_multi_optional ).EQUALS( True )
    testing( ma.AnnotationInspector( Union[str, int] ).is_multi_optional ).EQUALS( False )
    testing( ma.AnnotationInspector( None ).is_multi_optional ).EQUALS( False )
    testing( ma.AnnotationInspector( str ).is_multi_optional ).EQUALS( False )


@test
def is_optional():
    testing( ma.AnnotationInspector( Optional[str] ).is_optional ).EQUALS( True )
    testing( ma.AnnotationInspector( Optional[Union[str, int]] ).is_optional ).EQUALS( False )
    testing( ma.AnnotationInspector( Union[str, int, None] ).is_optional ).EQUALS( False )
    testing( ma.AnnotationInspector( Union[str, int] ).is_optional ).EQUALS( False )
    testing( ma.AnnotationInspector( None ).is_optional ).EQUALS( False )
    testing( ma.AnnotationInspector( str ).is_optional ).EQUALS( False )


@test
def is_type():
    testing( ma.AnnotationInspector( Optional[Union[str, int]] ).is_type ).EQUALS( False )
    testing( ma.AnnotationInspector( Union[str, int, None] ).is_type ).EQUALS( False )
    testing( ma.AnnotationInspector( Union[str, int] ).is_type ).EQUALS( False )
    testing( ma.AnnotationInspector( List[str] ).is_type ).EQUALS( False )
    testing( ma.AnnotationInspector( None ).is_type ).EQUALS( False )
    testing( ma.AnnotationInspector( ma.isFilename ).is_type ).EQUALS( False )
    testing( ma.AnnotationInspector( str ).is_type ).EQUALS( True )


@test
def is_union():
    testing( ma.AnnotationInspector( Optional[str] ).is_union ).IS_TRUE()
    testing( ma.AnnotationInspector( Optional[Union[str, int]] ).is_union ).IS_TRUE()
    testing( ma.AnnotationInspector( Union[str, int, None] ).is_union ).IS_TRUE()
    testing( ma.AnnotationInspector( Union[str, int] ).is_union ).IS_TRUE()
    testing( ma.AnnotationInspector( ma.isUnion[str, int, None] ).is_union ).IS_TRUE()
    testing( ma.AnnotationInspector( ma.isUnion[str, int] ).is_union ).IS_TRUE()
    testing( ma.AnnotationInspector( ma.isOptional[str] ).is_union ).IS_TRUE()
    testing( ma.AnnotationInspector( None ).is_union ).IS_FALSE()
    testing( ma.AnnotationInspector( str ).is_union ).IS_FALSE()


@test
def is_viable_instance():
    testing( ma.AnnotationInspector( MyDelta ).is_viable_instance( MyAlpha() ) ).EQUALS( False )
    testing( ma.AnnotationInspector( Optional[MyDelta] ).is_viable_instance( MyAlpha() ) ).EQUALS( False )
    testing( ma.AnnotationInspector( Union[str, MyDelta] ).is_viable_instance( MyAlpha() ) ).EQUALS( False )
    testing( ma.AnnotationInspector( MyDelta ).is_viable_instance( MyEpsilon() ) ).EQUALS( True )
    testing( ma.AnnotationInspector( Optional[MyDelta] ).is_viable_instance( MyEpsilon() ) ).EQUALS( True )
    testing( ma.AnnotationInspector( Union[str, MyDelta] ).is_viable_instance( MyEpsilon() ) ).EQUALS( True )
    testing( ma.AnnotationInspector( Union[str, MyDelta] ).is_viable_instance( 5 ) ).EQUALS( False )


# noinspection PyDeprecation
@test
def mannotation():
    testing( ma.AnnotationInspector( ma.isFilename["foo", "R"] ).mannotation ).IS_INSTANCE( ma.MAnnotation )


# noinspection PyDeprecation
@test
def mannotation_arg():
    testing( ma.AnnotationInspector( ma.isFilename["foo", "R"] ).mannotation_arg ).EQUALS( str )


# noinspection PyDeprecation
@test
def name():
    testing( ma.AnnotationInspector( int ).name ).EQUALS( "int" )


# noinspection PyDeprecation
@test
def optional_types():
    testing( ma.AnnotationInspector( Optional[str] ).optional_types ).EQUALS( [str] )
    testing( ma.AnnotationInspector( Optional[Union[str, int]] ).optional_types ).EQUALS( [str, int] )
    testing( ma.AnnotationInspector( Union[str, int, None] ).optional_types ).EQUALS( [str, int] )
    testing( lambda: ma.AnnotationInspector( Union[str, int] ).optional_types ).ERRORS()
    testing( ma.AnnotationInspector( ma.isUnion[str, int, None] ).optional_types ).EQUALS( [str, int] )
    testing( lambda: ma.AnnotationInspector( ma.isUnion[str, int] ).optional_types ).ERRORS()
    testing( lambda: ma.AnnotationInspector( None ).optional_types ).ERRORS()
    testing( lambda: ma.AnnotationInspector( str ).optional_types ).ERRORS()


# noinspection PyDeprecation
@test
def optional_value():
    testing( ma.AnnotationInspector( Optional[str] ).optional_value ).EQUALS( str )
    testing( ma.AnnotationInspector( ma.isOptional[str] ).optional_value ).EQUALS( str )
    testing( lambda: ma.AnnotationInspector( Optional[Union[str, int]] ).optional_value ).ERRORS()
    testing( lambda: ma.AnnotationInspector( Union[str, int, None] ).optional_value ).ERRORS()
    testing( lambda: ma.AnnotationInspector( Union[str, int] ).optional_value ).ERRORS()
    testing( lambda: ma.AnnotationInspector( ma.isUnion[str, int, None] ).optional_value ).ERRORS()
    testing( lambda: ma.AnnotationInspector( ma.isUnion[str, int] ).optional_value ).ERRORS()
    testing( lambda: ma.AnnotationInspector( None ).optional_value ).ERRORS()
    testing( lambda: ma.AnnotationInspector( str ).optional_value ).ERRORS()


# noinspection PyDeprecation
@test
def safe_type():
    testing( ma.AnnotationInspector( str ).safe_type ).EQUALS( str )
    testing( ma.AnnotationInspector( Optional[str] ).safe_type ).EQUALS( None )
    testing( ma.AnnotationInspector( 5 ).safe_type ).EQUALS( None )


# noinspection PyDeprecation
@test
def union_args():
    testing( ma.AnnotationInspector( Optional[str] ).union_args ).SET_EQUALS( [str, type( None )] )
    testing( ma.AnnotationInspector( Optional[Union[str, int]] ).union_args ).SET_EQUALS( [str, int, type( None )] )
    testing( ma.AnnotationInspector( Union[str, int, None] ).union_args ).SET_EQUALS( [str, int, type( None )] )
    testing( ma.AnnotationInspector( Union[str, int] ).union_args ).SET_EQUALS( [str, int] )
    testing( ma.AnnotationInspector( ma.isUnion[str, int, None] ).union_args ).SET_EQUALS( [str, int, None] )
    testing( ma.AnnotationInspector( ma.isUnion[str, int] ).union_args ).SET_EQUALS( [str, int] )
    testing( lambda: ma.AnnotationInspector( None ).union_args ).ERRORS()
    testing( lambda: ma.AnnotationInspector( str ).union_args ).ERRORS()


@test
def value_or_optional_value():
    testing( ma.AnnotationInspector( Optional[str] ).value_or_optional_value ).EQUALS( str )
    testing( ma.AnnotationInspector( str ).value_or_optional_value ).EQUALS( str )
