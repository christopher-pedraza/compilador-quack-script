from Exceptions import (
    SymbolRedeclarationError,
    ParameterRedeclarationError,
    ParameterMismatchError,
    InvalidParameterIndexError,
    NameNotFoundError,
    CannotModifyConstantError,
    ContainerRedeclarationError,
    ReservedWordError,
)

from dataclasses import dataclass
from typing import Union, Literal


@dataclass
class Symbol:
    name: str
    var_type: Literal["int", "float", "str", "bool"]
    isConstant: bool = False
    address: int = None

    def __post_init__(self):
        if not isinstance(self.name, str):
            raise TypeError(f"Invalid type for symbol name: {type(self.name)}. Must be str.")
        if self.var_type not in ["int", "float", "str", "bool"]:
            raise ValueError(f"Invalid type: {self.var_type}. Must be 'int', 'float', 'str', or 'bool'.")


@dataclass
class Parameter:
    name: str
    var_type: Literal["int", "float", "str", "bool"]


@dataclass
class Constant:
    value: Union[int, float, str, bool]
    var_type: Literal["int", "float", "str", "bool"]

    def __post_init__(self):
        if not isinstance(self.value, (int, float, str, bool)):
            raise TypeError(f"Invalid type for constant value: {type(self.value)}. Must be int, float, str, or bool.")


class Container:
    def __init__(self, name, return_type: Literal["int", "float", None]):
        self.name = name
        self.return_type = return_type
        self.initial_position = None
        self.symbols = {}
        self.param_signature = []
        self.reserved_words = [
            "if",
            "else",
            "while",
            "do",
            "int",
            "float",
            "program",
            "main",
            "void",
            "end",
            "const",
            "var",
            "print",
            "and",
            "or",
        ]

    def add_symbol(self, symbol: Symbol) -> None:
        """Add a symbol to the container."""
        if symbol.name in self.reserved_words:
            raise ReservedWordError(f"Symbol '{symbol.name}' is a reserved word and cannot be used as an identifier.")
        if symbol.name in self.symbols:
            raise SymbolRedeclarationError(f"Symbol '{symbol.name}' already exists in '{self.name}'.")
        self.symbols[symbol.name] = symbol

    def get_symbol(self, name: str) -> Symbol:
        """Get a symbol from the container."""
        if name in self.symbols:
            return self.symbols.get(name)
        else:
            raise NameNotFoundError(f"Symbol '{name}' not found in '{self.name}'.")

    def is_symbol_declared(self, name: str) -> bool:
        """Check if a symbol is declared in the container."""
        return name in self.symbols or name in self.params

    def set_initial_position(self, position: int) -> None:
        """Set the initial position of the container."""
        self.initial_position = position


class ConstantsTable:
    def __init__(self):
        self.constants = {}

    def add_constant(
        self, address: int, value: Union[int, float, str, bool], value_type: Literal["int", "float", "str", "bool"]
    ) -> None:
        """Add a constant to the table."""
        if address not in self.constants:
            self.constants[address] = Constant(value=value, value_type=value_type)


class SymbolTable:
    def __init__(self):
        self.containers = {}
        self.global_container_name = "global"
        self.constants_table = ConstantsTable()

    def get_variable(self, name: str, containerName: str) -> Symbol:
        """Get a variable from the specified container."""
        container = self.get_container(containerName)
        # Check if the symbol is declared in the specified container
        if container.is_symbol_declared(name):
            return container.get_symbol(name)
        # If not, check in the global container
        else:
            container = self.get_container(self.global_container_name)
            if container.is_symbol_declared(name):
                return container.get_symbol(name)
            else:
                raise NameNotFoundError(f"Symbol '{name}' not found in '{containerName}' or global container.")

    def add_variable(
        self,
        name: str,
        var_type: str,
        containerName: str,
        isConstant: bool = False,
        address: int = None,
    ) -> None:
        """Add a variable to the specified container."""
        variable = Symbol(name=name, var_type=var_type, isConstant=isConstant, address=address)
        container = self.get_container(containerName)
        container.add_symbol(variable)

    def add_parameter(self, name: str, var_type: str, containerName: str, address: int) -> None:
        """Add a parameter to the specified container."""
        self.add_variable(
            name=name,
            var_type=var_type,
            isConstant=False,
            containerName=containerName,
            address=address,
        )
        self.get_container(containerName).param_signature.append(var_type)

    def add_function(self, name: str, return_type: str) -> None:
        """Add a function as a container"""
        if name in self.containers:
            raise ContainerRedeclarationError(f"Container '{name}' already exists.")
        self.containers[name] = Container(name=name, return_type=return_type)

    def create_global_container(self, id):
        """Create a global container with the given id."""
        self.add_function(id, None)
        self.global_container_name = id

    def get_container(self, name: str) -> Container:
        """Get a container by name."""
        if name not in self.containers:
            raise NameNotFoundError(f"Container {name} not found.")
        return self.containers.get(name)

    def add_constant(
        self, address: int, value: Union[int, float, str, bool], value_type: Literal["int", "float", "str", "bool"]
    ) -> None:
        """Add a constant to the constants table."""
        self.constants_table.add_constant(address=address, value=value, value_type=value_type)

    def get_str_representation(self):
        """String representation of the symbol table."""
        result = ""
        # Global container
        gcontainer = self.containers.get(self.global_container_name)
        result += f"Global Container: {self.global_container_name}\n"
        for symbol_name, symbol in gcontainer.symbols.items():
            result += f"  {symbol_name}: {symbol.var_type} (Address: {symbol.address})\n"

        # Rest of the containers
        for container_name, container in self.containers.items():
            if container_name == self.global_container_name:
                continue
            result += f"Container: {container_name}\n"
            result += f"Return Type: {container.return_type}\n"
            result += "Symbols:\n"
            for symbol_name, symbol in container.symbols.items():
                result += f"  {symbol_name}: {symbol.var_type} (Address: {symbol.address})\n"
            result += "Parameters:\n"
            for param in container.param_signature:
                result += f"  {param}\n"
            result += "\n"
        result += "Constants:\n"
        for address, constant in self.constants_table.constants.items():
            result += f"  Address: {address}, Value: {constant.value}, Type: {constant.var_type}\n"
        result += "\n"

        return result

    def __str__(self):
        """String representation of the symbol table."""
        return self.get_str_representation()
