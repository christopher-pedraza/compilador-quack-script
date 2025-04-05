from lark import Lark, Transformer

# Definición de la gramática
grammar = """
    start: sum
    sum: product ("+" product)*
    product: NUMBER ("*" NUMBER)*
    %import common.NUMBER
    %import common.WS
    %ignore WS
"""

# Clase Transformer para realizar la evaluación
class EvalTransformer(Transformer):
    def sum(self, items):
        return sum(items)

    def product(self, items):
        result = 1
        for item in items:
            result *= item
        return result

    def NUMBER(self, token):
        return int(token)

# Creación del parser
parser = Lark(grammar, parser='lalr', transformer=EvalTransformer())

# Análisis y evaluación de una expresión
result = parser.parse("2 + 3 * 4 + 5")
print(result)  # Salida: 19
