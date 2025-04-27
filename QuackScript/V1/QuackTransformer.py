from lark import Lark, Transformer, v_args

@v_args(inline=True)
class QuackTransformer(Transformer):
    def const_decl(self, const, id, colon, type, assign, expression, semicolon):
        return ("const_decl", id, expression)
    
    def var_decl(self, var, id, colon, type, assign, expression, semicolon):
        return ("var_decl", id, expression)

    def func_decl(self, func, id, lpar, params, rpar, colon, type, assign, block):
        return (id, params, block)
    
    def FLOAT(self, value):
        return float(value)
    
    def INT(self, value):
        return int(value)
    
    def CTE_STRING(self, value):
        return str(value[1:-1])
    
    # print: PRINT LPAREN (expresion | CTE_STRING) (COMMA (expresion | CTE_STRING))* RPAREN SEMICOLON
    def print(self, PRINT, LPAREN, expresion, CTE_STRING, *args):
        print(CTE_STRING)
        return ("print", CTE_STRING, args)