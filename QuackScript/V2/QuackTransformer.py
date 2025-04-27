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
    
    def factor_cte_num(self, cte_num):
        return cte_num
    
    def positive_cte_num(self, plus, cte_num):
        return cte_num

    def negative_cte_num(self, minus, cte_num):
        return -cte_num 
    
    def term_mult(self, factor1, mult, factor2):
        return factor1 * factor2
    
    def term_div(self, factor1, div, factor2):
        return factor1 / factor2

    def exp_plus(self, term1, plus, term2):
        return term1 + term2
    
    def exp_minus(self, term1, minus, term2):
        return term1 - term2