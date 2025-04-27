import logging
from lark import Lark, logger, UnexpectedInput
from QuackTransformer import QuackTransformer
from SymbolTable import SymbolTable

logger.setLevel(logging.DEBUG)

# Import grammar from file
with open('grammar.lark', 'r') as file:
    grammar = file.read()

# TODO: Define .lark file as an argument to the script
with open('test.quack', 'r') as file:
    input_program = file.read()

# Create the Lark parser
quackParser = Lark(grammar, start='start', parser='lalr', debug=True)
quack = quackParser.parse

# Initialize the symbol table
symbol_table = SymbolTable()
symbol_table.add_variable(name="a", value=15, var_type="int", containerName="global", is_const=False)

def parse_program(program):
    try:
        # clear console
        print("\033[H\033[J", end="")
        # Parse the input program
        tree = quack(program)
        print(tree.pretty())
        # Transform the parse tree using QuackTransformer
        transformed_tree = QuackTransformer(symbol_table).transform(tree)
        print(transformed_tree)
    except UnexpectedInput as e:
        print(f"Parsing failed: {e}")

# Parse the example input program
parse_program(input_program)