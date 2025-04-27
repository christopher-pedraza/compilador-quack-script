from lark import Lark, Transformer, v_args, Tree, Token



@v_args(inline=True)
class QuackTransformer(Transformer):
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.current_container = "global"  # Start in the global scope

    def evaluate_expression(self, expr_tree):
        """
        Recursively evaluates an expression tree.
        """
        # print("Evaluating:", expr_tree)
        if isinstance(expr_tree, tuple):
            expr_type = expr_tree[0]
            if expr_type == "id":  # Variable reference
                var_name = expr_tree[1]
                return self.symbol_table.get_variable(name=var_name, containerName=self.current_container)
            elif expr_type == "negative_id":  # Negative variable reference
                var_name = expr_tree[1]
                return -self.symbol_table.get_variable(name=var_name, containerName=self.current_container)
            elif expr_type == "cte_num":  # Constant number
                return expr_tree[1]
            elif expr_type == "negative_cte_num":  # Negative constant number
                return expr_tree[1]
            elif expr_type == "term_mult":  # Multiplication
                left = self.evaluate_expression(expr_tree[1])
                right = self.evaluate_expression(expr_tree[2])
                return left * right
            elif expr_type == "term_div":  # Division
                left = self.evaluate_expression(expr_tree[1])
                right = self.evaluate_expression(expr_tree[2])
                if right == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                return left / right
            elif expr_type == "exp_plus":  # Addition
                left = self.evaluate_expression(expr_tree[1])
                right = self.evaluate_expression(expr_tree[2])
                return left + right
            elif expr_type == "exp_minus":  # Subtraction
                left = self.evaluate_expression(expr_tree[1])
                right = self.evaluate_expression(expr_tree[2])
                return left - right
            elif expr_type == "expresion_comparison_op":  # Comparison
                left = self.evaluate_expression(expr_tree[1])
                op = expr_tree[2]
                right = self.evaluate_expression(expr_tree[3])
                if op == "==":
                    return left == right
                elif op == "!=":
                    return left != right
                elif op == "<":
                    return left < right
                elif op == "<=":
                    return left <= right
                elif op == ">":
                    return left > right
                elif op == ">=":
                    return left >= right
                else:
                    raise ValueError(f"Unknown comparison operator: {op}")
            elif expr_type == "expresion_logic_cond":  # Logical operation
                left = self.evaluate_expression(expr_tree[1])
                op = expr_tree[2]
                right = self.evaluate_expression(expr_tree[3])
                if op == "and":
                    return left and right
                elif op == "or":
                    return left or right
                else:
                    raise ValueError(f"Unknown logical operator: {op}")
        else:
            raise ValueError(f"Unsupported expression type: {expr_tree}")

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
        # Evaluate the expression
        evaluated_expresion = self.evaluate_expression(expresion)
        # Update the symbol table with the new value
        self.symbol_table.update_variable(name=id, value=evaluated_expresion, containerName=self.current_container)
        # return the assign as it was received (Tree(Token('RULE', 'assign'),
        # ['a', Token('ASSIGN', '='), ('cte_num', 1), Token('SEMICOLON', ';')]))
        return (Tree(Token('RULE', 'assign'), [id, Token('ASSIGN', '='), expresion, Token('SEMICOLON', ';')]))

    
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
        print("PRINTING:")
        print(content)
        return ("print", content)
    
    def print_multiple(self, print_, lpar, content, *args):
        print("PRINTING:")
        odd_args = args[1:len(args)-1:2]  # This slices the args list to get elements at odd indexes
        print(content, *odd_args)
        return ("print", content, odd_args)

    """
    cycle: WHILE LPAREN expresion RPAREN DO body SEMICOLON
    """
    def cycle(self, while_, lpar, expresion, rpar, do, body, semicolon):
        # Initial evaluation of the condition
        evaluated_expression = self.evaluate_expression(expresion)

        # Loop while the condition is True
        while evaluated_expression:
            # Execute the body of the loop
            print("BODY CONTENT:", body[1][1])
            for statement in body[1]:  # body[1] contains the list of statements
                self.transform(statement)

            # Re-evaluate the condition after executing the body
            evaluated_expression = self.evaluate_expression(expresion)
            # print("Re-evaluated condition:", evaluated_expression)

        return ("cycle", expresion, body)