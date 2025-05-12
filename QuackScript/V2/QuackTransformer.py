from lark import Lark, Transformer, v_args, Tree, Token
from SymbolTable import SymbolTable


@v_args(inline=True)
class QuackTransformer(Transformer):
    def __init__(self):
        self.symbol_table = None

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
    
    def negative_factor_id(self, minus, id):
        return ("exp_minus", ("cte_num", 0), ("id", id))
    
    def factor_cte_num(self, cte_num):
        return ("cte_num", cte_num)
    
    def positive_cte_num(self, plus, cte_num):
        return ("cte_num", cte_num)

    def negative_cte_num(self, minus, cte_num):
        return ("negative_cte_num", cte_num)
    
    def parenthesis_expresion(self, lpar, expresion, rpar):
        return expresion
    
    """
    ?term: factor
        | term MULT factor -> term_mult
        | term DIV factor -> term_div
    """
    def term_mult(self, term, mult, factor):
        return ("term_mult", term, factor)
    
    def term_div(self, term, div, factor):
        return ("term_div", term, factor)

    """
    ?exp: term
        | exp PLUS term -> exp_plus
        | exp MINUS term -> exp_minus
    """
    def exp_plus(self, exp, plus, term):
        return ("exp_plus", exp, term)
    
    def exp_minus(self, exp, minus, term):
        return ("exp_minus", exp, term)

    """
    ?comparison: exp
               | exp comparison_op exp -> binary_comparison
    """
    def binary_comparison(self, exp1, comparison_op, exp2):
        return ("binary_comparison", exp1, comparison_op, exp2)
    
    """
    ?logical_and: comparison
                | logical_and AND comparison -> binary_logical_and
    """
    def binary_logical_and(self, logical_and, and_, comparison):
        return ("binary_logical_and", logical_and, comparison)

    """
    ?logical_or: logical_and
               | logical_or OR logical_and -> binary_logical_or
    """
    def binary_logical_or(self, logical_or, or_, logical_and):
        return ("binary_logical_or", logical_or, logical_and)
    
    """
    comparison_op: GT | LT | NE | EE | GTE | LTE
    """
    def comparison_op(self, value):
        return str(value)
    
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
        for i in range(1, len(args)-2, 2):
            cont.append(args[i])
        return ("print", cont)

    """
    cycle: WHILE LPAREN expresion RPAREN DO body SEMICOLON
    """
    def cycle(self, while_, lpar, expresion, rpar, do, body, semicolon):
        return ("cycle", expresion, body)
    
    """
    condition: IF LPAREN expresion RPAREN body SEMICOLON -> condition_if
             | IF LPAREN expresion RPAREN body ELSE body SEMICOLON -> condition_if_else
    """
    def condition_if(self, if_, lpar, expresion, rpar, body, semicolon):
        return ("condition_if", expresion, body)
    
    def condition_if_else(self, if_, lpar, expresion, rpar, body1, else_, body2, semicolon):
        return ("condition_if_else", expresion, body1, body2)
    
    """
    const_decl: CONST id COLON var_type ASSIGN expresion SEMICOLON
    """
    def const_decl(self, const, id, colon, var_type, assign, expresion, semicolon):
        return ("var_decl", [id], var_type, expresion, "const")
    
    """
    var_decl: VAR id COLON var_type SEMICOLON -> var_single_decl_no_assign
            | VAR id COLON var_type ASSIGN expresion SEMICOLON -> var_single_decl_assign
            | VAR id (COMMA id)+ COLON var_type SEMICOLON -> var_multi_decl_no_assign
            | VAR id (COMMA id)+ COLON var_type ASSIGN expresion SEMICOLON -> var_multi_decl_assign
    """
    def var_single_decl_no_assign(self, var, id, colon, var_type, semicolon):
        return ("var_decl", [id], var_type, None, "var")
    
    def var_single_decl_assign(self, var, id, colon, var_type, assign, expresion, semicolon):
        return ("var_decl", [id], var_type, expresion, "var")
    
    def var_multi_decl_no_assign(self, var, id, *args):
        ids = [id]
        for i in range(0, len(args)-1, 2):
            ids.append(args[i - 1])
        return ("var_decl", ids, args[-1], None, "var")
    
    def var_multi_decl_assign(self, var, id, *args):
        ids = [id]
        for i in range(1, len(args)-5, 2):
            ids.append(args[i])
        return ("var_decl", ids, args[-4], args[-2], "var")
    
    """
    ?params: id COLON var_type -> param
           | id COLON var_type (COMMA id COLON var_type)+ -> params_list
    """
    def param(self, id, colon, type):
        return ("params", [(id, type)])
    
    def params_list(self, id, colon, type, comma, *args):
        params = ("params", [(id, type)])
        for i in range(0, len(args)-1, 4):
            params[1].append((args[i], args[i + 2]))
        return params
    
    """
    function: VOID id LPAREN RPAREN LBRACKET body RBRACKET SEMICOLON -> function_no_params_no_var_decl
            | VOID id LPAREN params RPAREN LBRACKET body RBRACKET SEMICOLON -> function_no_var_decl
            | VOID id LPAREN params RPAREN LBRACKET var_decl+ body RBRACKET SEMICOLON -> function_params_var_decl
            | VOID id LPAREN RPAREN LBRACKET var_decl+ body RBRACKET SEMICOLON -> function_no_params
    """
    def function_no_params_no_var_decl(self, void, id, lpar, rpar, lbracket, body, rbracket, semicolon):
        return ("function_decl", id, [], body, [])
    
    def function_no_var_decl(self, void, id, lpar, params, rpar, lbracket, body, rbracket, semicolon):
        return ("function_decl", id, params, body, [])
    
    def function_params_var_decl(self, void, id, lpar, params, rpar, lbracket, *args):
        body = args[-3]
        var_decl = []
        for i in range(0, len(args)-3):
            var_decl.append(args[i])
        return ("function_decl", id, params, body, var_decl)
    
    def function_no_params(self, void, id, lpar, rpar, lbracket, *args):
        body = args[-3]
        var_decl = []
        for i in range(0, len(args)-3):
            var_decl.append(args[i])
        return ("function_decl", id, [], body, var_decl)

    """
    func_call: id LPAREN RPAREN SEMICOLON -> func_call_no_params
             | id LPAREN expresion RPAREN SEMICOLON -> func_call_single_param
             | id LPAREN expresion (COMMA expresion)+ RPAREN SEMICOLON -> func_call_multiple_params
    """
    def func_call_no_params(self, id, lpar, rpar, semicolon):
        return ("func_call", id, [])
    
    def func_call_single_param(self, id, lpar, expresion, rpar, semicolon):
        return ("func_call", id, [expresion])
    
    def func_call_multiple_params(self, id, lpar, expresion, *args):
        params = [expresion]
        for i in range(1, len(args)-1, 2):
            params.append(args[i])
        return ("func_call", id, params)
        
    """
    program: program_pt1 program_pt2 MAIN body END -> program_no_decl
           | program_pt1 program_pt2 (const_decl | var_decl)+ MAIN body END -> program_decl_no_func
           | program_pt1 program_pt2 function+ MAIN body END -> program_func_no_decl
           | program_pt1 program_pt2 (const_decl | var_decl)+ function+ MAIN body END -> program_decl_func
    """
    def program_no_decl(self, program_pt1, program_pt2, main, body, end):
        id = program_pt2
        return ("program", id, [], [], body)
     
    def program_decl_no_func(self, program_pt1, program_pt2, *args):
        id = program_pt2
        body = args[-2]
        decls = []
        for i in range(0, len(args)-3):
            decls.append(args[i])
        return ("program", id, decls, [], body)
    
    def program_func_no_decl(self, program_pt1, program_pt2, *args):
        id = program_pt2
        body = args[-2]
        funcs = []
        for i in range(0, len(args)-3):
            funcs.append(args[i])
        return ("program", id, [], funcs, body)
    
    def program_decl_func(self, program_pt1, program_pt2, *args):
        id = program_pt2
        body = args[-2]
        decls = []
        funcs = []
        for i in range(0, len(args)-3):
            if args[i][0] == "var_decl":
                decls.append(args[i])
            else:
                funcs.append(args[i])
        return ("program", id, decls, funcs, body)
    
    """
    ?program_pt1: PROGRAM
    ?program_pt2: id SEMICOLON
    """
    def program_pt1(self, program):
        self.symbol_table = SymbolTable()
        return program
    
    def program_pt2(self, id, semicolon):
        self.symbol_table.create_global_container(id)
        return id