from collections import abc
from typing import Tuple, cast, List, Optional, Union, Callable, Generic, Sequence

from mhelper.mannotation.classes import MAnnotation
from mhelper.mannotation.predefined import isUnion, isOptional

import warnings


GAlias = type( List )
NoneType = type( None )


# noinspection PyUnresolvedReferences,PyTypeHints,PyTypeChecker
class AnnotationInspector:
    """
    Class to inspect PEP-484 annotations: handles GenericAliases (`Union`,
    `List`, `Tuple`, `Optional`), Generics (`Generic`) and custom
    (`MAnnotation`) annotations.
    """
    
    
    def __init__( self, annotation: object ):
        """
        Construct a class to inspect a particular annotation.
        """
        if isinstance( annotation, AnnotationInspector ):
            raise TypeError( "Encompassing an `AnnotationInspector` within an `AnnotationInspector` is probably an error." )
        
        self.value = annotation
    
    
    def _get_generic_info( self ):
        """
        This is the workhorse of this class.
        
        It should return a tuple of the type and its args.

        =================== =========================== ========================
        Input               Output I                    Output II
        =================== =========================== ========================
        typing.Union        `typing.Union`              Union arguments
        typing.List         `list`                      List arguments
        typing.Tuple        `tuple`                     Tuple arguments
        typing.Sequence     `collections.abc.Sequence`  Sequence arguments
        MAnnotation         `MAnnotation`               MAnnotation arguments
        Generic-base        The `Generic`-derived base  Generic arguments
        (anything else)     `None`                      `None`
        =================== =========================== ========================
        """
        if isinstance( self.value, GAlias ):
            # Union, List, etc.
            return self.value.__origin__, self.value.__args__
        elif isinstance( self.value, type ) and issubclass( self.value, Generic ):
            # Custom generics
            try:
                # Python 3.7 Custom Generics
                ob = getattr( self.value, "__orig_bases__" )[0]
            except Exception:
                # Python 3.6 All + Python 3.7 "GenericAlias" 
                ob = self.value
            
            return ob.__origin__, ob.__args__
        elif isinstance( self.value, MAnnotation ):
            return MAnnotation, self.value.parameters
        else:
            return None, None
    
    
    @property
    def is_generic( self ):
        """
        Determines whether the underlying annotation is some sort of generic the
        `AnnotationInspector` can handle.
        """
        c, a = self._get_generic_info()
        return c is not None
    
    
    def is_generic_u( self, u: type ) -> bool:
        """
        Determines whether the underlying annotation is some sort of generic the
        `AnnotationInspector` can handle, and if that generic is of the
        specified type `u`.
        
        * For Generic, `u` should be the generic base class. 
        * For MAnnotation, `u` should be the base annotation.
        * For GenericAlias, `u` should be either the bound type (`list`,
            `tuple`, `Union`, abc.Sequence) or any instance of the alias (`List`
            `List[int]`, etc.).
        """
        c, a = self._get_generic_info()
        
        if c is MAnnotation and isinstance( u, MAnnotation ):
            return self.value.is_derived_from( u )
        else:
            u = getattr( u, "__origin__", u )
            return bool( u == c )
    
    
    def is_generic_u_of_t( self, u: type ) -> bool:
        """
        Determines whether the underlying annotation is some sort of generic the
        `AnnotationInspector` can handle, and if that generic is of the
        specified type `u`, and if that generic has at least one argument passed.
        
        E.g. Like `is_generic_u` this will return `True` for `List[int]` but
        unlike `is_generic_u` it will return `False` for a plain `List`.
        """
        return bool( self.is_generic_u( u ) and self.generic_args )
    
    
    @property
    def generic_args( self ) -> Tuple[object, ...]:
        """
        If the underlying annotation `is_generic`, returns the generic
        arguments, otherwise, raises a `TypeError`.
        """
        return self.get_generic_args()
    
    
    @property
    def generic_arg( self ) -> object:
        """
        Returns the first of the `generic_args`.
        """
        r = self.get_generic_args()
        return self._first( r )
    
    
    def get_generic_args( self, filter_none = False, filter_name = False ) -> Sequence[object]:
        c, a = self._get_generic_info()
        
        if c is None:
            raise TypeError( "Cannot get `generic_args` because this annotation, «{}» is not a generic.".format( self ) )
        
        if filter_name and len( a ) > 0 and isinstance( a[0], str ):
            a = a[1:]
        
        if filter_none:
            return tuple( x for x in a if x is not None and x is not NoneType and x is not "isOptional" )
        else:
            return a
    
    
    def get_generic_arg( self, *args, **kwargs ) -> Sequence[object]:
        r = self.get_generic_args( *args, **kwargs )
        return self._first( r )
    
    
    def is_direct_subclass_of( self, super_class: type ) -> bool:
        """
        As `get_direct_subclass` but returns `True`/`False` instead of `type`/`None`.
        """
        # If BASE and/or DERIVED is not a type then we count only direct equality
        if self.value is super_class:
            return True
        
        if not self.is_type:
            return False
        
        super_inspector = AnnotationInspector( super_class )
        
        if not super_inspector.is_type:
            return False
        
        if super_inspector.is_generic_u( list ):
            super_inspector = AnnotationInspector( list )
        
        if super_inspector.is_union:
            return any( self.is_direct_subclass_of( x ) for x in super_inspector.generic_args )
        else:
            try:
                return issubclass( cast( type, self.value ), super_inspector.value )
            except TypeError as ex:
                raise TypeError( "Cannot determine if «{}» is derived from «{}» because `issubclass({}, {})` returned an error.".format( self, super_class, self, super_class ) ) from ex
    
    
    def is_direct_superclass_of( self, sub_class: type ) -> bool:
        """
        As `get_direct_superclass` but returns `True`/`False` instead of `type`/`None`.
        """
        if not self.is_type:
            return False
        
        if self.is_generic_u( list ):
            # Special case for List[T]
            return issubclass( sub_class, list )
        
        try:
            return issubclass( sub_class, cast( type, self.value ) )
        except TypeError as ex:
            raise TypeError( "Cannot determine if «{}» is a base class of «{}» because `issubclass({}, {})` returned an error.".format( self, sub_class, sub_class, self ) ) from ex
    
    
    def is_direct_subclass_of_or_optional( self, super_class: type ):
        """
        As `is_direct_subclass_of` but unwraps any optional annotation first.
        """
        if self.is_optional:
            arg = self.get_generic_arg( filter_none = True, filter_name = True )
            return AnnotationInspector( arg ).is_direct_subclass_of( super_class )
        else:
            return self.is_direct_subclass_of( super_class )
    
    
    def get_direct_subclass( self, super_class: type ) -> Optional[type]:
        """
        Checks if this annotation is derived from a `super_class`.
        
        :return: The type of the annotation is returned if this is the case,
                 otherwise `None`.
        """
        if self.is_direct_subclass_of( super_class ):
            return cast( type, self.value )
    
    
    def get_direct_superclass( self, lower_class: type ) -> Optional[type]:
        """
        The counterpart of `get_direct_subclass`, checking if this
        `lower_class` is derived from this annotation..
        """
        if self.is_direct_superclass_of( lower_class ):
            return cast( type, self.value )
    
    
    def is_indirect_subclass_of( self, super_class: type ) -> bool:
        """
        As `get_indirect_subclass` but returns `True`/`False` instead of `type`/`None`. 
        """
        return self.get_indirect_subclass( super_class ) is not None
    
    
    def is_indirectly_superclass_of( self, sub_class: type ) -> bool:
        """
        As `get_indirect_superclass` but returns `True`/`False` instead of `type`/`None`.
        """
        return self.get_indirect_superclass( sub_class ) is not None
    
    
    def get_indirect_superclass( self, sub_class: type ) -> Optional[type]:
        """
        As `get_direct_superclass`, but also checks annotations within the
        annotation (such as `Union`, `Optional`, or `MAnnotation`s with a
        concrete-type such as `isFileName` (`str`)).
        """
        return self.__get_indirectly( sub_class, AnnotationInspector.is_direct_superclass_of )
    
    
    def get_indirect_subclass( self, super_class: type ) -> Optional[type]:
        """
        As `get_direct_subclass`, but also checks annotations within the the
        annotation (such as `Union`, `Optional`, or `MAnnotation`s with
        a concrete-type such as `isFileName` (`str`)).
        """
        return self.__get_indirectly( super_class, AnnotationInspector.is_direct_subclass_of )
    
    
    def __get_indirectly( self, query: type, predicate: "Callable[[AnnotationInspector, type],bool]" ) -> Optional[object]:
        """
        Checks inside all `Unions` and `MAnnotations` until the predicate matches, returning the
        type (`self.value`) when it does.
        """
        if predicate( self, query ):
            return self.value
        
        if self.is_union:
            for arg in self.generic_args:
                if isinstance( arg, type ) and arg is not NoneType:
                    arg_type = AnnotationInspector( arg ).__get_indirectly( query, predicate )
                    
                    if arg_type is not None:
                        return arg_type
        
        if self.is_generic_u_of_t( MAnnotation ):
            for arg in self.generic_args:
                if isinstance( arg, type ) and arg is not NoneType:
                    annotation_type = AnnotationInspector( arg ).__get_indirectly( query, predicate )
                    
                    if annotation_type is not None:
                        return annotation_type
        
        return None
    
    
    @classmethod
    def get_type_name( cls, annotation: object ) -> str:
        """
        Gets a descriptive name of an annotation.
        """
        return str( cls( annotation ) )
    
    
    def __str__( self ) -> str:
        """
        Gets a descriptive name for the underlying annotation.
        """
        if isinstance( self.value, type ):
            result = self.value.__name__
        elif isinstance( self.value, MAnnotation ):
            result = str( self.value )
        else:
            result = str( self.value )
        
        return result
    
    
    def __repr__( self ):
        """
        !OVERRIDE
        """
        cls = type( self ).__name__
        if isinstance( self.value, type ):
            return "{}(type={})".format( cls, repr( self.value.__name__ ) )
        elif isinstance( self.value, MAnnotation ):
            return "{}(man={})".format( cls, repr( self.value ) )
        elif isinstance( self.value, GAlias ):
            return "{}(alias={})".format( cls, repr( self.value ) )
        else:
            return "{}(unknown={})".format( cls, repr( self.value ) )
    
    
    @property
    def is_union( self ) -> bool:
        """
        Determines if this is anything union-like.
        
        `Union[str, int]`   --> True
        `Optional[str]`     --> True
        `isUnion[str, int]` --> True
        `isOptional[str]`   --> True
        `str`               --> False
        """
        return (self.is_generic_u_of_t( Union )
                or self.is_generic_u_of_t( isUnion )
                or self.is_generic_u_of_t( isOptional ))
    
    
    @property
    def is_optional( self ) -> bool:
        """
        Returns if this is an "optional"-type annotation with a *single* option.
        
        * `Optional[T]`         --> `True`
        * `isOptional[T]`       --> `True`
        * `Union[T, None]`      --> `True`
        * `Union[T, U, None]`   --> `False`
        * `Union[T]`            --> `False`
        * `Union[T, U]`         --> `False`
        * `T`                   --> `False`
        """
        if self.is_generic_u_of_t( isOptional ):
            return True
        
        if not self.is_union:
            return False
        
        a = self.generic_args
        
        if len( a ) == 2 and (NoneType in a or None in a):
            return True
        
        return False
    
    
    @property
    def is_multi_optional( self ) -> bool:
        """
        Returns if this is an "optional"-type annotation.
        
        * `Optional[T]`         --> `True`
        * `isOptional[T]`       --> `True`
        * `Union[T, None]`      --> `True`
        * `Union[T, U, None]`   --> `True`
        * `Union[T]`            --> `False`
        * `Union[T, U]`         --> `False`
        * `T`                   --> `False`
        """
        if self.is_generic_u_of_t( isOptional ):
            return True
        
        if not self.is_union:
            return False
        
        a = self.generic_args
        
        # Python 3.6 + MAnnotation uses None, Python 3.7 uses NoneType
        if None in a or NoneType in a:
            return True
        
        return False
    
    
    @property
    def value_or_optional_value( self ) -> Optional[object]:
        """
        If this annotation is an optional specifying a single type, obtain that
        type, otherwise, just obtain the annotation verbatim.
        
        * `Optional[T]`     --> `T`
        * `isOptional[T]`   --> `T`
        * `Union[T, None]`  --> `T`
        * `X`               --> `X`
            * Where X is anything else, including `Union[T, U, None]`.
        """
        if self.is_optional:
            return self.get_generic_arg( filter_none = True )
        else:
            return self.value
    
    
    @property
    def is_type( self ):
        """
        Returns if my `type` is an actual `type`, not an annotation object like `Union`.
        """
        return isinstance( self.value, type )
    
    
    def is_viable_instance( self, value ):
        """
        Returns `is_viable_subclass` on the value's type.
        """
        if value is None and self.is_multi_optional:
            return True
        
        return self.is_indirectly_superclass_of( type( value ) )
    
    
    # region Deprecated
    
    @property
    def is_mannotation( self ):
        warnings.warn( "Deprecated - use is_generic_u", DeprecationWarning )
        return self.is_generic_u( MAnnotation )
    
    
    def is_mannotation_of( self, parent: MAnnotation ):
        warnings.warn( "Deprecated - use is_generic_u", DeprecationWarning )
        return self.is_generic_u( parent )
    
    
    @property
    def mannotation( self ) -> MAnnotation:
        warnings.warn( "Deprecated - use is_generic_u", DeprecationWarning )
        return self.value if self.is_generic_u( MAnnotation ) else None
    
    
    @property
    def mannotation_arg( self ):
        """
        If this is an instance of `MAnnotation`, return the underlying argument
        #1 (typically the type), otherwise, raise a `TypeError`. If this is an
        `MAnnotation`, but has no arguments, returns `None`.
        """
        warnings.warn( "Deprecated - use generic_args", DeprecationWarning )
        
        if not self.is_generic_u( MAnnotation ):
            raise TypeError( "«{}» is not an MAnnotation[T].".format( self ) )
        
        c, a = self._get_generic_info()
        
        if len( a ) >= 2:
            return a[1]
        else:
            return None
    
    
    @property
    def is_generic_list( self ) -> bool:
        warnings.warn( "Deprecated - use is_generic_u_of_t", DeprecationWarning )
        return self.is_generic_u_of_t( list )
    
    
    @property
    def is_generic_sequence( self ) -> bool:
        warnings.warn( "Deprecated - use is_generic_u_of_t", DeprecationWarning )
        return self.is_generic_u_of_t( abc.Sequence )
    
    
    @property
    def generic_list_type( self ) -> type:
        """
        Gets the T in List[T]. Otherwise raises `TypeError`.
        """
        warnings.warn( "Deprecated - use generic_arg", DeprecationWarning )
        
        if not self.is_generic_u_of_t( list ):
            raise TypeError( "«{}» is not a List[T].".format( self ) )
        
        c, a = self._get_generic_info()
        
        return a[0]
    
    
    # noinspection PyDeprecation
    @property
    def union_args( self ) -> List[type]:
        """
        If this is a "union"-type annotation, returns the option list.
        If this is not a "union"-type, return an error.
        
        * `Optional[T]`         --> `[T, NoneType]`
        * `isOptional[T]`       --> *Error*
        * `Union[T, None]`      --> `[T, NoneType]`
        * `Union[T, U, None]`   --> `[T, U, NoneType]`
        * `Union[T]`            --> `[T]`
        * `Union[T, U]`         --> `[T, U]`
        * `isUnion[T, None]`    --> `[T, NoneType]`
        * `isUnion[T, U, None]` --> `[T, U, NoneType]`
        * `isUnion[T]`          --> `[T]`
        * `isUnion[T, U]`       --> `[T, U]`
        * `T`                   --> *Error*
        """
        warnings.warn( "Deprecated - use generic_args", DeprecationWarning )
        
        if not self.is_union:
            raise TypeError( "«{}» is not a Union[T].".format( self ) )
        
        if self.is_mannotation_of( isUnion ):
            return self.value.parameters[1:]  # "1:" = skip name
        elif self.is_mannotation_of( isOptional ):
            return [self.mannotation_arg]
        else:
            return self.value.__args__
    
    
    @property
    def optional_types( self ) -> List[type]:
        """
        If this annotation is an optional, obtain the option list, otherwise,
        raise a `TypeError`.
        
        * `Optional[T]`         --> `[T]`
        * `isOptional[T]`       --> `[T]`
        * `Union[T, None]`      --> `[T]`
        * `Union[T, U, None]`   --> `[T, U]`
        """
        warnings.warn( "Deprecated - use generic_args", DeprecationWarning )
        
        if self.is_mannotation_of( isOptional ):
            return [self.mannotation_arg]
        
        if not self.is_union:
            raise TypeError( "«{}» is not a Union[T].".format( self ) )
        
        union_params = list( self.union_args )
        
        if type( None ) in union_params:
            union_params.remove( type( None ) )
        elif None in union_params:
            union_params.remove( None )
        else:
            raise TypeError( "«{}» is not a Union[...] with `None` in `...`.".format( self ) )
        
        return union_params
    
    
    # noinspection PyDeprecation
    @property
    def optional_value( self ) -> Optional[object]:
        """
        If this annotation is an optional specifying a single type, obtain that
        type, otherwise, just raise a `TypeError`.
        
        * `Optional[T]`     --> `T`
        * `isOptional[T]`   --> `T`
        * `Union[T, None]`  --> `T`
        * `X`               --> `X`
            * Where X is anything else, including `Union[T, U, None]`.
        """
        warnings.warn( "Deprecated - use generic_arg", DeprecationWarning )
        
        t = self.optional_types
        
        if len( t ) == 1:
            return t[0]
        else:
            raise TypeError( "«{}» is not a Union[T, None] (i.e. an Optional[T]).".format( self ) )
    
    
    @property
    def safe_type( self ) -> Optional[type]:
        """
        If this is a `T`, returns `T`, else returns `None`.
        """
        warnings.warn( "Deprecated - use is_type", DeprecationWarning )
        
        if self.is_type:
            assert isinstance( self.value, type )
            return self.value
        else:
            return None
    
    
    @property
    def name( self ):
        """
        Returns the type name
        """
        warnings.warn( "Deprecated - use type.__name__ or str", DeprecationWarning )
        
        if not self.is_type:
            raise TypeError( "«{}» is not a <type>.".format( self ) )
        
        return self.value.__name__
    # endregion


    def _first( self, x ):
        if len( x ) != 1:
            raise ValueError( "When trying to parse {}, I expected 1 value in list, but got {} arguments: {}".format( self, len( x ), repr( x ) ) )
        else:
            return x[0]
