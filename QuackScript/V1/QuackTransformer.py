from lark import Lark, Transformer, v_args, Tree, Token
from SymbolTable import SymbolTable
from TransformerClasses import (
    IdNode,
    CteNumNode,
    CteStringNode,
    ArithmeticOpNode,
    UnaryOpNode,
    MultiplicativeOpNode,
    ComparisonNode,
    LogicalAndNode,
    LogicalOrNode,
    AssignNode,
    BodyNode,
    PrintNode,
    WhileNode,
    IfNode,
    IfElseNode,
    VarDeclNode,
    ParamsNode,
    ParamNode,
    FunctionDeclNode,
    FuncCallNode,
    ProgramNode,
)


@v_args(inline=True)
class QuackTransformer(Transformer):
    def __init__(self):
        self.symbol_table = None

    """
    id: CNAME
    """

    def id(self, value):
        return IdNode(name=str(value))

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
        return CteStringNode(value=str(value)[1:-1])

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
        return id

    def positive_factor_id(self, id):
        return id

    def negative_factor_id(self, minus, id):
        return ArithmeticOpNode(op="-", left=CteNumNode(0), right=id)

    def factor_cte_num(self, cte_num):
        return CteNumNode(value=cte_num)

    def positive_cte_num(self, plus, cte_num):
        return CteNumNode(value=cte_num)

    def negative_cte_num(self, minus, cte_num):
        return ArithmeticOpNode(op="-", left=CteNumNode(0), right=CteNumNode(cte_num))

    def parenthesis_expresion(self, lpar, expresion, rpar):
        return expresion

    """
    ?term: factor
        | term MULT factor -> term_mult
        | term DIV factor -> term_div
    """

    def term_mult(self, term, mult, factor):
        return MultiplicativeOpNode(op="*", left=term, right=factor)

    def term_div(self, term, div, factor):
        return MultiplicativeOpNode(op="/", left=term, right=factor)

    """
    ?exp: term
        | exp PLUS term -> exp_plus
        | exp MINUS term -> exp_minus
    """

    def exp_plus(self, exp, plus, term):
        return ArithmeticOpNode(op="+", left=exp, right=term)

    def exp_minus(self, exp, minus, term):
        return ArithmeticOpNode(op="-", left=exp, right=term)

    """
    ?comparison: exp
               | exp comparison_op exp -> binary_comparison
    """

    def binary_comparison(self, exp1, comparison_op, exp2):
        return ComparisonNode(op=comparison_op, left=exp1, right=exp2)

    """
    ?logical_and: comparison
                | logical_and AND comparison -> binary_logical_and
    """

    def binary_logical_and(self, logical_and, and_, comparison):
        return LogicalAndNode(op="and", left=logical_and, right=comparison)

    """
    ?logical_or: logical_and
               | logical_or OR logical_and -> binary_logical_or
    """

    def binary_logical_or(self, logical_or, or_, logical_and):
        return LogicalOrNode(op="or", left=logical_or, right=logical_and)

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
        return AssignNode(var_name=id.name, expr=expresion)

    """
    body: LBRACE RBRACE -> empty_body
    | LBRACE statement+ RBRACE -> body_statements
    """

    def empty_body(self, lbrace, rbrace):
        return BodyNode(statements=[])

    def body_statements(self, lbrace, *statements):
        return BodyNode(statements=list(statements[:-1]))

    """
    print: PRINT LPAREN (expresion | cte_string) RPAREN SEMICOLON -> print_single
         | PRINT LPAREN (expresion | cte_string) (COMMA (expresion | cte_string))+ RPAREN SEMICOLON -> print_multiple
    """

    def print_single(self, print_, lpar, content, rpar, semicolon):
        return PrintNode(values=[content])

    def print_multiple(self, print_, lpar, content, *args):
        cont = [content]  # Start with the first content
        for i in range(1, len(args) - 2, 2):
            cont.append(args[i])
        return PrintNode(values=cont)

    """
    cycle: WHILE LPAREN expresion RPAREN DO body SEMICOLON
    """

    def cycle(self, while_, lpar, expresion, rpar, do, body, semicolon):
        return WhileNode(condition=expresion, body=body)

    """
    condition: IF LPAREN expresion RPAREN body SEMICOLON -> condition_if
             | IF LPAREN expresion RPAREN body ELSE body SEMICOLON -> condition_if_else
    """

    def condition_if(self, if_, lpar, expresion, rpar, body, semicolon):
        return IfNode(condition=expresion, then_body=body)

    def condition_if_else(self, if_, lpar, expresion, rpar, body1, else_, body2, semicolon):
        return IfElseNode(condition=expresion, then_body=body1, else_body=body2)

    """
    const_decl: CONST id COLON var_type ASSIGN expresion SEMICOLON
    """

    def const_decl(self, const, id, colon, var_type, assign, expresion, semicolon):
        return VarDeclNode(names=[id], var_type=var_type, init_value=expresion, category="const")

    """
    var_decl: VAR id COLON var_type SEMICOLON -> var_single_decl_no_assign
            | VAR id COLON var_type ASSIGN expresion SEMICOLON -> var_single_decl_assign
            | VAR id (COMMA id)+ COLON var_type SEMICOLON -> var_multi_decl_no_assign
            | VAR id (COMMA id)+ COLON var_type ASSIGN expresion SEMICOLON -> var_multi_decl_assign
    """

    def var_single_decl_no_assign(self, var, id, colon, var_type, semicolon):
        return VarDeclNode(names=[id], var_type=var_type, category="var")

    def var_single_decl_assign(self, var, id, colon, var_type, assign, expresion, semicolon):
        return VarDeclNode(names=[id], var_type=var_type, init_value=expresion, category="var")

    def var_multi_decl_no_assign(self, var, id, *args):
        ids = [id]
        for i in range(0, len(args) - 1, 2):
            ids.append(args[i - 1])
        return VarDeclNode(names=ids, var_type=args[-1], category="var")

    def var_multi_decl_assign(self, var, id, *args):
        ids = [id]
        for i in range(1, len(args) - 5, 2):
            ids.append(args[i])
        return VarDeclNode(names=ids, var_type=args[-4], init_value=args[-2], category="var")

    """
    ?params: id COLON var_type -> param
           | id COLON var_type (COMMA id COLON var_type)+ -> params_list
    """

    def param(self, id, colon, type_):
        return ParamsNode(params=[ParamNode(name=id, param_type=type_)])

    def params_list(self, id, colon, type_, comma, *args):
        params = [ParamNode(name=id, param_type=type_)]
        for i in range(0, len(args) - 1, 4):
            params.append(ParamNode(name=args[i], param_type=args[i + 2]))
        return ParamsNode(params=params)

    """
    function: VOID id LPAREN RPAREN LBRACKET body RBRACKET SEMICOLON -> function_no_params_no_var_decl
            | VOID id LPAREN params RPAREN LBRACKET body RBRACKET SEMICOLON -> function_no_var_decl
            | VOID id LPAREN params RPAREN LBRACKET var_decl+ body RBRACKET SEMICOLON -> function_params_var_decl
            | VOID id LPAREN RPAREN LBRACKET var_decl+ body RBRACKET SEMICOLON -> function_no_params
    """

    def function_no_params_no_var_decl(self, void, id, lpar, rpar, lbracket, body, rbracket, semicolon):
        return FunctionDeclNode(name=id, params=ParamsNode(params=[]), body=body, var_decls=[])

    def function_no_var_decl(self, void, id, lpar, params, rpar, lbracket, body, rbracket, semicolon):
        return FunctionDeclNode(name=id, params=params, body=body, var_decls=[])

    def function_params_var_decl(self, void, id, lpar, params, rpar, lbracket, *args):
        body = args[-3]
        var_decls = list(args[:-3])
        return FunctionDeclNode(name=id, params=params, body=body, var_decls=var_decls)

    def function_no_params(self, void, id, lpar, rpar, lbracket, *args):
        body = args[-3]
        var_decls = list(args[:-3])
        return FunctionDeclNode(name=id, params=ParamsNode(params=[]), body=body, var_decls=var_decls)

    """
    func_call: id LPAREN RPAREN SEMICOLON -> func_call_no_params
             | id LPAREN expresion RPAREN SEMICOLON -> func_call_single_param
             | id LPAREN expresion (COMMA expresion)+ RPAREN SEMICOLON -> func_call_multiple_params
    """

    def func_call_no_params(self, id, lpar, rpar, semicolon):
        return FuncCallNode(name=id, args=[])

    def func_call_single_param(self, id, lpar, expresion, rpar, semicolon):
        return FuncCallNode(name=id, args=[expresion])

    def func_call_multiple_params(self, id, lpar, expresion, *args):
        params = [expresion]
        for i in range(1, len(args) - 1, 2):
            params.append(args[i])
        return FuncCallNode(name=id, args=params)

    """
    program: program_pt1 program_pt2 MAIN body END -> program_no_decl
           | program_pt1 program_pt2 (const_decl | var_decl)+ MAIN body END -> program_decl_no_func
           | program_pt1 program_pt2 function+ MAIN body END -> program_func_no_decl
           | program_pt1 program_pt2 (const_decl | var_decl)+ function+ MAIN body END -> program_decl_func
    """

    def program_no_decl(self, program_pt1, program_pt2, main, body, end):
        return ProgramNode(name=program_pt2, global_decls=[], functions=[], main_body=body)

    def program_decl_no_func(self, program_pt1, program_pt2, *args):
        body = args[-2]
        decls = []
        for i in range(0, len(args) - 3):
            decls.append(args[i])
        return ProgramNode(name=program_pt2, global_decls=decls, functions=[], main_body=body)

    def program_func_no_decl(self, program_pt1, program_pt2, *args):
        body = args[-2]
        funcs = []
        for i in range(0, len(args) - 3):
            funcs.append(args[i])
        return ProgramNode(name=program_pt2, global_decls=[], functions=funcs, main_body=body)

    def program_decl_func(self, program_pt1, program_pt2, *args):
        id = program_pt2
        body = args[-2]
        decls = []
        funcs = []
        for i in range(0, len(args) - 3):
            item = args[i]
            if isinstance(item, VarDeclNode):
                decls.append(item)
            elif isinstance(item, FunctionDeclNode):
                funcs.append(item)
        return ProgramNode(name=program_pt2, global_decls=decls, functions=funcs, main_body=body)

    """
    ?program_pt1: PROGRAM
    ?program_pt2: id SEMICOLON
    """

    def program_pt1(self, program):
        self.symbol_table = SymbolTable()
        return program

    def program_pt2(self, id, semicolon):
        self.symbol_table.create_global_container(id.name)
        return id.name
