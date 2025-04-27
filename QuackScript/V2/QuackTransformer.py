from lark import Lark, Transformer, v_args


@v_args(inline=True)
class QuackTransformer(Transformer):
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.current_container = "global"  # Start in the global scope

    def int(self, value):
        return int(value)
    
    def float(self, value):
        return float(value)

    def cte_string(self, value):
        return str(value[1:-1])
    
    def id(self, value):
        return str(value)
    
    def factor_id(self, id):
        return self.symbol_table.get_variable(name=id, containerName=self.current_container)
    
    def positive_factor_id(self, id):
        return self.symbol_table.get_variable(name=id, containerName=self.current_container)