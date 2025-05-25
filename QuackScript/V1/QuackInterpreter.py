from SemanticCube import SemanticCube

from Exceptions import (
    UnsupportedOperationError,
    DivisionByZeroError,
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

# from MemoryManager import MemoryAddress


class QuackInterpreter:
    def __init__(self, symbol_table, quack_quadruple, memory_manager):
        self.memory_manager = memory_manager
        self.symbol_table = symbol_table
        self.global_container_name = self.symbol_table.global_container_name
        self.current_container = self.global_container_name
        self.semantic_cube = SemanticCube()
        self.quack_quadruple = quack_quadruple
        self.current_memory_space = "global"

    def evaluate_expression(self, expr_tree):
        if isinstance(expr_tree, IdNode):
            var_name = expr_tree.name
            variable = self.symbol_table.get_variable(name=var_name, containerName=self.current_container)
            value = variable.address
            var_type = variable.var_type
            return value, var_type

        elif isinstance(expr_tree, CteNumNode) or isinstance(expr_tree, CteStringNode):
            var_type = type(expr_tree.value).__name__
            value = expr_tree.value

            constant_address = self.symbol_table.constants_table.check_and_get_address(value)

            if constant_address is not None:
                result = constant_address
            else:
                result = self.memory_manager.get_first_available_address(
                    var_type=var_type,
                    space="constant",
                )
                self.symbol_table.add_constant(address=result, value=value, value_type=var_type)

            return result, var_type

        elif (
            isinstance(expr_tree, MultiplicativeOpNode)
            or isinstance(expr_tree, ArithmeticOpNode)
            or isinstance(expr_tree, ComparisonNode)
            or isinstance(expr_tree, LogicalAndNode)
            or isinstance(expr_tree, LogicalOrNode)
        ):
            left_value, left_type = self.evaluate_expression(expr_tree.left)
            right_value, right_type = self.evaluate_expression(expr_tree.right)

            result_type = self.semantic_cube.get_type(left_type, right_type, expr_tree.op)

            if result_type is None:
                raise UnsupportedOperationError(
                    f"Unsupported operation '{expr_tree.op}' for types '{left_type}' and '{right_type}'"
                )

            if expr_tree.op == "/" and right_value == 0:
                raise DivisionByZeroError("Division by zero is not allowed.")

            address = self.memory_manager.get_first_available_address(
                var_type=f"t{result_type}",
                space=self.current_memory_space,
            )

            result = self.quack_quadruple.add_quadruple(
                op=expr_tree.op, arg1=left_value, arg2=right_value, result=address
            )
            return result, result_type

        else:
            print("Oye, llegué aquí, qué procede?")
            return expr_tree

    def execute(self, ir):
        if isinstance(ir, AssignNode):
            var_name = ir.var_name
            variable = self.symbol_table.get_variable(name=var_name, containerName=self.current_container)

            value, value_type = self.evaluate_expression(ir.expr)

            if self.semantic_cube.is_decl_valid(variable.var_type, value_type):
                self.quack_quadruple.add_quadruple("=", value, None, variable.address)
            else:
                raise TypeMismatchError(
                    f"Cannot assign type '{value_type}' to variable '{var_name}' of type '{variable.var_type}'"
                )
        ###################################################################################
        elif isinstance(ir, VarDeclNode):
            var_type = ir.var_type

            #########Esto se puede mejorar######
            value, value_type = (None, None)
            if ir.init_value:
                value, value_type = self.evaluate_expression(ir.init_value)
                if not self.semantic_cube.is_decl_valid(var_type, value_type):
                    raise TypeMismatchError(
                        f"Cannot assign value of type '{value_type}' to variable of type '{var_type}'"
                    )
            ####################################

            for var_name in ir.names:
                address = self.memory_manager.get_first_available_address(
                    var_type=var_type,
                    space=self.current_memory_space,
                )
                self.symbol_table.add_variable(
                    name=var_name.name,
                    var_type=var_type,
                    containerName=self.current_container,
                    isConstant=ir.isConstant,
                    address=address,
                )
                self.quack_quadruple.add_quadruple("=", value, None, address)
        ###################################################################################
        elif isinstance(ir, BodyNode):
            for statement in ir.statements:
                self.execute(statement)
        ###################################################################################
        elif isinstance(ir, WhileNode):
            self.quack_quadruple.add_return()
            condition = self.evaluate_expression(ir.condition)

            self.quack_quadruple.push_jump()
            self.quack_quadruple.add_jump(type="gotoF", condition=condition[0])

            self.execute(ir.body)

            self.quack_quadruple.add_jump(type="goto", target=self.quack_quadruple.pop_return())
            self.quack_quadruple.update_jump(
                index=self.quack_quadruple.pop_jump(), target=self.quack_quadruple.get_current_index()
            )
        ###################################################################################
        elif isinstance(ir, PrintNode):
            for value in ir.values:
                value, value_type = self.evaluate_expression(value)
                self.quack_quadruple.add_quadruple("print", None, None, value)
        ###################################################################################
        elif isinstance(ir, IfNode):
            value, value_type = self.evaluate_expression(ir.condition)

            self.quack_quadruple.push_jump()
            self.quack_quadruple.add_jump(type="gotoF", condition=value)

            self.execute(ir.then_body)

            self.quack_quadruple.update_jump(
                index=self.quack_quadruple.pop_jump(), target=self.quack_quadruple.get_current_index()
            )
        ###################################################################################
        elif isinstance(ir, IfElseNode):
            value, value_type = self.evaluate_expression(ir.condition)

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
        ###################################################################################
        elif isinstance(ir, FunctionDeclNode):
            pass
        elif isinstance(ir, FuncCallNode):
            pass

        ###################################################################################
        elif isinstance(ir, ProgramNode):
            for decl in ir.global_decls:
                self.execute(decl)

            for func in ir.functions:
                self.execute(func)

            self.execute(ir.main_body)
        else:
            raise UnknownIRTypeError(f"Unknown IR type: {type(ir)}")
