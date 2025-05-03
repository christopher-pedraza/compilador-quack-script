class SemanticCube:
    def __init__(self):
        self.cube = {
            "int": {
                "int": {
                    "+": "int",
                    "-": "int",
                    "*": "int",
                    "/": "float",
                    "<": "int",
                    "<=": "int",
                    ">": "int",
                    ">=": "int",
                    "==": "int",
                    "!=": "int",
                    "and": "int",
                    "or": "int",
                },
                "float": {
                    "+": "float",
                    "-": "float",
                    "*": "float",
                    "/": "float",
                    "<": "int",
                    "<=": "int",
                    ">": "int",
                    ">=": "int",
                    "==": "int",
                    "!=": "int",
                    "and": "int",
                    "or": "int",
                }
            },
            "float": {
                "int": {
                    "+": "float",
                    "-": "float",
                    "*": "float",
                    "/": "float",
                    "<": "int",
                    "<=": "int",
                    ">": "int",
                    ">=": "int",
                    "==": "int",
                    "!=": "int",
                    "and": "int",
                    "or": "int",
                },
                "float": {
                    "+": "float",
                    "-": "float",
                    "*": "float",
                    "/": "float",
                    "<": "int",
                    "<=": "int",
                    ">": "int",
                    ">=": "int",
                    "==": "int",
                    "!=": "int",
                    "and": "int",
                    "or": "int",
                }
            }
        }

        self.valid_declarations = {
            "int": {
                "int": lambda x: x,  # No conversion needed
                "float": lambda x: int(x)  # Convert float to int (truncation)
            },
            "float": {
                "int": lambda x: float(x),  # Convert int to float
                "float": lambda x: x  # No conversion needed
            }
        }

    def get_type(self, type1, type2, operation):
        # Get the resulting type of an operation between two types
        if type1 in self.cube and type2 in self.cube[type1]:
            if operation in self.cube[type1][type2]:
                return self.cube[type1][type2][operation]
        return None  # Invalid operation or types

    def is_decl_valid(self, type1, type2):
        # Check if the types are valid for declaration
        return type1 in self.valid_declarations and type2 in self.valid_declarations[type1]
    
    def convert_type(self, type1, type2, value):
        # Convert value from type1 to type2 if valid
        if self.is_decl_valid(type1, type2):
            return self.valid_declarations[type1][type2](value)
        return None