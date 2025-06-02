from QuackCompiler import compile_program
from VirtualMachine import QuackVirtualMachine
import sys
import traceback

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python Quackify.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not input_file.endswith(".quack"):
        print("Error: Input file must have a .quack extension.")
        sys.exit(1)

    qvm = QuackVirtualMachine()

    try:
        compile_program(input_file, input_file.replace(".quack", ".obj"))
        qvm.translate_program(input_file.replace(".quack", ".obj"))
    except FileNotFoundError:
        print(f"File {input_file} not found.")
    except Exception as e:
        print("An unexpected error occurred!")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {e}")
        print("Traceback:")
        traceback.print_exc()
