from lark import Lark, Transformer, v_args

@v_args(inline=True)
class QuackTransformer(Transformer):
    def const_decl(self, const, id, colon, type, assign, expression, semicolon):
        return ("const_decl", id[0], expression)
    
    def var_decl(self, var, id, colon, type, assign, expression, semicolon):
        return ("var_decl", id[0], expression)

    def func_decl(self, func, id, lpar, params, rpar, colon, type, assign, block):
        return (id, params, block)
    
    def FLOAT(self, value):
        return float(value)
    
    def INT(self, value):
        return int(value)