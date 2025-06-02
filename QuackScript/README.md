# QuackScript Language and Compiler

QuackScript is a custom programming language with a full compilation and
execution pipeline. It features a robust syntax supporting various programming
constructs and a virtual machine for code execution.

## Documentation (in Spanish)

- For detailed information about this code, please refer to the documentation: [Documentacion.pdf](./Documentacion.pdf)

## Language Features

### Data Types and Variables

- **Primitive Types:** Integer (`int`) and floating-point (`float`) data types
- **Variable Declaration:** `var name: type;` or `var name: type = value;`
- **Constants:** `const NAME: type = value;`
- **Multiple Declarations:** `var x, y, z: int;`

### Numeric Operations

- **Arithmetic:** Addition (`+`), subtraction (`-`), multiplication (`*`), division (`/`)
- **Scientific Notation:** Supports numbers like `2E2` (equals 200)
- **Parenthesized Expressions:** Full support for complex mathematical expressions

### Comparison and Logical Operations

- **Comparison:** `<`, `>`, `<=`, `>=`, `!=`, `==`
- **Logical:** `and`, `or`
- **Boolean Results:** Represented as integers (1 for true, 0 for false)

### Control Structures

- **Conditional Statements:**

  ```
  if (condition) {
      // code
  };

  if (condition) {
      // code
  } else {
      // alternative code
  };
  ```

- **Loops:**
  ```
  while (condition) do {
      // code
  };
  ```

### Functions

- **Declaration:**

  ```
  return_type function_name(param1: type, param2: type) [
      var local_var: type;
      {
          // function body
          return value;  // for non-void functions
      }
  ];
  ```

- **Types:** Supports `void`, `int`, and `float` return types
- **Parameters:** Typed parameter passing
- **Recursion:** Full support through function-specific memory allocation

### Input/Output

- **Printing:**
  ```
  print("Hello World!");
  print("Value:", variable);
  ```
- **String Literals:** Support for escape sequences like `\n`, `\t`
- **Multiple Values:** Print multiple expressions in a single statement

### Error Handling

- Lexical error detection
- Syntax error validation
- Semantic checking including type compatibility
- Runtime error handling

## Project Architecture

The QuackScript compiler is organized into several key components:

1. **Lexical and Syntax Analysis**

   - grammar.lark: Defines the language grammar using Lark parsing library

2. **Semantic Analysis**

   - QuackTransformer.py: Transforms the parse tree into an abstract syntax tree
   - SymbolTable.py: Manages variables, functions, and their types
   - SemanticCube.py: Validates operations between types

3. **Intermediate Code Generation**

   - QuackInterpreter.py: Generates intermediate representation
   - QuackQuadruple.py: Manages four-address code generation

4. **Memory Management**

   - MemoryManager.py: Handles memory allocation for variables and temporaries

5. **Execution**

   - VirtualMachine.py: Executes compiled QuackScript programs

6. **Compilation Pipeline**

   - QuackCompiler.py: Orchestrates the compilation process
   - Quackify.py: Command-line interface for compilation and execution

7. **Testing**
   - ParseTests.py: Tests for lexical and syntax analysis
   - RunAllTests.py: Runs all integration tests

## Memory Model

The memory is organized into three main segments:

- **Global Memory (1000-4999)**

  - Int: 1000-1999
  - Float: 2000-2999
  - Temporary Int: 3000-3999
  - Temporary Float: 4000-4999

- **Local Memory (5000-8999)**

  - Int: 5000-5999
  - Float: 6000-6999
  - Temporary Int: 7000-7999
  - Temporary Float: 8000-8999

- **Constant Memory (9000-11999)**
  - Int: 9000-9999
  - Float: 10000-10999
  - String: 11000-11999

## Running Tests

### Lexical and Syntax Tests

To test just the lexer and parser:

```bash
pytest -v ParseTests.py
```

### Full Compilation and Execution Tests

To run all tests that validate the entire compilation and execution pipeline:

```bash
python RunAllTests.py
```

## Compiling and Running QuackScript Programs

To compile and execute a QuackScript program:

```bash
python Quackify.py your_program.quack
```

This automatically compiles the program and executes it using the QuackScript virtual machine.

## QuackScript Program Structure

```
program ProgramName;

// Global variable declarations
var x: int;
var y: float = 3.14;
const PI: float = 3.14159;

// Function declarations
int factorial(n: int) [
    {
        if (n <= 1) {
            return 1;
        };
        return n * factorial(n - 1);
    }
];

// Main function - required
main {
    // Your code here
    print("Factorial of 5: ", factorial(5));
}
end
```

## Example Programs

The tests directory contains various example programs demonstrating language features:

- Basic arithmetic operations
- Variable declarations and assignments
- Conditional statements and loops
- Function calls and recursion
- Fibonacci sequence calculation
- Factorial computation

## Implementation Details

1. **Compilation Process:**

   - Lexical analysis tokenizes source code
   - Syntax analysis builds an abstract syntax tree
   - Semantic analysis verifies types and operations
   - Intermediate code generation produces quadruples
   - Final compilation creates an object file for the VM

2. **Virtual Machine:**

   - Reads compiled object file
   - Executes quadruples sequentially
   - Manages memory spaces for execution
   - Handles function calls and returns
   - Provides output through print operations

3. **Error Handling:**
   - Comprehensive error detection during compilation
   - Runtime error checking during execution
   - Detailed error messages for easier debugging

## Dependencies

- Python 3.6+
- Lark parsing library
- pytest (for running tests)

## Requirements

The full list of dependencies can be found in requirements.txt.
