class SemanticCube:
    def __init__(self):
        self.cube = {
            "int": {
                "int": {
                    "+": "int",
                    "-": "int",
                    "*": "int",
                    "/": "int",
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
                },
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
                },
            },
        }

        self.valid_declarations = {
            "int": {
                "int": True,
            },
            "float": {"float": True},
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
