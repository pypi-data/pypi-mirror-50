"""
Deprecated - use property_helper
"""
import warnings


def coalesce( value, default_ ):
    """
    Deprecated - use property_helper
    """
    warnings.warn( "Deprecated - use property_helper", DeprecationWarning )
    
    if value is None:
        return default_
    else:
        return value
