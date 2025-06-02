from collections import deque


class OperatorsInterface:
    def __init__(self):
        self.operators = {
            "+": 1,
            "-": 2,
            "*": 3,
            "/": 4,
            "<": 5,
            "<=": 6,
            ">": 7,
            ">=": 8,
            "==": 9,
            "!=": 10,
            "and": 11,
            "or": 12,
            "goto": 13,
            "gotoF": 14,
            "gotoT": 15,
            "=": 16,
            "print": 17,
            "era": 18,
            "param": 19,
            "gosub": 20,
            "return": 21,
            "endFunc": 22,
            "end": 23,
        }

    def get_operator(self, op: str):
        """Get the operator."""
        return self.operators.get(op, None)


class QuackQuadruple:
    def __init__(self):
        self.jumps_stack = []
        self.returns_stack = []
        self.quadruples = deque()
        self.current_index = 0
        self.operators = OperatorsInterface()

    def get_current_index(self):
        """Get the current index."""
        return self.current_index

    def add_quadruple(
        self, op: str, arg1: str, arg2: str, result: str = None, memory_space: str = None, result_type: str = None
    ):
        """Add a quadruple to the list."""
        op = self.operators.get_operator(op)
        self.quadruples.append((op, arg1, arg2, result))
        self.current_index += 1
        return result

    def add_return(self, return_value=None):
        """Add a return to the list."""
        if return_value is None:
            return_value = self.current_index

        self.returns_stack.append(return_value)

    def add_jump(self, type: str = "goto", condition: str = None, target: str = None):
        """Add a jump to the list."""
        type = self.operators.get_operator(type)
        self.quadruples.append((type, condition, None, target))
        self.current_index += 1

    def get_quadruples(self):
        """Get the list of quadruples."""
        return list(self.quadruples)

    def push_jump(self, jump: int = None):
        """Push a jump onto the stack."""
        if jump is None:
            jump = self.current_index
        self.jumps_stack.append(jump)

    def pop_jump(self):
        """Pop the last jump from the stack."""
        if self.jumps_stack:
            return self.jumps_stack.pop()
        return None

    def pop_return(self):
        """Pop the last return from the stack."""
        if self.returns_stack:
            return self.returns_stack.pop()
        return None

    def update_jump(self, index: int, target: int):
        """Update the jump at the given index."""
        if 0 <= index < len(self.quadruples):
            op, arg1, arg2, _ = self.quadruples[index]
            self.quadruples[index] = (op, arg1, arg2, target)
        else:
            raise IndexError("Jump index out of range")

    def get_str_representation(self, pretty: bool = False):
        """Get a string representation of the quadruples."""
        lines = []
        for i, quadruple in enumerate(self.quadruples):
            op = quadruple[0]
            op_str = next((k for k, v in self.operators.operators.items() if v == op), op) if pretty else op
            lines.append(f"{i}: ({op_str}, {quadruple[1]}, {quadruple[2]}, {quadruple[3]})")
        return "\n".join(lines)

    def __str__(self):
        """Get a string representation of the quadruples."""
        return "\n".join([f"{i}: {quadruple}" for i, quadruple in enumerate(self.quadruples)])

    def __repr__(self):
        """Get a string representation of the quadruples."""
        return self.__str__()
