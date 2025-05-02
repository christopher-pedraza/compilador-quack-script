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
        return ("negative_cte_num", cte_num)
    
    def parenthesis_expresion(self, lpar, expresion, rpar):
        return expresion
    
    """
    ?term: factor
         | factor (MULT factor)+ -> term_mult
         | factor (DIV factor)+ -> term_div
    """
    # def term_mult(self, factor1, mult, factor2):
    #     return ("term_mult", factor1, factor2)
    def term_mult(self, factor1, *args):
        factors = [factor1]
        for i in range(1, len(args), 2):
            factors.append(args[i])
        # Create a nested structure for multiplication
        result = factors[0]
        for factor in factors[1:]:
            result = ("term_mult", result, factor)
        return result
    
    # def term_div(self, factor1, div, factor2):
    #     return ("term_div", factor1, factor2)
    def term_div(self, factor1, *args):
        factors = [factor1]
        for i in range(1, len(args), 2):
            factors.append(args[i])
        # Create a nested structure for division
        result = factors[0]
        for factor in factors[1:]:
            result = ("term_div", result, factor)
        return result

    """
    ?exp: term
        | term (PLUS term)+ -> exp_plus
        | term (MINUS term)+ -> exp_minus
    """
    # def exp_plus(self, term1, plus, term2):
    #     return ("exp_plus", term1, term2)
    def exp_plus(self, term1, *args):
        terms = [term1]
        for i in range(1, len(args), 2):
            terms.append(args[i])
        # Create a nested structure for addition
        result = terms[0]
        for term in terms[1:]:
            result = ("exp_plus", result, term)
        return result
    
    # def exp_minus(self, term1, minus, term2):
    #     return ("exp_minus", term1, term2)
    def exp_minus(self, term1, *args):
        terms = [term1]
        for i in range(1, len(args), 2):
            terms.append(args[i])
        # Create a nested structure for subtraction
        result = terms[0]
        for term in terms[1:]:
            result = ("exp_minus", result, term)
        return result

    
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
    program: PROGRAM id SEMICOLON MAIN body END -> program_no_decl
           | PROGRAM id SEMICOLON (const_decl | var_decl)+ MAIN body END -> program_decl_no_func
           | PROGRAM id SEMICOLON function+ MAIN body END -> program_func_no_decl
           | PROGRAM id SEMICOLON (const_decl | var_decl)+ function+ MAIN body END -> program_decl_func
    """
    def program_no_decl(self, program, id, semicolon, main, body, end):
        return ("program", id, [], [], body)
     
    def program_decl_no_func(self, program, id, semicolon, *args):
        body = args[-2]
        decls = []
        for i in range(0, len(args)-3):
            decls.append(args[i])
        return ("program", id, decls, [], body)
    
    def program_func_no_decl(self, program, id, semicolon, *args):
        body = args[-2]
        funcs = []
        for i in range(0, len(args)-3):
            funcs.append(args[i])
        return ("program", id, [], funcs, body)
    
    def program_decl_func(self, program, id, semicolon, *args):
        body = args[-2]
        decls = []
        funcs = []
        for i in range(0, len(args)-3):
            if args[i][0] == "var_decl":
                decls.append(args[i])
            else:
                funcs.append(args[i])
        return ("program", id, decls, funcs, body)