from lark import Lark, Transformer, v_args


@v_args(inline=True)
class QuackTransformer(Transformer):
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.current_container = "global"  # Start in the global scope

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
        return str(value[1:-1])
    
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
        return self.symbol_table.get_variable(name=id, containerName=self.current_container)
    
    def positive_factor_id(self, id):
        return self.symbol_table.get_variable(name=id, containerName=self.current_container)
    
    def negative_factor_id(self, id):
        return -self.symbol_table.get_variable(name=id, containerName=self.current_container)
    
    def factor_cte_num(self, cte_num):
        return cte_num
    
    def positive_cte_num(self, plus, cte_num):
        return cte_num

    def negative_cte_num(self, minus, cte_num):
        return -cte_num 
    
    def parenthesis_expresion(self, lpar, expresion, rpar):
        return expresion
    
    def term_mult(self, factor1, mult, factor2):
        return factor1 * factor2
    
    def term_div(self, factor1, div, factor2):
        return factor1 / factor2

    """
    ?exp: term
        | term (PLUS term)+ -> exp_plus
        | term (MINUS term)+ -> exp_minus
    """
    def exp_plus(self, term1, plus, term2):
        return term1 + term2
    
    def exp_minus(self, term1, minus, term2):
        return term1 - term2
    
    """
    ?expresion: exp
              | exp comparison_op exp -> expresion_comparison_op
              | exp logic_cond exp -> expresion_logic_cond
    """
    def expresion_comparison_op(self, exp1, comparison_op, exp2):
        if comparison_op == "==":
            return exp1 == exp2
        elif comparison_op == "!=":
            return exp1 != exp2
        elif comparison_op == "<":
            return exp1 < exp2
        elif comparison_op == "<=":
            return exp1 <= exp2
        elif comparison_op == ">":
            return exp1 > exp2
        elif comparison_op == ">=":
            return exp1 >= exp2
        else:
            raise ValueError(f"Unknown type condition: {comparison_op}")
        
    def expresion_logic_cond(self, exp1, logic_cond, exp2):
        if logic_cond == "and":
            return exp1 and exp2
        elif logic_cond == "or":
            return exp1 or exp2
        else:
            raise ValueError(f"Unknown logic condition: {logic_cond}")
        
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
        # Update the symbol table with the new value
        self.symbol_table.update_variable(name=id, value=expresion, containerName=self.current_container)
        return ("assign", id, expresion)
    
    """
    body: LBRACE RBRACE -> empty_body
    | LBRACE statement+ RBRACE -> body_statements
    """
    def empty_body(self, lbrace, rbrace):
        return ("empty_body",)
    
    def body_statements(self, lbrace, statements, rbrace):
        return ("body_statements", statements)
    
    """
    print: PRINT LPAREN (expresion | cte_string) RPAREN SEMICOLON -> print_single
         | PRINT LPAREN (expresion | cte_string) (COMMA (expresion | cte_string))+ RPAREN SEMICOLON -> print_multiple
    """
    def print_single(self, print_, lpar, content, rpar, semicolon):
        print(content)
        return ("print", content)
    
    def print_multiple(self, print_, lpar, content, *args):
        odd_args = args[1:len(args)-1:2]  # This slices the args list to get elements at odd indexes
        print(content, *odd_args)
        return ("print", content, odd_args)
    