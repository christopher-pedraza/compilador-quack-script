from Exceptions import (
    TypeMismatchError,
    UnknownIRTypeError,
    UnsupportedOperationError,
)
from MemoryManager import Memory
from SemanticCube import SemanticCube
from TransformerClasses import (
    ArithmeticOpNode,
    AssignNode,
    BodyNode,
    ComparisonNode,
    CteNumNode,
    CteStringNode,
    FuncCallNode,
    FunctionDeclNode,
    IdNode,
    IfElseNode,
    IfNode,
    LogicalAndNode,
    LogicalOrNode,
    MultiplicativeOpNode,
    ParamNode,
    PrintNode,
    ProgramNode,
    ReturnNode,
    VarDeclNode,
    WhileNode,
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

    def __process_func_call(self, func_call):
        func_name = func_call.name.name
        func_args = func_call.args

        old_memory = self.memory_manager.replace_memory_space(
            "local",
            Memory(
                mapping={
                    "int": ((5000, 5999), 0),
                    "float": ((6000, 6999), 0),
                    "t_int": ((7000, 7999), 0),
                    "t_float": ((8000, 8999), 0),
                }
            ),
        )

        self.quack_quadruple.add_quadruple("era", None, None, func_name)

        param_signature = self.symbol_table.get_function(func_name).get_param_signature()

        if len(param_signature) != len(func_args):
            raise TypeMismatchError(
                f"Function '{func_name}' expects {len(param_signature)} arguments, but got {len(func_args)}"
            )

        for i, arg in enumerate(func_args):
            arg_value, arg_type = self.__evaluate_expression(arg)

            if not self.semantic_cube.is_decl_valid(param_signature[i], arg_type):
                raise TypeMismatchError(
                    f"Argument {i + 1} of function '{func_name}' expects type '{param_signature[i]}', but got '{arg_type}'"
                )

            address_in_function = self.memory_manager.get_first_available_address(
                var_type=arg_type,
                space="local",
            )

            self.quack_quadruple.add_quadruple("param", arg_value, None, address_in_function)

        self.quack_quadruple.add_quadruple("gosub", None, None, func_name)

        return_type = self.symbol_table.get_return_type(func_name)

        self.memory_manager.replace_memory_space("local", old_memory)

        return return_type

    def __evaluate_expression(self, expr_tree):
        if isinstance(expr_tree, IdNode):
            var_name = expr_tree.name
            variable = self.symbol_table.get_variable(name=var_name, containerName=self.current_container)
            value = variable.address
            var_type = variable.var_type
            return value, var_type

        if isinstance(expr_tree, FuncCallNode):
            func_name = expr_tree.name.name
            return_type = self.__process_func_call(expr_tree)

            if return_type != "void":
                if self.symbol_table.get_function(self.global_container_name).is_symbol_declared(name=func_name):
                    func_address = self.symbol_table.get_variable(
                        name=func_name, containerName=self.global_container_name
                    ).address
                else:
                    func_address = self.memory_manager.get_first_available_address(
                        var_type=return_type,
                        space="global",
                    )
                    self.symbol_table.add_variable(
                        name=func_name,
                        var_type=return_type,
                        containerName=self.global_container_name,
                        address=func_address,
                    )
                temp_address = self.memory_manager.get_first_available_address(
                    var_type=f"t_{return_type}",
                    space=self.current_memory_space,
                )
                self.symbol_table.add_temp(
                    var_type=f"t_{return_type}",
                    containerName=self.current_container,
                )
                self.quack_quadruple.add_quadruple("=", func_address, None, temp_address)
                self.symbol_table.get_function(func_name).return_address = func_address

                return temp_address, return_type
            else:
                raise TypeMismatchError(
                    f"Function '{func_name}' does not return a value, cannot be used in an expression."
                )

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
            left_value, left_type = self.__evaluate_expression(expr_tree.left)
            right_value, right_type = self.__evaluate_expression(expr_tree.right)

            result_type = self.semantic_cube.get_type(left_type, right_type, expr_tree.op)

            if result_type is None:
                raise UnsupportedOperationError(
                    f"Unsupported operation '{expr_tree.op}' for types '{left_type}' and '{right_type}'"
                )

            func_address = self.memory_manager.get_first_available_address(
                var_type=f"t_{result_type}",
                space=self.current_memory_space,
            )
            self.symbol_table.add_temp(
                var_type=f"t_{result_type}",
                containerName=self.current_container,
            )

            result = self.quack_quadruple.add_quadruple(
                op=expr_tree.op, arg1=left_value, arg2=right_value, result=func_address
            )
            return result, result_type

        else:
            raise UnsupportedOperationError(f"Unsupported expression type: {type(expr_tree)}")
            # return expr_tree

    def execute(self, ir):
        if isinstance(ir, AssignNode):
            var_name = ir.var_name
            variable = self.symbol_table.get_variable(name=var_name, containerName=self.current_container)

            if variable.isConstant:
                raise TypeMismatchError(f"Cannot reassign constant variable '{var_name}'")

            value, value_type = self.__evaluate_expression(ir.expr)

            if self.semantic_cube.is_decl_valid(variable.var_type, value_type):
                self.quack_quadruple.add_quadruple("=", value, None, variable.address)
            else:
                raise TypeMismatchError(
                    f"Cannot assign type '{value_type}' to variable '{var_name}' of type '{variable.var_type}'"
                )

        ###################################################################################
        elif isinstance(ir, VarDeclNode):
            var_type = ir.var_type

            value, value_type = (None, None)
            if ir.init_value:
                value, value_type = self.__evaluate_expression(ir.init_value)
                if not self.semantic_cube.is_decl_valid(var_type, value_type):
                    raise TypeMismatchError(
                        f"Cannot assign value of type '{value_type}' to variable of type '{var_type}'"
                    )

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
            condition = self.__evaluate_expression(ir.condition)

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
                value, value_type = self.__evaluate_expression(value)
                self.quack_quadruple.add_quadruple("print", None, None, value)

        ###################################################################################
        elif isinstance(ir, IfNode):
            value, value_type = self.__evaluate_expression(ir.condition)

            self.quack_quadruple.push_jump()
            self.quack_quadruple.add_jump(type="gotoF", condition=value)

            self.execute(ir.then_body)

            self.quack_quadruple.update_jump(
                index=self.quack_quadruple.pop_jump(), target=self.quack_quadruple.get_current_index()
            )

        ###################################################################################
        elif isinstance(ir, IfElseNode):
            value, value_type = self.__evaluate_expression(ir.condition)

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
            func_name = ir.name.name
            func_return_type = ir.return_type
            func_params = ir.params.params
            func_body = ir.body
            func_var_decls = ir.var_decls

            self.current_container = func_name
            self.current_memory_space = "local"

            old_memory = self.memory_manager.replace_memory_space(
                "local",
                Memory(
                    mapping={
                        "int": ((5000, 5999), 0),
                        "float": ((6000, 6999), 0),
                        "t_int": ((7000, 7999), 0),
                        "t_float": ((8000, 8999), 0),
                    }
                ),
            )

            self.symbol_table.add_function(name=func_name, return_type=func_return_type)

            starting_index = self.quack_quadruple.get_current_index()
            self.symbol_table.get_function(func_name).initial_position = starting_index

            for param in func_params:
                self.execute(param)

            for var_decl in func_var_decls:
                self.execute(var_decl)

            self.execute(func_body)

            final_index = self.quack_quadruple.get_current_index()
            self.symbol_table.get_function(func_name).final_position = final_index - 1

            self.quack_quadruple.add_quadruple("endFunc", None, None, func_name)

            self.current_container = self.global_container_name
            self.current_memory_space = "global"
            self.symbol_table.get_function(func_name).clear()

            self.memory_manager.replace_memory_space("local", old_memory)

        ###################################################################################
        elif isinstance(ir, ParamNode):
            param_name = ir.name.name
            param_type = ir.param_type

            address = self.memory_manager.get_first_available_address(
                var_type=param_type,
                space=self.current_memory_space,
            )
            self.symbol_table.add_parameter(
                name=param_name,
                var_type=param_type,
                containerName=self.current_container,
                address=address,
            )

        ###################################################################################
        elif isinstance(ir, FuncCallNode):
            self.__process_func_call(ir)

        ###################################################################################
        elif isinstance(ir, ReturnNode):
            return_value = self.__evaluate_expression(ir.expresion)
            self.quack_quadruple.add_quadruple("return", self.current_container, None, return_value[0])

        ###################################################################################
        elif isinstance(ir, ProgramNode):
            for decl in ir.global_decls:
                self.execute(decl)

            self.quack_quadruple.push_jump()
            self.quack_quadruple.add_jump(type="goto")

            for func in ir.functions:
                self.execute(func)

            self.quack_quadruple.update_jump(
                index=self.quack_quadruple.pop_jump(), target=self.quack_quadruple.get_current_index()
            )

            self.execute(ir.main_body)

            self.quack_quadruple.add_quadruple("end", None, None, None)

            self.symbol_table.get_function(self.global_container_name).clear()
        else:
            raise UnknownIRTypeError(f"Unknown IR type: {type(ir)}")
