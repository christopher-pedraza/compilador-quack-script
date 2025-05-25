from dataclasses import dataclass
from typing import Union, List, Optional, Literal


@dataclass
class CteNumNode:
    value: Union[int, float]


@dataclass
class IdNode:
    name: str


@dataclass
class CteStringNode:
    value: str


@dataclass
class UnaryOpNode:
    op: Literal["+", "-"]
    expr: Union[CteNumNode, IdNode]


@dataclass
class ExpMinusNode:
    left: CteNumNode
    right: IdNode


@dataclass
class MultiplicativeOpNode:
    op: Literal["*", "/"]
    left: "ExprNode"
    right: "ExprNode"


@dataclass
class ArithmeticOpNode:
    op: Literal["+", "-"]
    left: "ExprNode"
    right: "ExprNode"


@dataclass
class ComparisonNode:
    op: Literal[">", "<", "==", "!=", ">=", "<="]
    left: "ExprNode"
    right: "ExprNode"


@dataclass
class LogicalAndNode:
    op: Literal["and"]
    left: "ExprNode"
    right: "ExprNode"


@dataclass
class LogicalOrNode:
    op: Literal["or"]
    left: "ExprNode"
    right: "ExprNode"


@dataclass
class AssignNode:
    var_name: str
    expr: "ExprNode"


@dataclass
class BodyNode:
    statements: List["StmtNode"]


@dataclass
class PrintNode:
    values: List[Union["ExprNode", CteStringNode]]


@dataclass
class WhileNode:
    condition: "ExprNode"
    body: BodyNode


@dataclass
class IfNode:
    condition: "ExprNode"
    then_body: BodyNode


@dataclass
class IfElseNode:
    condition: "ExprNode"
    then_body: BodyNode
    else_body: BodyNode


TypeNode = Literal["int", "float"]


@dataclass
class VarDeclNode:
    names: List[str]
    var_type: TypeNode
    init_value: Optional["ExprNode"] = None
    isConstant: bool = False


@dataclass
class ParamNode:
    name: str
    param_type: TypeNode


@dataclass
class ParamsNode:
    params: List[ParamNode]


@dataclass
class FunctionDeclNode:
    name: str
    params: ParamsNode
    body: BodyNode
    var_decls: List[VarDeclNode]


@dataclass
class FuncCallNode:
    name: str
    args: List["ExprNode"]


@dataclass
class ProgramNode:
    name: str
    global_decls: List[VarDeclNode]
    functions: List[FunctionDeclNode]
    main_body: BodyNode


# Para poder referenciar ExprNode y StmtNode antes de que estén completamente definidos

ExprNode = Union[
    CteNumNode,
    IdNode,
    CteStringNode,
    UnaryOpNode,
    MultiplicativeOpNode,
    ArithmeticOpNode,
    ComparisonNode,
    LogicalAndNode,
    LogicalOrNode,
    FuncCallNode,
]

StmtNode = Union[
    AssignNode,
    PrintNode,
    WhileNode,
    IfNode,
    IfElseNode,
    VarDeclNode,
    FunctionDeclNode,
]
