from QuackCompiler import compile_program
from VirtualMachine import QuackVirtualMachine
import os
import traceback

if __name__ == "__main__":
    test_files = []
    tests_dir = os.path.join(os.path.dirname(__file__), "tests")
    # Collect .quack files in tests/
    for f in os.listdir(tests_dir):
        if f.endswith(".quack"):
            test_files.append(os.path.join(tests_dir, f))
    # Collect .quack files in tests/unit-tests/
    unit_tests_dir = os.path.join(tests_dir, "unit-tests")
    for f in os.listdir(unit_tests_dir):
        if f.endswith(".quack"):
            test_files.append(os.path.join(unit_tests_dir, f))

    qvm = QuackVirtualMachine()

    for test_file in test_files:
        print("\n" * 3)
        print("=" * 80)
        print(f"About to run test: {test_file}")
        input("Press Enter to continue...")
        try:
            compile_program(test_file, test_file.replace(".quack", ".obj"))
            qvm.translate_program(test_file.replace(".quack", ".obj"))
        except FileNotFoundError:
            print(f"File {test_file} not found.")
        except Exception as e:
            print("An unexpected error occurred!")
            print(f"Type: {type(e).__name__}")
            print(f"Message: {e}")
            print("Traceback:")
            traceback.print_exc()
