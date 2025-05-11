import logging
import argparse
import sys
import os
from lark import Lark, logger, UnexpectedInput
from QuackTransformer import QuackTransformer
from QuackInterpreter import QuackInterpreter
from QuackQuadruple import QuackQuadruple

logger.setLevel(logging.DEBUG)

# Parse command-line arguments
# parser = argparse.ArgumentParser(description="Run a QuackScript program.")
# parser.add_argument("input_file", help="Path to the QuackScript input file")
# args = parser.parse_args()

# Import grammar from file
with open('grammar.lark', 'r') as file:
    grammar = file.read()

# Create the Lark parser
quackParser = Lark(grammar, start='start', parser='lalr', debug=True)
quack = quackParser.parse

def parse_program(program):
    try:
        # clear console
        # print("\033[H\033[J", end="")

        # Parse the input program
        tree = quack(program)

        # Transform the parse tree using QuackTransformer
        quack_transformer = QuackTransformer()
        ir = quack_transformer.transform(tree)

        # Get the symbol table from the transformer
        symbol_table = quack_transformer.symbol_table

        # Execute the IR
        quack_quadruple = QuackQuadruple()
        quack_interpreter = QuackInterpreter(symbol_table, quack_quadruple)
        quack_interpreter.execute(ir)

        print(quack_quadruple)

        # Display the symbol table after execution
        # print("\nSymbol Table after execution:")
        # symbol_table.display()

        return (tree.pretty(), ir, symbol_table.get_str_representation())
    except UnexpectedInput as e:
        print(f"Parsing failed: {e}")

if __name__ == "__main__":
    # Toma todos los archivos de la carpeta ./tests, realiza el parseo y guarda
    # el output en un archivo .out por cada uno de los archivos .quack
    # en la carpeta ./output
        if not os.path.exists("./tests"):
            os.makedirs("./tests")
        if not os.path.exists("./output"):
            os.makedirs("./output")

        for file in os.listdir("./tests"):
            if file.endswith(".quack"):
                with open(os.path.join("./output", f"{file[:-6]}.log"), "w", encoding="utf-8") as log_file:
                    sys.stdout = log_file
                    with open(os.path.join("./tests", file), 'r', encoding='utf-8') as input_file:
                        program = input_file.read()
                        tree, ir, symbol_table = parse_program(program)
                        # Guarda el output en un archivo .out
                        with open(os.path.join("./output", file.replace(".quack", ".out")), 'w', encoding='utf-8') as output_file:
                            output_file.write("Parse Tree:\n")
                            output_file.write(str(tree))
                            output_file.write("\n")
                            output_file.write("IR:\n")
                            output_file.write(str(ir))
                            output_file.write("\n\n")
                            output_file.write("Symbol Table:\n")
                            output_file.write(symbol_table)
                            output_file.write("\n")

                sys.stdout = sys.__stdout__
    # Si se pasa un archivo como argumento, lo parsea y ejecuta
    # el programa, mostrando el resultado en la consola
    # if args.input_file:
    #     # clear console
    #     print("\033[H\033[J", end="")
    #     # Parse the input program
    #     with open(args.input_file, 'r') as input_file:
    #         program = input_file.read()
    #         parse_program(program)

    