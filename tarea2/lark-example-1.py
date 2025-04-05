from lark import Lark, Token, Tree

# Define the grammar
grammar = """
    start: statement+

    statement: var_decl
             | func_decl

    var_decl: "var" NAME "=" expr ";"
    func_decl: "func" NAME "(" [params] ")" block

    params: NAME ("," NAME)*
    block: "{" statement* "}"
    expr: NUMBER -> number
        | NAME   -> var

    NAME: /[a-zA-Z_][a-zA-Z0-9_]*/

    %import common.SIGNED_NUMBER -> NUMBER
    %import common.WS
    %ignore WS
"""

# Create the parser
parser = Lark(grammar, parser='lalr')
    
# Example input code
code = """
var x = -5e10;
func add(a, b) {
    var result = a;
}
"""

# Parse and print the tree
parse_tree = parser.parse(code)
print(parse_tree.pretty())

# Show all tokens
tokens = list(parser.lex(code))
print("\nTokens:")
for token in tokens:
    print(f"{token.type}: {token.value}")
