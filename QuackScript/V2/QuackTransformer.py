from lark import Lark, Transformer, v_args

@v_args(inline=True)
class QuackTransformer(Transformer):
    