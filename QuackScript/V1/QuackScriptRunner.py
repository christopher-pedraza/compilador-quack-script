import logging
from lark import Lark, logger, UnexpectedInput

from QuackTransformer import QuackTransformer

logger.setLevel(logging.DEBUG)

# Import grammar from file
with open('grammar_v1.lark', 'r') as file:
    grammar = file.read()

# Create the Lark parser
parser = Lark(grammar, start='start', parser='lalr', debug=True)

with open('test.quack', 'r') as file:
    input_program = file.read()

# Function to parse the input program
def parse_program(program):
    try:
        tree = parser.parse(program)
        print(tree.pretty())
        # Transform the parse tree using QuackTransformer
        transformed_tree = QuackTransformer().transform(tree)
        print(transformed_tree)
    except UnexpectedInput as e:
        print(f"Parsing failed: {e}")

# Parse the example input program
parse_program(input_program)