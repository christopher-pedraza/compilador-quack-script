from lark import Lark, UnexpectedInput

# Load your grammar file or string
with open("grammar.lark") as f:
    grammar = f.read()

parser = Lark(grammar, start="start", parser="lalr")


def parse_test(program_text):
    try:
        parser.parse(program_text)
        print("✅ Parsed successfully.")
        return True
    except UnexpectedInput as e:
        print(f"❌ Parse error: {e}")
        return False


# ========== TEST CASES ========== #


def test_basic_arithmetic():
    program = """
    program Test;
    var x: int;
    main {
        x = 3 + 4 * (5 - 2);
    }
    end
    """
    assert parse_test(program)


def test_logic_ops():
    program = """
    program Test;
    var result: int;
    main {
        result = (5 > 3) or (4 == 5) and (6 <= 7);
    }
    end
    """
    assert parse_test(program)


def test_if_else():
    program = """
    program Test;
    var x: int = 10;
    main {
        if (x > 5) {
            print("Greater than 5");
        } else {
            print("Less than or equal to 5");
        };
    }
    end
    """
    assert parse_test(program)


def test_while_loop():
    program = """
    program Test;
    var i: int = 0;
    main {
        while (i < 5) do {
            print(i);
            i = i + 1;
        };
    }
    end
    """
    assert parse_test(program)


def test_print_statements():
    program = """
    program Test;
    main {
        print("Hello", "World", "!");
        print(42);
        print(3.14159);
    }
    end
    """
    assert parse_test(program)


def test_function_call():
    program = """
    program Test;
    var sum: int;

    int add(a: int, b: int) [
        {
            return a + b;
        }
    ];

    main {
        sum = add(2, 3);
    }
    end
    """
    assert parse_test(program)


def test_nested_function_call():
    program = """
    program Test;
    var result: int;

    int square(x: int) [
        {
            return x * x;
        }
    ];

    int add(a: int, b: int) [
        {
            return a + b;
        }
    ];

    main {
        result = square(add(2, 3));
    }
    end
    """
    assert parse_test(program)


def test_var_decls():
    program = """
    program Test;
    var a: int;
    var b, c: float = 3.14;
    var d: int = 5;

    main {
    }
    end
    """
    assert parse_test(program)


def test_const_decls():
    program = """
    program Test;
    const PI: float = 3.14159;
    const MAX: int = 100;

    main {
    }
    end
    """
    assert parse_test(program)


def test_return_statement():
    program = """
    program Test;
    var value: int;

    int get_value() [
        {
            return 42;
        }
    ];

    main {
        value = get_value();
    }
    end
    """
    assert parse_test(program)


def test_minimal_functions():
    program = """
    program Test;

    void greet() [
        {
            print("Hello world!");
        }
    ];

    int get_answer() [
        {
            return 42;
        }
    ];

    main {
        greet();
    }
    end
    """
    assert parse_test(program)


def test_empty_program():
    program = """
    program Test;

    main {
    }
    end
    """
    assert parse_test(program)


def test_negative_numbers():
    program = """
    program Test;
    var x: int = -5;
    var y: int = (+x - 10);

    main {
    }
    end
    """
    assert parse_test(program)


def test_mixed_types():
    program = """
    program Test;
    var a: int = 3 + 4.5;
    var b: float = 2.5 * 3;

    main {
    }
    end
    """
    assert parse_test(program)


def test_comments_and_whitespace():
    program = """
    // This is a comment
    program Test; // Another comment
    var x : int = 5;

    main {
        print(x); // Print x
    }
    end
    """
    assert parse_test(program)


def test_fibonacci():
    program = """
    program Fibonacci;

    void fibonacci_iterativo(n: int) [
        var a, b, tmp, count: int;
        {
          if (n <= 0) {
            print("Introduce un numero entero positivo!");
            return -1;
          };

          a = 0;
          b = 1;
          count = 0;

          while (count < n) do {
            print("->", a);
            tmp = a;
            a = b;
            b = tmp + b;
            count = count + 1;
          };
        }
    ];

    int fibonacci_recursivo(n: int) [
        var fib1, fib2: int;
        {
          if (n < 0) {
            return -1;
          };
          if (n == 0) {
            return 0;
          };
          if (n == 1) {
            return 1;
          };
          if (n > 1) {
            fib1 = fibonacci_recursivo(n - 1);
            fib2 = fibonacci_recursivo(n - 2);
            return fib1 + fib2;
          };
        }
    ];

    void fibonacci_recursivo_secuencia(n: int) [
      var i: int = 0;
      {
        if (n <= 0) {
          print("Introduce un numero entero positivo!");
        }
        else {
          while (i < n) do {
            print("->", fibonacci_recursivo(i));
            i = i + 1;
          };
        };
      }
    ];

    main {
        print("Fibonacci iterativo:");
        fibonacci_iterativo(5);
        print("\\n");
        print("Fibonacci recursivo:");
        fibonacci_recursivo_secuencia(5);
        print("\\n");
    }
    end
    """
    assert parse_test(program)
