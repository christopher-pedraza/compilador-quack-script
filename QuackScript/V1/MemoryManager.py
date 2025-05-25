from dataclasses import dataclass
from typing import Union, List, Optional, Literal, Dict, Tuple


# @dataclass
# class MemoryAddress:
#     address: int
#     var_type: Literal["int", "float", "str", "bool"]

#     def __post_init__(self):
#         if not isinstance(self.address, int):
#             raise TypeError(f"Invalid type for address: {type(self.address)}. Must be int.")
#         if self.var_type not in ["int", "float", "str", "bool"]:
#             raise ValueError(f"Invalid type: {self.var_type}. Must be 'int', 'float', 'str', or 'bool'.")


@dataclass
class Memory:
    memory: Dict

    def __init__(self, mapping: Dict[str, Tuple[Tuple[int, int], Optional[int]]]):
        """
        Initialize memory for specified var types and allocation sizes.
        mapping: dict where keys are var types ("int", "float", "bool", "str")
        and values are the amount to allocate (int) or None (do not allocate).
        """
        self.memory = {}
        for var_type, config in mapping.items():
            addres_range, amount = config

            if var_type not in self.memory:
                self.memory[var_type] = {}

            self.memory[var_type]["address_range"] = addres_range

            if amount is not None:
                if not isinstance(amount, int) or amount < 0:
                    raise ValueError(f"Allocation for {var_type} must be a non-negative integer or None.")

                self.memory[var_type]["allocated"] = [None] * amount
            else:
                self.memory[var_type]["allocated"] = []

    def get_memory(
        self,
        var_type: str,
        index: int,
    ):
        """Get the memory for a specific var type."""
        if var_type not in self.memory:
            raise KeyError(f"Memory for type {var_type} not found.")
        start = self.memory[var_type]["address_range"][0]
        return self.memory[var_type]["allocated"][index - start]

    def set_memory(
        self,
        var_type: str,
        index: int,
        value: Union[int, float, str, bool],
    ):
        """Set the memory for a specific var type."""
        if var_type not in self.memory:
            raise KeyError(f"Memory for type {var_type} not found.")
        start, end = self.memory[var_type]["address_range"]

        if index < start or index > end:
            raise IndexError(f"Index {index} out of range for type {var_type}.")

        if index - start >= len(self.memory[var_type]["allocated"]):
            # Extend the allocated list if the index is greater than the current size
            self.memory[var_type]["allocated"].extend(
                [None] * (index - start - len(self.memory[var_type]["allocated"]) + 1)
            )

        self.memory[var_type]["allocated"][index - start] = value

    def add_memory(
        self,
        var_type: str,
        value: Union[int, float, str, bool],
    ):
        """Add a value to the memory for a specific var type in the next available slot."""
        if var_type not in self.memory:
            raise KeyError(f"Memory for type {var_type} not found.")
        start, end = self.memory[var_type]["address_range"]
        allocated = self.memory[var_type]["allocated"]
        for i in range(len(allocated)):
            if allocated[i] is None:
                allocated[i] = value
                return start + i
        if len(allocated) < end - start:
            allocated.append(value)
            return start + len(allocated) - 1
        raise MemoryError(f"No available space in memory for type {var_type}.")

    def get_var_type_from_address(self, address: int) -> str:
        """Get the variable type from the address."""
        for var_type, config in self.memory.items():
            start, end = config["address_range"]
            if start <= address <= end:
                return var_type
        raise ValueError(f"Address {address} not found in any memory space.")


@dataclass
class MemoryManager:
    memory_spaces: Dict[str, Memory]

    def __init__(self, mappings: Dict[str, Dict[str, Tuple[Tuple[int, int], Optional[int]]]] = None):
        self.memory_spaces = {}  # Ensure this is initialized before use
        if mappings is None:
            mappings = {
                "global": {
                    "int": ((1000, 1999), None),
                    "float": ((2000, 2999), None),
                    "t_int": ((3000, 3999), None),
                    "t_float": ((4000, 4999), None),
                    "t_bool": ((5000, 6999), None),
                },
                "local": {
                    "int": ((7000, 7999), None),
                    "float": ((8000, 8999), None),
                    "t_int": ((9000, 9999), None),
                    "t_float": ((10000, 10999), None),
                    "t_bool": ((11000, 11999), None),
                },
                "constant": {
                    "int": ((12000, 12999), None),
                    "float": ((13000, 13999), None),
                    "str": ((14000, 14999), None),
                },
            }
        self.next_available = {s: {} for s in ["global", "local", "constant"]}
        for space_name, mapping in mappings.items():
            self.add_memory_space(space_name=space_name, mapping=mapping)
            for var_type, (addr_range, _) in mapping.items():
                self.next_available[space_name][var_type] = addr_range[0]

    def add_memory_space(self, space_name: str, mapping: Dict[str, Tuple[Tuple[int, int], Optional[int]]]):
        """
        Add a new memory space with the specified mapping.
        space_name: Name of the memory space (e.g., "global", "local", "constant").
        mapping: dict where keys are var types ("int", "float", "bool", "str")
        and values are the amount to allocate (int) or None (do not allocate).
        """
        self.memory_spaces[space_name] = Memory(mapping=mapping)

    def get_first_available_address(self, space: str, var_type: str) -> int:
        """
        Returns the first available address for the given space and var_type, and increments the counter.
        Does not store anything in memory.
        """
        if space not in self.next_available or var_type not in self.next_available[space]:
            raise ValueError(f"No such space/var_type: {space}/{var_type}")
        addr = self.next_available[space][var_type]
        end_addr = self.memory_spaces[space].memory[var_type]["address_range"][1]
        if addr > end_addr:
            raise MemoryError(f"No available addresses left in {space} for type {var_type}.")
        self.next_available[space][var_type] += 1
        return addr

    def get_memory(self, space_name: str, index: int):
        """Get the memory for a specific space and index."""
        if space_name not in self.memory_spaces:
            raise KeyError(f"Memory space {space_name} not found.")
        var_type = self.memory_spaces[space_name].get_var_type_from_address(index)
        return self.memory_spaces[space_name].get_memory(var_type=var_type, index=index)

    def add_memory(self, space_name: str, var_type: str, value: Union[int, float, str, bool]):
        """Add a value to the memory for a specific space and var type."""
        if space_name not in self.memory_spaces:
            raise KeyError(f"Memory space {space_name} not found.")
        return self.memory_spaces[space_name].add_memory(var_type=var_type, value=value)

    def set_memory(self, space_name: str, var_type: str, index: int, value: Union[int, float, str, bool]):
        """Set the memory for a specific space and var type."""
        if space_name not in self.memory_spaces:
            raise KeyError(f"Memory space {space_name} not found.")
        return self.memory_spaces[space_name].set_memory(var_type=var_type, index=index, value=value)

    def replace_memory_space(self, space_name: str, new_memory: Memory) -> Memory:
        """Replace an existing memory space with a new Memory object."""
        if space_name not in self.memory_spaces:
            raise KeyError(f"Memory space {space_name} not found.")
        if not isinstance(new_memory, Memory):
            raise TypeError("Provided object is not of type Memory.")
        current_space = self.memory_spaces[space_name]
        self.memory_spaces[space_name] = new_memory
        return current_space

    def get_str_representation(self) -> str:
        """Return a table-like string representation of the memory manager."""
        lines = []
        for space, memory in self.memory_spaces.items():
            lines.append(f"Memory Space: {space}")
            lines.append(f"{'Type':<10} {'Address Range':<20} {'Allocated':<10} {'Values'}")
            for var_type, info in memory.memory.items():
                addr_range = f"{info['address_range'][0]}-{info['address_range'][1]}"
                allocated = len(info["allocated"])
                values = info["allocated"]
                lines.append(f"{var_type:<10} {addr_range:<20} {allocated:<10} {values}")
            lines.append("")
        return "\n".join(lines)

    def reset_local_temp_memory(self):
        """Reset the temporary memory spaces."""
        for var_type in self.memory_spaces["local"].memory:
            start = self.memory_spaces["local"].memory[var_type]["address_range"][0]
            self.next_available["local"][var_type] = start


if __name__ == "__main__":
    mm = MemoryManager()
    # mm.add_memory_space(
    #     "global",
    #     {
    #         "int": ((1000, 1999), None),
    #         "float": ((2000, 2999), None),
    #         "t_int": ((3000, 3999), None),
    #         "t_float": ((4000, 4999), None),
    #         "t_bool": ((5000, 6999), None),
    #     },
    # )
    # mm.add_memory_space(
    #     "constant", {"int": ((4000, 4999), None), "float": ((5000, 5999), None), "str": ((6000, 6999), None)}
    # )
    # mm.add_memory_space("local", {"int": ((7000, 7999), 5), "float": ((8000, 8999), 2), "t_int": ((9000, 9999), None)})

    mm.add_memory("local", "int", 10)
    mm.add_memory("local", "float", 3.14)
    print(mm.memory_spaces["local"], "\n\n")
    old_memory = mm.replace_memory_space(
        "local",
        Memory(
            mapping={
                "int": ((7000, 7999), 10),
                "float": ((8000, 8999), 5),
                "t_int": ((9000, 9999), None),
                "t_float": ((10000, 10999), None),
                "t_bool": ((11000, 11999), None),
            }
        ),
    )
    print("Old memory space:\n", old_memory, "\n\n")
    print("New memory space:\n", mm.memory_spaces["local"], "\n\n")
    mm.replace_memory_space("local", old_memory)  # Restore the old memory space
    print("Restored memory space:\n", mm.memory_spaces["local"], "\n\n")
