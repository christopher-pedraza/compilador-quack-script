class InterpreterError(Exception):
    """Base class for all interpreter-related errors."""
    pass

# Redeclaration Errors
class SymbolRedeclarationError(InterpreterError):
    """Raised when a symbol is redeclared in the same scope."""
    pass
class ParameterRedeclarationError(SymbolRedeclarationError):
    """Raised when a function parameter is redeclared."""
    pass
class ContainerRedeclarationError(SymbolRedeclarationError):
    """Raised when a container (e.g., function, module) is redeclared."""
    pass

# Type Mismatch Errors
class TypeMismatchError(InterpreterError):
    """Raised when there is a type mismatch during assignment or operation."""
    pass

# Operation Errors
class UnsupportedOperationError(InterpreterError):
    """Raised when an operation is not supported between given types."""
    pass
class UnsupportedExpressionError(InterpreterError):
    """Raised when an expression is not supported."""
    pass
class UnknownIRTypeError(InterpreterError):
    """Raised when an unknown IR type is encountered."""
    pass

# Runtime Errors
class DivisionByZeroError(InterpreterError):
    """Raised when attempting to divide by zero."""
    pass
class CannotModifyConstantError(InterpreterError):
    """Raised when trying to update a constant."""
    pass

# Lookup Errors
class NameNotFoundError(InterpreterError):
    """Raised when a variable, function, or container name is not found."""
    pass
class UnknownOperatorError(InterpreterError):
    """Raised when encountering an unknown operator."""
    pass
class ParameterMismatchError(InterpreterError):
    """Raised when number of passed values doesn't match expected parameters."""
    pass
class InvalidParameterIndexError(ParameterMismatchError):
    """Raised when a parameter does not have a valid index."""
    pass

# Variable declaration errors
class ReservedWordError(InterpreterError):
    """Raised when a variable or identifier is named using a reserved word."""
    pass