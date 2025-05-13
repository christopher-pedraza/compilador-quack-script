class MemoryManager:
    def __init__(self):
        self.memory = {"global": {}, "local": {}, "temp": {}, "constant": {}}
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
                "float": (10000, 11999),
                "bool": (12000, 13999),
            },
            "constant": {
                "int": (14000, 15999),
                "float": (16000, 17999),
                "string": (18000, 19999),
            }
        }

    def save(self, memory_index: int, value):
        """Save a value in the appropriate memory space based on the memory index."""
        for space, types in self.memory_spaces_reference.items():
            for var_type, (start, end) in types.items():
                if start <= memory_index <= end:
                    if var_type not in self.memory[space]:
                        self.memory[space][var_type] = []
                    offset = memory_index - start
                    # Ensure the list is large enough to hold the value at the offset
                    while len(self.memory[space][var_type]) <= offset:
                        self.memory[space][var_type].append(None)
                    self.memory[space][var_type][offset] = value
                    return
        raise ValueError(f"Memory index {memory_index} is out of bounds.")

    def retrieve(self, memory_index: int):
        """Retrieve the value and its type from memory using the memory index."""
        for space, types in self.memory_spaces_reference.items():
            for var_type, (start, end) in types.items():
                if start <= memory_index <= end:
                    if var_type in self.memory[space]:
                        offset = memory_index - start
                        if 0 <= offset < len(self.memory[space][var_type]):
                            return self.memory[space][var_type][offset], var_type
                    return None, None
        raise ValueError(f"Memory index {memory_index} is out of bounds.")

    def save_to_first_available(self, value, var_type, space):
        """Save a value in the first available position of the specified memory space."""
        if space not in self.memory_spaces_reference:
            raise ValueError(f"Invalid memory space: {space}")

        types = self.memory_spaces_reference[space]
        if var_type not in types:
            raise ValueError(f"Invalid type {var_type} for memory space {space}")

        start, end = types[var_type]
        if var_type not in self.memory[space]:
            self.memory[space][var_type] = []

        # Find the first available position
        for offset in range(end - start + 1):
            if offset >= len(self.memory[space][var_type]):
                self.memory[space][var_type].append(None)
            if self.memory[space][var_type][offset] is None:
                self.memory[space][var_type][offset] = value
                return start + offset

        raise ValueError(f"No available space for type {var_type} in memory space {space}.")

if __name__ == "__main__":
    memory_manager = MemoryManager()
    # memory_manager.save(1005, 42)  # Save a global int
    # memory_manager.save(16000, 3.14)  # Save a constant float
    # print(memory_manager.retrieve(1500))  # Retrieve the global int
    # print(memory_manager.retrieve(16000))  # Retrieve the constant float
    memory_manager.save_to_first_available(42, "int", "global")  # Save an int in global space
    memory_manager.save_to_first_available(3.14, "float", "global")  # Save a float in global space
    memory_manager.save_to_first_available("Hello", "string", "constant")  # Save a string in constant space
    memory_manager.save_to_first_available(100, "int", "local")  # Save another int in global space
    print(memory_manager.retrieve(1000))  # Retrieve the first int
    print(memory_manager.retrieve(3000))  # Retrieve the float
    print(memory_manager.retrieve(18000))  # Retrieve the string
    print(memory_manager.retrieve(5000))  # Retrieve the second int
    print(memory_manager.memory)  # Print the memory state