from SemanticCube import SemanticCube
from Exceptions import UnsupportedOperationError, \
                       DivisionByZeroError, \
                       UnsupportedExpressionError, \
                       TypeMismatchError, \
                       UnknownIRTypeError

class QuackInterpreter:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.current_container = "global"
        self.semantic_cube = SemanticCube()

    def evaluate_expression(self, expr_tree):
        if isinstance(expr_tree, tuple):
            expr_type = expr_tree[0]

            #############################################################################################################
            if expr_type == "id":  # Variable reference
                var_name = expr_tree[1]
                return self.symbol_table.get_variable(name=var_name, containerName=self.current_container)
            
            #############################################################################################################
            elif expr_type == "negative_id":  # Negative variable reference
                var_name = expr_tree[1]
                return -self.symbol_table.get_variable(name=var_name, containerName=self.current_container)
            
            #############################################################################################################
            elif expr_type == "cte_num":  # Constant number
                return expr_tree[1]
            
            #############################################################################################################
            elif expr_type == "negative_cte_num":  # Negative constant number
                return -expr_tree[1]
            
            #############################################################################################################
            elif expr_type == "term_mult":  # Multiplication
                left = self.evaluate_expression(expr_tree[1])
                right = self.evaluate_expression(expr_tree[2])

                t_left = type(left).__name__
                t_right = type(right).__name__
                result_type = self.semantic_cube.get_type(t_left, t_right, "*")

                if result_type == "int":
                    return int(left * right)
                elif result_type == "float":
                    return float(left * right)
                else:
                    raise UnsupportedOperationError(
                        f"Unsupported operand types for multiplication: {t_left} * {t_right}"
                    )

            #############################################################################################################
            elif expr_type == "term_div":  # Division
                left = self.evaluate_expression(expr_tree[1])
                right = self.evaluate_expression(expr_tree[2])

                t_left = type(left).__name__
                t_right = type(right).__name__
                result_type = self.semantic_cube.get_type(t_left, t_right, "/")

                if result_type is None:
                    raise UnsupportedOperationError(f"Unsupported operand types for division: {t_left} / {t_right}")

                if right == 0:
                    raise DivisionByZeroError("Division by zero is not allowed.")
                
                if result_type == "int":
                    return int(left / right)
                elif result_type == "float":
                    return float(left / right)
                else:
                    raise UnsupportedOperationError(f"Unsupported operand types for division: {t_left} / {t_right}")
                
            #############################################################################################################
            elif expr_type == "exp_plus":  # Addition
                left = self.evaluate_expression(expr_tree[1])
                right = self.evaluate_expression(expr_tree[2])

                t_left = type(left).__name__
                t_right = type(right).__name__
                result_type = self.semantic_cube.get_type(t_left, t_right, "+")

                if (result_type == "int"):
                    return int(left + right)
                elif (result_type == "float"):
                    return float(left + right)
                else:
                    raise UnsupportedOperationError(f"Unsupported operand types for addition: {t_left} + {t_right}")
            
            #############################################################################################################
            elif expr_type == "exp_minus":  # Subtraction
                left = self.evaluate_expression(expr_tree[1])
                right = self.evaluate_expression(expr_tree[2])

                t_left = type(left).__name__
                t_right = type(right).__name__
                result_type = self.semantic_cube.get_type(t_left, t_right, "-")

                if (result_type == "int"):
                    return int(left - right)
                elif (result_type == "float"):
                    return float(left - right)
                else:
                    raise UnsupportedOperationError(f"Unsupported operand types for subtraction: {t_left} - {t_right}")
            
            #############################################################################################################
            elif expr_type == "expresion_comparison_op":  # Comparison
                left = self.evaluate_expression(expr_tree[1])
                op = expr_tree[2]
                right = self.evaluate_expression(expr_tree[3])

                t_left = type(left).__name__
                t_right = type(right).__name__
                result_type = self.semantic_cube.get_type(t_left, t_right, op)

                if (result_type != "int"):
                    raise UnsupportedOperationError(f"Unsupported operand types for comparison: {t_left} {op} {t_right}")

                if op == "==":
                    result = left == right
                elif op == "!=":
                    result = left != right
                elif op == "<":
                    result = left < right
                elif op == "<=":
                    result = left <= right
                elif op == ">":
                    result = left > right
                elif op == ">=":
                    result = left >= right
                else:
                    raise UnsupportedOperationError(f"Unknown comparison operator: {op}")

                return 1 if result else 0
                
            #############################################################################################################
            elif expr_type == "expresion_logic_cond":  # Logical operation
                left = self.evaluate_expression(expr_tree[1])
                op = expr_tree[2]
                right = self.evaluate_expression(expr_tree[3])

                t_left = type(left).__name__
                t_right = type(right).__name__
                result_type = self.semantic_cube.get_type(t_left, t_right, op)

                if (result_type != "int"):
                    raise UnsupportedOperationError(f"Invalid types for logical operation: {t_left} {op} {t_right}")

                if op == "and":
                    result = bool(left) and bool(right)
                elif op == "or":
                    result = bool(left) or bool(right)
                else:
                    raise UnsupportedOperationError(f"Unknown logical operator: {op}")

                return 1 if result else 0
                
        else:
            raise UnsupportedExpressionError(f"Unsupported expression type: {expr_tree}")

    def execute(self, ir):
        if isinstance(ir, tuple):
            ir_type = ir[0]

            #############################################################################################################
            if ir_type == "assign":
                var_name = ir[1]
                value = self.evaluate_expression(ir[2])

                value_type = type(value).__name__
                var_type = self.symbol_table.get_variable_type(name=var_name, containerName=self.current_container)

                if self.semantic_cube.is_decl_valid(var_type, value_type):
                    value = self.semantic_cube.convert_type(var_type, value_type, value)
                else:
                    raise TypeMismatchError(
                        f"Cannot assign type '{value_type}' to variable '{var_name}' of type '{var_type}'"
                    )

                self.symbol_table.update_variable(name=var_name, value=value, containerName=self.current_container)

            #############################################################################################################
            elif ir_type == "var_decl":
                var_type = ir[2]
                initializer = ir[3] if ir[3] else None

                value = self.evaluate_expression(initializer) if initializer else None
                value_type = type(value).__name__ if value is not None else None

                if value is not None:
                    if not self.semantic_cube.is_decl_valid(var_type, value_type):
                        raise TypeMismatchError(
                            f"Cannot assign value of type '{value_type}' to variable of type '{var_type}'"
                        )
                    converted_value = self.semantic_cube.convert_type(var_type, value_type, value)
                else:
                    converted_value = None

                for var in ir[1]:
                    self.symbol_table.add_variable(
                        name=var,
                        value=converted_value,
                        var_type=var_type,
                        containerName=self.current_container,
                        category=ir[4]
                    )
            
            #############################################################################################################
            elif ir_type == "body_statements":
                for statement in ir[1]:
                    self.execute(statement)
            
            #############################################################################################################
            elif ir_type == "empty_body":
                pass
            
            #############################################################################################################
            elif ir_type == "cycle":
                condition = ir[1]
                body = ir[2]
                while self.evaluate_expression(condition):
                    self.execute(body)
           
            #############################################################################################################
            elif ir_type == "print":
                n = 1 if len(ir[1])==1 else len(ir[1])
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
         
            #############################################################################################################
            elif ir_type == "condition_if":
                condition = ir[1]
                body = ir[2]
                if self.evaluate_expression(condition):
                    self.execute(body)
         
            #############################################################################################################
            elif ir_type == "condition_if_else":
                condition = ir[1]
                body_if = ir[2]
                body_else = ir[3]
                if self.evaluate_expression(condition):
                    self.execute(body_if)
                else:
                    self.execute(body_else)
          
            #############################################################################################################
            elif ir_type == "function_decl":
                self.current_container = ir[1]
                func_name = ir[1]
                params_list = []
                if ir[2]:
                    for param in ir[2][1]:
                        param_name = param[0]
                        param_type = param[1]
                        params_list.append((param_name, param_type))
                body = ir[3]
                self.symbol_table.add_function(name=func_name, params=params_list, body=body)
                for var in ir[4]:
                    self.execute(var)
                self.current_container = "global"
            
            #############################################################################################################
            elif ir_type == "func_call":
                self.current_container = ir[1]
                func_name = ir[1]
                params = ir[2]
                values = []
                for param in params:
                    value = self.evaluate_expression(param)
                    values.append(value)
                self.symbol_table.update_params_values(values=values, containerName=func_name)
                func_body = self.symbol_table.get_container(func_name).body
                self.execute(func_body)
                self.symbol_table.clean_params_values(containerName=func_name)
                self.current_container = "global"

            #############################################################################################################
            elif ir_type == "program":
                # ("program", id, decls, funcs, body)
                _, id, decls, funcs, body = ir
                for decl in decls:
                    self.execute(decl)
                for func in funcs:
                    self.execute(func)
                self.execute(body)

            #############################################################################################################
            else:
                raise UnknownIRTypeError(f"Unknown IR type: {ir_type}")
        else:
            raise UnknownIRTypeError(f"Unsupported IR: {ir}")