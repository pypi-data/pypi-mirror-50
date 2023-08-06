"""
Deprecated - use debug_helper.
"""
import warnings


warnings.warn( "Deprecated - use debug_helper", DeprecationWarning )


def add_display_hook():
    warnings.warn( "Deprecated - use debug_helper.set_display_hook", DeprecationWarning )
    from mhelper import debug_helper
    debug_helper.set_display_hook()
