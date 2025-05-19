class MemoryAddress:
    def __init__(self, address: int, space: str, var_type: str):
        self.address = address
        self.space = space
        self.var_type = var_type

    def __repr__(self):
        return f"MemoryAddress({self.address}, {self.space}, {self.var_type})"


class MemoryManager:
    def __init__(self):
        # Memory layout configuration using plain strings
        self.memory_spaces_reference = {
            "global": {
                "int": (1000, 2999),
                "float": (3000, 4999),
            },
            "local": {
                "int": (5000, 6999),
                "float": (7000, 8999),
            },
            "temp": {
                "int": (9000, 9999),
                "float": (10000, 10999),
                "bool": (11000, 11999),
            },
            "constant": {
                "int": (12000, 13999),
                "float": (14000, 15999),
                "str": (16000, 17999),
            },
        }

        # Build flat list of ranges, ordered by start address
        self.ranges = []
        for space, types in self.memory_spaces_reference.items():
            for var_type, (start, end) in types.items():
                self.ranges.append((start, end, space, var_type))

        # Sort once by starting address
        self.ranges.sort()

        # Memory storage (nested dictionaries by space and type)
        self.memory = {"global": {}, "local": {}, "temp": {}, "constant": {}}

        # Temp pointers
        self.reset_temp_pointers()

    def reset_temp_pointers(self):
        """Reset temp memory pointers to initial values."""
        self.temp_pointer = {}
        for vtype, (start, _) in self.memory_spaces_reference["temp"].items():
            self.temp_pointer[vtype] = start

    def get_address_info(self, memory_index: int) -> MemoryAddress:
        """Return MemoryAddress object using a fast linear scan optimized for sequential allocation."""
        for start, end, space, var_type in self.ranges:
            if start <= memory_index <= end:
                return MemoryAddress(memory_index, space, var_type)
        raise ValueError(f"Memory index {memory_index} is out of bounds.")

    def save(self, memory_index: int, value):
        mem_addr = self.get_address_info(memory_index)
        space = mem_addr.space
        var_type = mem_addr.var_type
        if var_type not in self.memory[space]:
            self.memory[space][var_type] = []
        offset = memory_index - self._get_range_start(space, var_type)
        while len(self.memory[space][var_type]) <= offset:
            self.memory[space][var_type].append(None)
        self.memory[space][var_type][offset] = value

    def retrieve(self, memory_index: int):
        mem_addr = self.get_address_info(memory_index)
        space = mem_addr.space
        var_type = mem_addr.var_type
        if var_type not in self.memory[space]:
            return None, mem_addr
        offset = memory_index - self._get_range_start(space, var_type)
        arr = self.memory[space][var_type]
        if 0 <= offset < len(arr):
            return arr[offset], mem_addr
        return None, mem_addr

    def _get_range_start(self, space: str, var_type: str):
        return self.memory_spaces_reference[space][var_type][0]

    def save_to_first_available(self, value, var_type: str, space: str) -> MemoryAddress:
        if space not in self.memory_spaces_reference:
            raise ValueError(f"Invalid memory space: {space}")
        if var_type not in self.memory_spaces_reference[space]:
            raise ValueError(f"Invalid type {var_type} for memory space {space}")

        start, end = self.memory_spaces_reference[space][var_type]
        if var_type not in self.memory[space]:
            self.memory[space][var_type] = []

        # Handle local/temp differently (use pointer-based allocation)
        if space == "temp":
            current = self.temp_pointer[var_type]
            if current > end:
                raise ValueError("No available space in temp memory.")
            memory_index = current
            self.temp_pointer[var_type] += 1
        # Handle constant differently (if the constant is already in memory, reuse it)
        elif space == "constant":
            for offset in range(start, end + 1):
                if (offset - start) < len(self.memory[space][var_type]) and self.memory[space][var_type][
                    offset - start
                ] == value:
                    memory_index = offset
                    break
                elif (offset - start) >= len(self.memory[space][var_type]) or self.memory[space][var_type][
                    offset - start
                ] is None:
                    memory_index = offset
                    self.memory[space][var_type].append(value)
                    break
            else:
                raise ValueError("No available space in constant memory.")
        else:
            # For global/local, search for first None slot
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

        if space != "constant":
            offset = memory_index - start
            while len(self.memory[space][var_type]) <= offset:
                self.memory[space][var_type].append(None)
            self.memory[space][var_type][offset] = value

        return MemoryAddress(memory_index, space, var_type)

    def get_str_representation(self):
        """Return a string representation of the memory manager."""
        return "\n".join(f"{space}: {types}" for space, types in self.memory.items())

    def __str__(self):
        """Return a string representation of the memory manager, including memory indices with respect to their ranges."""
        result = []
        for space, types in self.memory.items():
            result.append(f"{space}:")
            for var_type, values in types.items():
                start = self.memory_spaces_reference[space][var_type][0]
                indexed_values = [f"{start + i}: {v}" for i, v in enumerate(values)]
                result.append(f"  {var_type}: {indexed_values}")
        return "\n".join(result)

    def __repr__(self):
        """Return a string representation of the memory manager."""
        return self.__str__()


if __name__ == "__main__":
    mm = MemoryManager()

    t1 = mm.save_to_first_available("Hello", "str", "constant")
    print("\n", t1, "\n", mm)
    t2 = mm.save_to_first_available("World", "str", "constant")
    print("\n", t2, "\n", mm)
    t3 = mm.save_to_first_available("Hello", "str", "constant")
    print("\n", t3, "\n", mm)
    t4 = mm.save_to_first_available("World", "str", "constant")
    print("\n", t4, "\n", mm)

    # print("Saved at:", i1, f1, s1, t1, t2, t3)

    # print(mm.retrieve(i1.address))  # returns (value, MemoryAddress)
    # print(mm.retrieve(f1.address))
    # print(mm.retrieve(s1.address))
    # print(mm.retrieve(t1.address))
    # print(mm.retrieve(t2.address))
    # print(mm.retrieve(t3.address))

    # mm.reset_temp_pointers()
    # t3 = mm.save_to_first_available(100, "int", "temp")
    # print("Reused temp at:", t3)
    # print(mm.retrieve(t3.address))
