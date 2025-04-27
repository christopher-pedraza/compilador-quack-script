class Symbol:
    def __init__(self, name, var_type, value=None, is_const=False):
        self.name = name
        self.var_type = var_type
        self.value = value
        self.is_const = is_const

class Container:
    def __init__(self, name):
        self.name = name
        self.symbols = {}

    def add_symbol(self, symbol: Symbol) -> None:
        """Add a symbol to the container."""
        if symbol.name in self.symbols:
            raise ValueError(f"Symbol {symbol.name} already exists in {self.name}.")
        self.symbols[symbol.name] = symbol

    def get_symbol(self, name: str) -> Symbol:
        """Get a symbol from the container."""
        return self.symbols.get(name, None)
    
    def update_symbol(self, name: str, value) -> None:
        """Update the value of a symbol in the container."""
        if name not in self.symbols:
            raise ValueError(f"Symbol {name} not found in {self.name}.")
        symbol = self.symbols[name]
        if symbol.is_const:
            raise ValueError(f"Cannot modify constant {name}.")
        symbol.value = value

    def is_symbol_declared(self, name: str) -> bool:
        """Check if a symbol is declared in the container."""
        return name in self.symbols

class SymbolTable:
    def __init__(self):
        self.containers = {}
        self.add_container(Container("global"))

    def get_container(self, name: str) -> Container:
        """Get a container by name."""
        if name not in self.containers:
            self.containers[name] = Container(name)
        return self.containers.get(name)

    def add_container(self, container: Container) -> None:
        """Add a new container to the symbol table."""
        if container.name in self.containers:
            raise ValueError(f"Container {container.name} already exists.")
        self.containers[container.name] = container

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
            container = self.containers["global"]
            if container.isSymbolDeclared(name):
                return container.get_symbol(name)
            else:
                raise ValueError(f"Symbol {name} not found in {containerName} or global container.")

    def __update_symbol(self, name: str, value, containerName: str) -> None:
        """Update the value of a symbol in the specified container."""
        container = self.get_container(containerName)
        if container.is_symbol_declared(name):
            container.update_symbol(name, value)
        else:
            container = self.containers["global"]
            if container.isSymbolDeclared(name):
                container.update_symbol(name, value)
            else:
                raise ValueError(f"Symbol {name} not found in {containerName} or global container.")
            
    def add_variable(self, name: str, var_type: str, value=None, is_const=False, containerName: str = "global") -> None:
        """Add a variable to the specified container."""
        variable = Symbol(name, var_type, value, is_const)
        self.__add_symbol(variable, containerName)

    def get_variable(self, name: str, containerName: str) -> Symbol:
        """Get a variable from the specified container."""
        return self.__get_symbol(name, containerName).value
    
    def update_variable(self, name: str, value, containerName: str) -> None:
        """Update the value of a variable in the specified container."""
        self.__update_symbol(name, value, containerName)