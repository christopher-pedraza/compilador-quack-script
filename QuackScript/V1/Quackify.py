from QuackCompiler import compile_program
from VirtualMachine import translate_program
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python Quackify.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        compile_program(input_file, input_file.replace(".quack", ".obj"))
        translate_program(input_file.replace(".quack", ".obj"))
    except FileNotFoundError:
        print(f"File {input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
