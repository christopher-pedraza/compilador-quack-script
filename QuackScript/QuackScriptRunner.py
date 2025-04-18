from lark import Lark, UnexpectedInput

# Import grammar from file
with open('grammar.lark', 'r') as file:
    grammar = file.read()

# Create the Lark parser
parser = Lark(grammar, start='start', parser='lalr')

with open('test.quack', 'r') as file:
    input_program = file.read()

# Function to parse the input program
def parse_program(program):
    try:
        tree = parser.parse(program)
        print("Parsing successful!")
        print(tree.pretty())
    except UnexpectedInput as e:
        print(f"Parsing failed: {e}")

# Parse the example input program
parse_program(input_program)