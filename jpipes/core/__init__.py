"""JPipes core exceptions module."""

class JPipesError(Exception):
    """Generic errors."""
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg
    
    def __str__(self):
        return self.msg

            
class JPipesConfigError(JPipesError):
    pass

class JPipesRuntimeError(JPipesError):
    pass
        
class JPipesArgumentError(JPipesError):
    pass

class JPipesInterfaceError(JPipesError):
    pass