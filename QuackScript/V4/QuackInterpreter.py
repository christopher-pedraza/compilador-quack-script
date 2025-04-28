class QuackInterpreter:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.current_container = "global"

    def evaluate_expression(self, expr_tree):
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

    def execute(self, ir):
        if isinstance(ir, tuple):
            ir_type = ir[0]
            if ir_type == "assign":
                var_name = ir[1]
                value = self.evaluate_expression(ir[2])
                self.symbol_table.update_variable(name=var_name, value=value, containerName=self.current_container)
            elif ir_type == "body_statements":
                for statement in ir[1]:
                    self.execute(statement)
            elif ir_type == "empty_body":
                pass
            elif ir_type == "cycle":
                condition = ir[1]
                body = ir[2]
                while self.evaluate_expression(condition):
                    self.execute(body)
            elif ir_type == "print":
                n = 1 if len(ir[1])==1 else len(ir[1])-1
                for i in range(n):
                    item = ir[1][i]
                    if isinstance(item, tuple) and item[0] == "id":
                        var_name = item[1]
                        value = self.symbol_table.get_variable(name=var_name, containerName=self.current_container)
                        print(value, end=" ")
                    elif isinstance(item, tuple) and item[0] == "cte_string":
                        value = item[1]
                        print(value, end=" ")
                    else:
                        value = self.evaluate_expression(item)
                        print(value, end=" ")
                print()
            elif ir_type == "condition_if":
                condition = ir[1]
                body = ir[2]
                if self.evaluate_expression(condition):
                    self.execute(body)
            elif ir_type == "condition_if_else":
                condition = ir[1]
                body_if = ir[2]
                body_else = ir[3]
                print(condition)
                print(body_if)
                print(body_else)
                if self.evaluate_expression(condition):
                    self.execute(body_if)
                else:
                    self.execute(body_else)
            else:
                raise ValueError(f"Unknown IR type: {ir_type}")
        else:
            raise ValueError(f"Unsupported IR: {ir}")