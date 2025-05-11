from collections import deque 

class QuackQuadruple:
    def __init__(self):
        self.jumps_stack = []
        self.returns_stack = []
        self.quadruples = deque()
        self.current_memory_space = 0
        self.current_index = 0

    def get_current_memory_space(self):
        """Get the current memory space."""
        current = self.current_memory_space
        self.current_memory_space += 1
        return current

    def add_quadruple(self, op: str, arg1: str, arg2: str, result: str = None):
        """Add a quadruple to the list."""
        if result is None:
            result = f"t{self.get_current_memory_space()}"
        self.quadruples.append((op, arg1, arg2, result))
        self.current_index += 1
        return result

    def get_quadruples(self):
        """Get the list of quadruples."""
        return list(self.quadruples)
    
    def __str__(self):
        """Get a string representation of the quadruples."""
        return "\n".join([f"{i}: {quadruple}" for i, quadruple in enumerate(self.quadruples)])
