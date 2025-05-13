from enum import Enum

class MemorySpace(Enum):
    GLOBAL = "global"
    LOCAL = "local"
    TEMP = "temp"
    CONSTANT = "constant"

class VarType(Enum):
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    STRING = "string"


class MemoryAddress:
    def __init__(self, address: int, space: MemorySpace, var_type: VarType):
        self.address = address
        self.space = space
        self.var_type = var_type

    def __repr__(self):
        return f"MemoryAddress({self.address}, {self.space.value}, {self.var_type.value})"


class MemoryManager:
    def __init__(self):
        # Memory layout configuration
        self.memory_spaces_reference = {
            MemorySpace.GLOBAL: {
                VarType.INT: (1000, 2999),
                VarType.FLOAT: (3000, 4999),
            },
            MemorySpace.LOCAL: {
                VarType.INT: (5000, 6999),
                VarType.FLOAT: (7000, 8999),
            },
            MemorySpace.TEMP: {
                VarType.INT: (9000, 9999),
                VarType.FLOAT: (10000, 11999),
                VarType.BOOL: (12000, 13999),
            },
            MemorySpace.CONSTANT: {
                VarType.INT: (14000, 15999),
                VarType.FLOAT: (16000, 17999),
                VarType.STRING: (18000, 19999),
            }
        }

        # Build flat list of ranges, ordered by start address
        self.ranges = []
        for space, types in self.memory_spaces_reference.items():
            for var_type, (start, end) in types.items():
                self.ranges.append((start, end, space, var_type))

        # Sort once by starting address
        self.ranges.sort()

        # Memory storage (nested lists by space and type)
        self.memory = {
            space: {} for space in MemorySpace
        }

        # Temp pointers
        self.reset_temp_pointers()

    def reset_temp_pointers(self):
        """Reset temp memory pointers to initial values."""
        self.temp_pointer = {}
        for vtype, (start, _) in self.memory_spaces_reference[MemorySpace.TEMP].items():
            self.temp_pointer[vtype] = start

    def get_address_info(self, memory_index: int) -> MemoryAddress:
        """Return MemoryAddress object using a fast linear scan optimized for sequential allocation."""
        for start, end, space, var_type in self.ranges:
            if start <= memory_index <= end:
                return MemoryAddress(memory_index, space, var_type)
        raise ValueError(f"Memory index {memory_index} is out of bounds.")

    def save(self, memory_index: int, value):
        mem_addr = self.get_address_info(memory_index)
        if mem_addr.var_type not in self.memory[mem_addr.space]:
            self.memory[mem_addr.space][mem_addr.var_type] = []
        offset = memory_index - self._get_range_start(mem_addr.space, mem_addr.var_type)
        while len(self.memory[mem_addr.space][mem_addr.var_type]) <= offset:
            self.memory[mem_addr.space][mem_addr.var_type].append(None)
        self.memory[mem_addr.space][mem_addr.var_type][offset] = value

    def retrieve(self, memory_index: int):
        mem_addr = self.get_address_info(memory_index)
        if mem_addr.var_type not in self.memory[mem_addr.space]:
            return None, mem_addr
        offset = memory_index - self._get_range_start(mem_addr.space, mem_addr.var_type)
        arr = self.memory[mem_addr.space][mem_addr.var_type]
        if 0 <= offset < len(arr):
            return arr[offset], mem_addr
        return None, mem_addr

    def _get_range_start(self, space: MemorySpace, var_type: VarType):
        return self.memory_spaces_reference[space][var_type][0]

    def save_to_first_available(self, value, var_type: VarType, space: MemorySpace) -> MemoryAddress:
        if space not in self.memory_spaces_reference:
            raise ValueError(f"Invalid memory space: {space.value}")
        if var_type not in self.memory_spaces_reference[space]:
            raise ValueError(f"Invalid type {var_type.value} for memory space {space.value}")

        start, end = self.memory_spaces_reference[space][var_type]
        if var_type not in self.memory[space]:
            self.memory[space][var_type] = []

        # Handle local/temp differently (use pointer-based allocation)
        if space == MemorySpace.TEMP:
            current = self.temp_pointer[var_type]
            if current > end:
                raise ValueError("No available space in temp memory.")
            memory_index = current
            self.temp_pointer[var_type] += 1
        else:
            # For global/constant/local, search for first None slot
            arr = self.memory[space][var_type]
            for offset in range(end - start + 1):
                if offset >= len(arr):
                    arr.append(None)
                if arr[offset] is None:
                    arr[offset] = value
                    memory_index = start + offset
                    break
            else:
                raise ValueError("No available space in target segment.")

        offset = memory_index - start
        while len(self.memory[space][var_type]) <= offset:
            self.memory[space][var_type].append(None)
        self.memory[space][var_type][offset] = value

        return MemoryAddress(memory_index, space, var_type)
    
if __name__ == "__main__":
    mm = MemoryManager()

    i1 = mm.save_to_first_available(42, VarType.INT, MemorySpace.GLOBAL)
    f1 = mm.save_to_first_available(3.14, VarType.FLOAT, MemorySpace.GLOBAL)
    s1 = mm.save_to_first_available("Hello", VarType.STRING, MemorySpace.CONSTANT)
    t1 = mm.save_to_first_available(True, VarType.BOOL, MemorySpace.TEMP)
    t2 = mm.save_to_first_available(7.5, VarType.FLOAT, MemorySpace.TEMP)
    t3 = mm.save_to_first_available(200, VarType.INT, MemorySpace.TEMP)

    print("Saved at:", i1, f1, s1, t1, t2, t3)

    print(mm.retrieve(i1.address))  # returns (value, MemoryAddress)
    print(mm.retrieve(f1.address))
    print(mm.retrieve(s1.address))
    print(mm.retrieve(t1.address))
    print(mm.retrieve(t2.address))
    print(mm.retrieve(t3.address))

    mm.reset_temp_pointers()
    t3 = mm.save_to_first_available(100, VarType.INT, MemorySpace.TEMP)
    print("Reused temp at:", t3)
    print(mm.retrieve(t3.address))
    print()