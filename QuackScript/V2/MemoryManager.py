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
        """Retrieve the value from memory using the memory index."""
        for space, types in self.memory_spaces_reference.items():
            for var_type, (start, end) in types.items():
                if start <= memory_index <= end:
                    if var_type in self.memory[space]:
                        offset = memory_index - start
                        if 0 <= offset < len(self.memory[space][var_type]):
                            return self.memory[space][var_type][offset]
                    return None
        raise ValueError(f"Memory index {memory_index} is out of bounds.")

    def save_to_first_available(self, value, var_type):
        """Save a value in the first available position of the correct memory space."""
        for space, types in self.memory_spaces_reference.items():
            if var_type in types:
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
        raise ValueError(f"No available space for type {var_type}.")

if __name__ == "__main__":
    memory_manager = MemoryManager()
    # memory_manager.save(1005, 42)  # Save a global int
    # memory_manager.save(16000, 3.14)  # Save a constant float
    # print(memory_manager.retrieve(1500))  # Retrieve the global int
    # print(memory_manager.retrieve(16000))  # Retrieve the constant float
    memory_manager.save_to_first_available(42, "int")  # Save an int
    memory_manager.save_to_first_available(3.14, "float")  # Save a float
    memory_manager.save_to_first_available("Hello", "string")  # Save a string
    memory_manager.save_to_first_available(100, "int")  # Save another int
    print(memory_manager.retrieve(1000))  # Retrieve the first int
    print(memory_manager.retrieve(3000))  # Retrieve the float
    print(memory_manager.retrieve(18000))  # Retrieve the string
    print(memory_manager.retrieve(1001))  # Retrieve the second int
    print(memory_manager.memory)  # Print the memory state