from SemanticCube import SemanticCube

from Exceptions import (
    UnsupportedOperationError,
    DivisionByZeroError,
    UnsupportedExpressionError,
    TypeMismatchError,
    UnknownIRTypeError
)

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

class QuackInterpreter:
    def __init__(self, symbol_table, quack_quadruple, memory_manager):
        self.memory_manager = memory_manager
        self.symbol_table = symbol_table
        self.global_container_name = self.symbol_table.global_container_name
        self.current_container = self.global_container_name
        self.semantic_cube = SemanticCube()
        self.quack_quadruple = quack_quadruple
        self.current_memory_space = "global"

    def _resolve_operand(self, node):
        if isinstance(node, tuple) and node[0] == "quadruple":
            value = node[1]
            value_type = node[2]
        else:
            value = self.evaluate_expression(node)
            value_type = type(value).__name__

        # Second pass: unwrap if result is a quadruple
        if isinstance(value, tuple) and value[0] == "quadruple":
            value_type = value[2]
            value = value[1]
        elif isinstance(value, tuple) and value[0] == "id":
            value_type = value[3]
            value = value[1]

        return value, value_type

    def evaluate_expression(self, expr_tree):
        if isinstance(expr_tree, IdNode):
            var_name = expr_tree.name
            var_type = self.symbol_table.get_variable_type(name=var_name, containerName=self.current_container)
            value = self.symbol_table.get_variable_value(name=var_name, containerName=self.current_container)
            return value, var_type

    def execute(self, ir):
        if isinstance(ir, tuple):
            ir_type = ir[0]

            #############################################################################################################
            if ir_type == "assign":
                if self.current_container != self.global_container_name:
                    self.current_memory_space = "temp"

                var_name = ir[1]

                resolved_expression = self._resolve_operand(ir[2])
                value = resolved_expression[0]
                value_type = resolved_expression[1]

                var_type = self.symbol_table.get_variable_type(name=var_name, containerName=self.current_container)

                if self.semantic_cube.is_decl_valid(var_type, value_type):
                    value = self.semantic_cube.convert_type(var_type, value_type, value)
                else:
                    raise TypeMismatchError(
                        f"Cannot assign type '{value_type}' to variable '{var_name}' of type '{var_type}'"
                    )
                
                self.quack_quadruple.add_quadruple("=", value, None, var_name)

                self.symbol_table.update_variable(name=var_name, value=value, containerName=self.current_container)

                self.current_memory_space = "global"

            #############################################################################################################
            elif ir_type == "var_decl":
                var_type = ir[2]
                initializer = ir[3] if ir[3] else None

                resolved_operand = self._resolve_operand(initializer) if initializer else None
                value, value_type = resolved_operand if resolved_operand else (None, None)

                if value is not None:
                    if not self.semantic_cube.is_decl_valid(var_type, value_type):
                        raise TypeMismatchError(
                            f"Cannot assign value of type '{value_type}' to variable of type '{var_type}'"
                        )

                for var in ir[1]:
                    self.quack_quadruple.add_quadruple("=", value, None, var)

                    self.symbol_table.add_variable(
                        name=var,
                        value=value,
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
                self.quack_quadruple.add_return()
                condition = self._resolve_operand(ir[1])
            
                self.quack_quadruple.push_jump()
                self.quack_quadruple.add_jump(type="False", condition=condition[0], target=None)
                
                body = ir[2]
                self.execute(body)
                
                self.quack_quadruple.add_jump(target=self.quack_quadruple.pop_return())
                self.quack_quadruple.update_jump(index=self.quack_quadruple.pop_jump(), target=self.quack_quadruple.get_current_index())
           
            #############################################################################################################
            elif ir_type == "print":
                print_statement = None
                self.current_memory_space = "temp"

                if isinstance(ir[1], tuple) and ir[1][0] == "quadruple":
                    print_statement = ir[1][1]
                else:
                    print_statement = ir[1]

                n = 1 if len(print_statement)==1 else len(print_statement)
                for i in range(n):
                    item = print_statement[i]
                    if isinstance(item, tuple) and item[0] == "id":
                        var_name = item[1]
                        value = var_name
                    elif isinstance(item, tuple) and item[0] == "cte_string":
                        value = item[1]
                    else:
                        value = self._resolve_operand(item)[0]
                        
                    self.quack_quadruple.add_quadruple("print", None, None, value)

                    self.current_memory_space = "global"
         
            #############################################################################################################
            elif ir_type == "condition_if":
                condition = self._resolve_operand(ir[1])

                self.quack_quadruple.push_jump()
                self.quack_quadruple.add_jump(type="False", condition=condition[0], target=None)

                body = ir[2]
                self.execute(body)

                self.quack_quadruple.update_jump(index=self.quack_quadruple.pop_jump(), target=self.quack_quadruple.get_current_index())
         
            #############################################################################################################
            elif ir_type == "condition_if_else":
                condition = self._resolve_operand(ir[1])

                self.quack_quadruple.push_jump()
                self.quack_quadruple.add_jump(type="False", condition=condition[0], target=None)

                body_if = ir[2]
                self.execute(body_if)

                # Add 1 to the current index to skip the else block
                self.quack_quadruple.update_jump(index=self.quack_quadruple.pop_jump(), target=self.quack_quadruple.get_current_index()+1)

                self.quack_quadruple.push_jump()
                self.quack_quadruple.add_jump()

                body_else = ir[3]
                self.execute(body_else)

                self.quack_quadruple.update_jump(index=self.quack_quadruple.pop_jump(), target=self.quack_quadruple.get_current_index())
                    
          
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
                self.current_container = self.global_container_name
            
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
                self.current_container = self.global_container_name

            #############################################################################################################
            elif ir_type == "program":
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