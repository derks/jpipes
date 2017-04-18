"""Jpipes exception classes."""

class JPipesError(Exception):
    """Generic errors."""
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg
    
    def __str__(self):
        return self.msg

class JPipesConfigError(JPipesError):
    """Config related errors."""
    pass

class JPipesRuntimeError(JPipesError):
    """Generic runtime errors."""
    pass
        
class JPipesArgumentError(JPipesError):
    """Argument related errors."""
    pass
