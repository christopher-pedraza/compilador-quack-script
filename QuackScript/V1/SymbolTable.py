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


class Container:
    def __init__(self, name, return_type: Literal["int", "float", None]):
        self.name = name
        self.return_type = return_type
        self.return_address = None
        self.initial_position = None
        self.symbols = {}
        self.param_signature = []
        self.required_space = {}
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
        return name in self.symbols

    def set_initial_position(self, position: int) -> None:
        """Set the initial position of the container."""
        self.initial_position = position

    def get_param_signature(self) -> list:
        """Get the parameter signature of the container."""
        return self.param_signature

    def clear(self) -> None:
        """Clear the container's symbols."""
        self.symbols.clear()


@dataclass
class Constant:
    value: Union[int, float, str, bool]
    var_type: Literal["int", "float", "str", "bool"]

    def __post_init__(self):
        if not isinstance(self.value, (int, float, str, bool)):
            raise TypeError(f"Invalid type for constant value: {type(self.value)}. Must be int, float, str, or bool.")


class ConstantsTable:
    def __init__(self):
        self.constants = {}
        self.required_space = {"int": 0, "float": 0, "str": 0}

    def add_constant(
        self, address: int, value: Union[int, float, str, bool], value_type: Literal["int", "float", "str", "bool"]
    ) -> None:
        """Add a constant to the table."""
        if address not in self.constants:
            self.constants[address] = Constant(value=value, var_type=value_type)
            self.required_space[value_type] += 1

    def check_and_get_address(self, value: Union[int, float, str, bool]) -> int:
        """Check if a constant exists and retrieve its address."""
        for address, constant in self.constants.items():
            if constant.value == value:
                return address
        return None


class SymbolTable:
    def __init__(self):
        self.containers = {}
        self.global_container_name = "global"
        self.constants_table = ConstantsTable()

    def get_variable(self, name: str, containerName: str) -> Symbol:
        """Get a variable from the specified container."""
        container = self.get_function(containerName)
        # Check if the symbol is declared in the specified container
        if container.is_symbol_declared(name):
            return container.get_symbol(name)
        # If not, check in the global container
        else:
            container = self.get_function(self.global_container_name)
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
        container = self.get_function(containerName)
        container.add_symbol(variable)
        container.required_space[var_type] = container.required_space.get(var_type, 0) + 1

    def add_parameter(self, name: str, var_type: str, containerName: str, address: int) -> None:
        """Add a parameter to the specified container."""
        self.add_variable(
            name=name,
            var_type=var_type,
            isConstant=False,
            containerName=containerName,
            address=address,
        )
        container = self.get_function(containerName)
        container.param_signature.append(var_type)

    def add_temp(self, var_type: str, containerName: str):
        container = self.get_function(containerName)
        container.required_space[var_type] = container.required_space.get(var_type, 0) + 1

    def add_function(self, name: str, return_type: str) -> None:
        """Add a function as a container"""
        if name in self.containers:
            raise ContainerRedeclarationError(f"Container '{name}' already exists.")
        self.containers[name] = Container(name=name, return_type=return_type)

    def create_global_container(self, id):
        """Create a global container with the given id."""
        self.add_function(id, None)
        self.global_container_name = id

    def get_function(self, name: str) -> Container:
        """Get a container by name."""
        if name not in self.containers:
            raise NameNotFoundError(f"Container {name} not found.")
        return self.containers.get(name)

    def is_function_declared(self, name: str) -> bool:
        """Check if a function is declared."""
        return name in self.containers

    def add_constant(
        self, address: int, value: Union[int, float, str, bool], value_type: Literal["int", "float", "str", "bool"]
    ) -> None:
        """Add a constant to the constants table."""
        self.constants_table.add_constant(address=address, value=value, value_type=value_type)

    def get_return_type(self, containerName: str) -> str:
        """Get the return type of a container."""
        container = self.get_function(containerName)
        if container.return_type is None:
            raise ValueError(f"Container '{containerName}' has no return type.")
        return container.return_type

    def get_str_representation(self) -> str:
        """Return a table-like string representation of the symbol table."""
        lines = []

        # Global container
        gcontainer = self.containers.get(self.global_container_name)
        lines.append(f"Global Container: {self.global_container_name}")
        lines.append(f"Initial Position: {gcontainer.initial_position if gcontainer else 'N/A'}")
        if gcontainer and gcontainer.symbols:
            lines.append(f"{'Name':<15} {'Type':<10} {'Const':<6} {'Address':<10}")
            for symbol in gcontainer.symbols.values():
                lines.append(
                    f"{symbol.name:<15} {symbol.var_type:<10} {str(symbol.isConstant):<6} {str(symbol.address):<10}"
                )
            # Show required space for global container
            if gcontainer.required_space:
                lines.append("Required Space:")
                for vtype, amount in gcontainer.required_space.items():
                    lines.append(f"  {vtype}: {amount}")
        else:
            lines.append("  (No symbols)")
        lines.append("")

        # Other containers (functions)
        for cname, container in self.containers.items():
            if cname == self.global_container_name:
                continue
            lines.append(f"Container: {cname}")
            lines.append(
                f"Initial Position: {container.initial_position if container.initial_position is not None else 'N/A'}"
            )
            lines.append(f"Return Type: {container.return_type}")
            # Symbols
            lines.append(f"{'Name':<15} {'Type':<10} {'Const':<6} {'Address':<10}")
            if not container.symbols:
                lines.append("  (No symbols)")
            for symbol in container.symbols.values():
                lines.append(
                    f"{symbol.name:<15} {symbol.var_type:<10} {str(symbol.isConstant):<6} {str(symbol.address):<10}"
                )
            # Parameters
            if container.param_signature:
                lines.append("Parameters:")
                for idx, param_type in enumerate(container.param_signature):
                    lines.append(f"  {idx + 1}. {param_type}")
            else:
                lines.append("Parameters: None")
            # Show required space for this container
            if container.required_space:
                lines.append("Required Space:")
                for vtype, amount in container.required_space.items():
                    lines.append(f"  {vtype}: {amount}")
            lines.append("")

        # Constants table
        lines.append("Constants Table:")
        if self.constants_table.constants:
            lines.append(f"{'Address':<10} {'Value':<20} {'Type':<10}")
            for address, constant in self.constants_table.constants.items():
                lines.append(f"{str(address):<10} {str(constant.value):<20} {constant.var_type:<10}")
        else:
            lines.append("  (No constants)")
        lines.append("")

        return "\n".join(lines)

    def __str__(self):
        """String representation of the symbol table."""
        return self.get_str_representation()
