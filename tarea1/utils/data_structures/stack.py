from copy import deepcopy

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)
    
    def copy(self):
        new_stack = Stack()
        new_stack.items = deepcopy(self.items)
        return new_stack
    
    def __str__(self):
        return str(self.items)