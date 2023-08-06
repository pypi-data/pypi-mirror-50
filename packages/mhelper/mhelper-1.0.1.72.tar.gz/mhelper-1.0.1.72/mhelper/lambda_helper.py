"""
Provides classes with lambda based dunders. 
"""

class DynamicStr:
    def __init__( self, fn ):
        self.fn = fn
    
    
    def __str__( self ):
        return self.fn()


class DynamicBool:
    def __init__( self, fn ):
        self.fn = fn
    
    
    def __bool__( self ):
        return self.fn()
