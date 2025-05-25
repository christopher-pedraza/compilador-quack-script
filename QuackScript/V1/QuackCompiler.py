import logging
import sys
import os
from lark import Lark, logger, UnexpectedInput
from QuackTransformer import QuackTransformer
from QuackInterpreter import QuackInterpreter
from QuackQuadruple import QuackQuadruple
from MemoryManager import MemoryManager
import pickle

logger.setLevel(logging.DEBUG)

# Import grammar from file
with open("grammar.lark", "r") as file:
    grammar = file.read()

# Create the Lark parser
quackParser = Lark(grammar, start="start", parser="lalr", debug=True)
quack = quackParser.parse


def generate_obj_file(quadruples, symbol_table, output_file):
    """
    Generates a binary object file from the quadruple and symbol table.
    """
    data = {
        "quadruples": quadruples.quadruples,
        "operators": quadruples.operators.operators,
        "functions": symbol_table.containers,
        "constants_table": symbol_table.constants_table,
        "global_container_name": symbol_table.global_container_name,
    }
    with open(output_file, "wb") as f:
        pickle.dump(data, f)
    # print(f"Object file generated: {output_file}")


def parse_program(program):
    try:
        # Parse the input program
        tree = quack(program)

        # Transform the parse tree using QuackTransformer
        quack_transformer = QuackTransformer()
        ir = quack_transformer.transform(tree)

        # Get the symbol table from the transformer
        symbol_table = quack_transformer.symbol_table

        # Execute the IR
        # Initialize the memory manager
        memory_manager = MemoryManager()
        quack_quadruple = QuackQuadruple()
        quack_interpreter = QuackInterpreter(symbol_table, quack_quadruple, memory_manager)
        quack_interpreter.execute(ir)

        return (tree.pretty(), ir, symbol_table, quack_quadruple, memory_manager)
    except UnexpectedInput as e:
        print(f"Parsing failed: {e}")


def compile_program(input_file, output_file):
    """
    Compiles a QuackScript program from an input file and generates an object file.
    """
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            program = file.read()
        tree, ir, symbol_table, quadruples, memory = parse_program(program)
        generate_obj_file(quadruples, symbol_table, output_file)
    except FileNotFoundError:
        print(f"File {input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


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
                with open(os.path.join("./tests", file), "r", encoding="utf-8") as input_file:
                    program = input_file.read()
                    tree, ir, symbol_table, quadruples, memory = parse_program(program)
                    # Guarda el output en un archivo .out
                    with open(
                        os.path.join("./output", file.replace(".quack", ".out")), "w", encoding="utf-8"
                    ) as output_file:
                        output_file.write("Parse Tree:\n")
                        output_file.write(str(tree))
                        output_file.write("\n")
                        output_file.write("IR:\n")
                        output_file.write(str(ir))
                        output_file.write("\n\n")
                        output_file.write("Symbol Table:\n")
                        output_file.write(symbol_table.get_str_representation())
                        output_file.write("\n")
                        output_file.write("Quadruples:\n")
                        output_file.write(quadruples.get_str_representation(pretty=True))
                        output_file.write("\n\n")
                        output_file.write("Memory:\n")
                        output_file.write(memory.get_str_representation())
                        output_file.write("\n\n")

            sys.stdout = sys.__stdout__
