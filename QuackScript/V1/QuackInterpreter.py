from SemanticCube import SemanticCube

from Exceptions import (
    UnsupportedOperationError,
    DivisionByZeroError,
    UnsupportedExpressionError,
    TypeMismatchError,
    UnknownIRTypeError,
)

from TransformerClasses import (
    IdNode,
    CteNumNode,
    CteStringNode,
    ArithmeticOpNode,
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
    FunctionDeclNode,
    FuncCallNode,
    ProgramNode,
)

from MemoryManager import MemoryAddress


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
        if isinstance(node, MemoryAddress):
            value = node.address
            value_type = node.var_type
        elif isinstance(node, tuple) and node[0] == "id":
            value = node[0]
            value_type = node[1]
        else:
            value = self.evaluate_expression(node)
            value_type = type(value).__name__

        # Second pass: unwrap if result is a quadruple
        if isinstance(value, MemoryAddress):
            value_type = value.var_type
            value = value.address
        elif isinstance(value, tuple) and value[0] == "id":
            value_type = value[2]
            value = value[1]

        return value, value_type

    def evaluate_expression(self, expr_tree):
        if isinstance(expr_tree, IdNode):
            var_name = expr_tree.name
            variable = self.symbol_table.get_variable(name=var_name, containerName=self.current_container)
            value = var_name
            var_type = variable.var_type
            return ("id", value, var_type)

        elif isinstance(expr_tree, CteNumNode):
            var_type = type(expr_tree.value).__name__

            result = self.memory_manager.save_to_first_available(
                value=expr_tree.value,
                var_type=var_type,
                space="constant",
            )

            self.symbol_table.add_constant(address=result.address, value=expr_tree.value, value_type=var_type)

            return result

        elif isinstance(expr_tree, CteStringNode):
            var_type = type(expr_tree.value).__name__
            result = self.memory_manager.save_to_first_available(
                value=expr_tree.value,
                var_type=var_type,
                space="constant",
            )
            self.symbol_table.add_constant(address=result.address, value=expr_tree.value, value_type=var_type)
            return result

            # return expr_tree.value

        elif (
            isinstance(expr_tree, MultiplicativeOpNode)
            or isinstance(expr_tree, ArithmeticOpNode)
            or isinstance(expr_tree, ComparisonNode)
            or isinstance(expr_tree, LogicalAndNode)
            or isinstance(expr_tree, LogicalOrNode)
        ):
            left_value, left_type = self._resolve_operand(expr_tree.left)
            right_value, right_type = self._resolve_operand(expr_tree.right)

            result_type = self.semantic_cube.get_type(left_type, right_type, expr_tree.op)

            if result_type is None:
                raise UnsupportedOperationError(
                    f"Unsupported operation '{expr_tree.op}' for types '{left_type}' and '{right_type}'"
                )

            if expr_tree.op == "/" and right_value == 0:
                raise DivisionByZeroError("Division by zero is not allowed.")

            memory_space = self.memory_manager.save_to_first_available(
                value=(expr_tree.op, expr_tree.left, expr_tree.right),
                var_type=result_type,
                space=self.current_memory_space,
            )
            result = self.quack_quadruple.add_quadruple(
                op=expr_tree.op, arg1=left_value, arg2=right_value, result=memory_space.address
            )
            return result

        ## TODO: PUEDO DEJAR ESTO?? O SI NO HACE MATCH, DEBERIA ARROJAR UN ERROR
        else:
            return expr_tree

    def execute(self, ir):
        if isinstance(ir, AssignNode):
            var_name = ir.var_name
            var_type = self.symbol_table.get_variable_type(name=var_name, containerName=self.current_container)

            value, value_type = self._resolve_operand(ir.expr)

            if self.semantic_cube.is_decl_valid(var_type, value_type):
                self.symbol_table.update_variable(name=var_name, value=value, containerName=self.current_container)
                self.quack_quadruple.add_quadruple("=", value, None, var_name)
            else:
                raise TypeMismatchError(
                    f"Cannot assign type '{value_type}' to variable '{var_name}' of type '{var_type}'"
                )
        ######################################################################################################################
        elif isinstance(ir, VarDeclNode):
            var_type = ir.var_type
            value, value_type = self._resolve_operand(ir.init_value) if ir.init_value else (None, None)

            if ir.init_value and not self.semantic_cube.is_decl_valid(var_type, value_type):
                raise TypeMismatchError(f"Cannot assign value of type '{value_type}' to variable of type '{var_type}'")

            for var_name in ir.names:
                self.symbol_table.add_variable(
                    name=var_name.name,
                    var_type=var_type,
                    value=value,
                    containerName=self.current_container,
                    category=ir.category,
                )
                self.quack_quadruple.add_quadruple("=", value, None, var_name.name)
        ######################################################################################################################
        elif isinstance(ir, BodyNode):
            for statement in ir.statements:
                self.execute(statement)
        ######################################################################################################################
        elif isinstance(ir, WhileNode):
            self.quack_quadruple.add_return()
            condition = self._resolve_operand(ir.condition)

            self.quack_quadruple.push_jump()
            self.quack_quadruple.add_jump(type="gotoF", condition=condition[0])

            self.execute(ir.body)

            self.quack_quadruple.add_jump(type="goto", target=self.quack_quadruple.pop_return())
            self.quack_quadruple.update_jump(
                index=self.quack_quadruple.pop_jump(), target=self.quack_quadruple.get_current_index()
            )
        ######################################################################################################################
        elif isinstance(ir, PrintNode):
            for value in ir.values:
                value, value_type = self._resolve_operand(value)
                self.quack_quadruple.add_quadruple("print", None, None, value)
        ######################################################################################################################
        elif isinstance(ir, IfNode):
            value, value_type = self._resolve_operand(ir.condition)

            self.quack_quadruple.push_jump()
            self.quack_quadruple.add_jump(type="gotoF", condition=value)

            self.execute(ir.then_body)

            self.quack_quadruple.update_jump(
                index=self.quack_quadruple.pop_jump(), target=self.quack_quadruple.get_current_index()
            )
        ######################################################################################################################
        elif isinstance(ir, IfElseNode):
            value, value_type = self._resolve_operand(ir.condition)

            self.quack_quadruple.push_jump()
            self.quack_quadruple.add_jump(type="gotoF", condition=value, target=None)

            self.execute(ir.then_body)

            # Add 1 to the current index to skip the else block
            self.quack_quadruple.update_jump(
                index=self.quack_quadruple.pop_jump(), target=self.quack_quadruple.get_current_index() + 1
            )

            self.quack_quadruple.push_jump()
            self.quack_quadruple.add_jump()

            self.execute(ir.else_body)

            self.quack_quadruple.update_jump(
                index=self.quack_quadruple.pop_jump(), target=self.quack_quadruple.get_current_index()
            )
        ######################################################################################################################
        elif isinstance(ir, FunctionDeclNode):
            self.current_container = ir.name

            params_list = []
            if ir.params:
                for param in ir.params.params:
                    params_list.append((param.name, param.param_type))

            self.symbol_table.add_function(name=ir.name, params=params_list, body=ir.body)

            for var in ir.var_decls:
                # TODO: Checar si esto esta bien o si se tiene que sacar un
                # valor de var
                self.execute(var)

            self.current_container = self.global_container_name
        ######################################################################################################################
        ## TODO: REVISAR LUEGO COMO SE MANEJA LAS LLAMADAS DE FUNCIONES
        elif isinstance(ir, FuncCallNode):
            self.current_container = ir.name

            values = []
            for arg in ir.args:
                value, value_type = self._resolve_operand(arg)
                values.append(value)

            self.symbol_table.update_params_values(values=values, containerName=ir.name)
            func_body = self.symbol_table.get_container(ir.name).body
            self.execute(func_body)
            self.symbol_table.clean_params_values(containerName=ir.name)
            self.current_container = self.global_container_name
        ######################################################################################################################
        elif isinstance(ir, ProgramNode):
            for decl in ir.global_decls:
                self.execute(decl)

            for func in ir.functions:
                self.execute(func)

            self.current_memory_space = "temp"
            self.execute(ir.main_body)
            self.current_memory_space = "global"
        else:
            raise UnknownIRTypeError(f"Unknown IR type: {type(ir)}")
