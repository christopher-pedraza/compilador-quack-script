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
    category: Literal["var", "const", "param"] = "var"
    address: int = None

    def __post_init__(self):
        if not isinstance(self.name, str):
            raise TypeError(f"Invalid type for symbol name: {type(self.name)}. Must be str.")
        if self.category not in ["var", "const", "param"]:
            raise ValueError(f"Invalid category: {self.category}. Must be 'var', 'const', or 'param'.")
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
    def __init__(self, name, body=None):
        self.name = name
        self.symbols = {}
        self.params = []
        self.body = body
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
        if symbol.name in self.symbols or symbol.name in self.params:
            raise SymbolRedeclarationError(f"Symbol '{symbol.name}' already exists in '{self.name}'.")
        if symbol.name in self.reserved_words:
            raise ReservedWordError(f"Symbol '{symbol.name}' is a reserved word and cannot be used as an identifier.")
        self.symbols[symbol.name] = symbol

    def get_symbol(self, name: str) -> Symbol:
        """Get a symbol from the container."""
        if name in self.params:
            return self.params.get(name)
        elif name in self.symbols:
            return self.symbols.get(name)
        else:
            raise NameNotFoundError(f"Symbol '{name}' not found in '{self.name}'.")

    def update_symbol(self, name: str, value) -> None:
        """Update the value of a symbol in the container."""
        if name not in self.symbols and name not in self.params:
            raise NameNotFoundError(f"Symbol '{name}' not found in '{self.name}'.")
        symbol = self.get_symbol(name)
        if symbol.category == "const":
            raise CannotModifyConstantError(f"Cannot modify constant '{name}'.")
        symbol.value = value

    def is_symbol_declared(self, name: str) -> bool:
        """Check if a symbol is declared in the container."""
        return name in self.symbols or name in self.params


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

    def __add_symbol(self, symbol: Symbol, containerName: str) -> None:
        """Add a symbol to the specified container."""
        container = self.get_container(containerName)
        container.add_symbol(symbol)

    def __get_symbol(self, name: str, containerName: str) -> Symbol:
        """Get a symbol from the specified container."""
        container = self.get_container(containerName)
        if container.is_symbol_declared(name):
            return container.get_symbol(name)
        else:
            container = self.containers[self.global_container_name]
            if container.is_symbol_declared(name):
                return container.get_symbol(name)
            else:
                raise NameNotFoundError(f"Symbol '{name}' not found in '{containerName}' or global container.")

    def __update_symbol(self, name: str, value, containerName: str) -> None:
        """Update the value of a symbol in the specified container."""
        container = self.get_container(containerName)
        if container.is_symbol_declared(name):
            container.update_symbol(name, value)
        else:
            container = self.containers[self.global_container_name]
            if container.is_symbol_declared(name):
                container.update_symbol(name, value)
            else:
                raise NameNotFoundError(f"Symbol '{name}' not found in '{containerName}' or global container.")

    def add_variable(
        self,
        name: str,
        var_type: str,
        value=None,
        category="var",
        containerName: str = None,
        param_index: int = None,
        address: int = None,
    ) -> None:
        """Add a variable to the specified container."""
        if containerName is None:
            containerName = self.global_container_name
        variable = Symbol(
            name=name, var_type=var_type, value=value, category=category, param_index=param_index, address=address
        )
        self.__add_symbol(variable, containerName)

    def get_variable(self, name: str, containerName: str) -> Symbol:
        """Get a variable from the specified container."""
        return self.__get_symbol(name, containerName)

    def get_variable_value(self, name: str, containerName: str) -> Symbol:
        """Get a variable from the specified container."""
        return self.__get_symbol(name, containerName).value

    def get_variable_type(self, name: str, containerName: str) -> str:
        """Get the type of a variable from the specified container."""
        return self.__get_symbol(name, containerName).var_type

    def update_variable(self, name: str, value, containerName: str) -> None:
        """Update the value of a variable in the specified container."""
        self.__update_symbol(name, value, containerName)

    """
    CHECAR
    """

    def add_parameter(self, name: str, var_type: str, containerName: str, param_index: int = None) -> None:
        """Add a parameter to the specified container."""
        variable = Symbol(name=name, var_type=var_type, category="param", param_index=param_index)
        container = self.get_container(containerName)
        container.add_param(variable)

    def add_function(self, name: str, params: list, body) -> None:
        """Add a function as a container"""
        self.add_container(Container(name, body))

        for i, param in enumerate(params):
            param_name, param_type = param
            self.add_parameter(name=param_name, var_type=param_type, containerName=name, param_index=i)

    def get_container(self, name: str) -> Container:
        """Get a container by name."""
        if name not in self.containers:
            raise NameNotFoundError(f"Container {name} not found.")
        return self.containers.get(name)

    def add_container(self, container: Container) -> None:
        """Add a new container to the symbol table."""
        if container.name in self.containers:
            raise ContainerRedeclarationError(f"Container '{container.name}' already exists.")
        self.containers[container.name] = container

    """
    CHECAR
    """

    def add_constant(
        self, address: int, value: Union[int, float, str, bool], value_type: Literal["int", "float", "str", "bool"]
    ) -> None:
        """Add a constant to the constants table."""
        self.constants_table.add_constant(address=address, value=value, value_type=value_type)

    def display(self) -> None:
        """Display the contents of the symbol table."""
        for container_name, container in self.containers.items():
            print(f"Container: {container_name}")
            print("  Parameters:")
            for param_name, param in container.params.items():
                print(f"  {param_name}: {param.var_type}, {param.value}, {param.category}, {param.param_index}")
            print("  Symbols:")
            for symbol_name, symbol in container.symbols.items():
                print(f"  {symbol_name}: {symbol.var_type}, {symbol.value}, {symbol.category}, {symbol.param_index}")

    def get_str_representation(self):
        """String representation of the symbol table."""
        result = ""
        for container_name, container in self.containers.items():
            result += f"Container: {container_name}\n"
            result += "  Parameters:\n"
            for param_name, param in container.params.items():
                result += f"  {param_name}: {param.var_type}, {param.value}, {param.category}, {param.param_index}\n"
            result += "  Symbols:\n"
            for symbol_name, symbol in container.symbols.items():
                result += (
                    f"  {symbol_name}: {symbol.var_type}, {symbol.value}, {symbol.category}, {symbol.param_index}\n"
                )
        # Add constants
        result += "Constants:\n"
        for address, constant in self.constants_table.constants.items():
            result += f"  {address}: {constant.value}\n"

        return result

    def create_global_container(self, id):
        """Create a global container with the given id."""
        self.add_container(Container(id, None))
        self.global_container_name = id

    def __str__(self):
        """String representation of the symbol table."""
        return self.get_str_representation()
