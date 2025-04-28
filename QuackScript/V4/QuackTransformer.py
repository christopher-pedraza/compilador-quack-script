from lark import Lark, Transformer, v_args, Tree, Token



@v_args(inline=True)
class QuackTransformer(Transformer):
    def __init__(self, symbol_table):
        pass

    """
    id: CNAME
    """
    def id(self, value):
        return str(value)
    
    """
    cte_num: INT -> int
           | FLOAT -> float
    """
    def int(self, value):
        return int(value)
    
    def float(self, value):
        return float(value)

    """
    cte_string: ESCAPED_STRING
    """
    def cte_string(self, value):
        return ("cte_string", str(value)[1:-1]) 
    
    """
    factor: id -> factor_id
          | PLUS id -> positive_factor_id
          | MINUS id -> negative_factor_id
          | cte_num -> factor_cte_num
          | PLUS cte_num -> positive_cte_num
          | MINUS cte_num -> negative_cte_num
          | LPAREN expresion RPAREN -> parenthesis_expresion
    """
    def factor_id(self, id):
        return ("id", id)
    
    def positive_factor_id(self, id):
        return ("id", id)
    
    def negative_factor_id(self, id):
        return ("negative_id", id)
    
    def factor_cte_num(self, cte_num):
        return ("cte_num", cte_num)
    
    def positive_cte_num(self, plus, cte_num):
        return ("cte_num", cte_num)

    def negative_cte_num(self, minus, cte_num):
        return ("negative_cte_num", -cte_num)
    
    def parenthesis_expresion(self, lpar, expresion, rpar):
        return expresion
    
    """
    ?term: factor
         | factor (MULT factor)+ -> term_mult
         | factor (DIV factor)+ -> term_div
    """
    def term_mult(self, factor1, mult, factor2):
        return ("term_mult", factor1, factor2)
    
    def term_div(self, factor1, div, factor2):
        return ("term_div", factor1, factor2)

    """
    ?exp: term
        | term (PLUS term)+ -> exp_plus
        | term (MINUS term)+ -> exp_minus
    """
    def exp_plus(self, term1, plus, term2):
        return ("exp_plus", term1, term2)
    
    def exp_minus(self, term1, minus, term2):
        return ("exp_minus", term1, term2)
    
    """
    ?expresion: exp
              | exp comparison_op exp -> expresion_comparison_op
              | exp logic_cond exp -> expresion_logic_cond
    """
    def expresion_comparison_op(self, exp1, comparison_op, exp2):
        return ("expresion_comparison_op", exp1, comparison_op, exp2)
        
    def expresion_logic_cond(self, exp1, logic_cond, exp2):
        return ("expresion_logic_cond", exp1, logic_cond, exp2)
        
    """
    ?params: id COLON var_type -> param
           | id COLON var_type (COMMA id COLON var_type)+ -> params_list
    """
    def param(self, id, colon, type):
        return ["params", (id, type.value)]
    
    def params_list(self, id, colon, type, comma, *args):
        params = ["params", (id, type)] 
        for i in range(0, len(args)-1, 4):  # args contains (comma, param) pairs
            params.append((args[i], args[i + 2]))
        return params
    
    """
    ?var_type: "float" -> float_type
             | "int" -> int_type
    """
    def int_type(self):
        return "int"

    def float_type(self):
        return "float"

    """
    assign: id ASSIGN expresion SEMICOLON
    """
    def assign(self, id, assign, expresion, semicolon):
        return ("assign", id, expresion)
    
    """
    body: LBRACE RBRACE -> empty_body
    | LBRACE statement+ RBRACE -> body_statements
    """
    def empty_body(self, lbrace, rbrace):
        return ("empty_body",)
    
    def body_statements(self, lbrace, *statements):
        # Exclude the last RBRACE and return the statements as a list
        return ("body_statements", list(statements[:-1]))
    
    """
    print: PRINT LPAREN (expresion | cte_string) RPAREN SEMICOLON -> print_single
         | PRINT LPAREN (expresion | cte_string) (COMMA (expresion | cte_string))+ RPAREN SEMICOLON -> print_multiple
    """
    def print_single(self, print_, lpar, content, rpar, semicolon):
        return ("print", [content])
    
    def print_multiple(self, print_, lpar, content, *args):
        cont = [content]  # Start with the first content
        for i in range(0, len(args)-1, 2):
            cont.append(args[i + 1])
        return ("print", cont)

    """
    cycle: WHILE LPAREN expresion RPAREN DO body SEMICOLON
    """
    def cycle(self, while_, lpar, expresion, rpar, do, body, semicolon):
        return ("cycle", expresion, body)