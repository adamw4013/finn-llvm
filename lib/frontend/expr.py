# type: ignore
# we type ignore this file because the python type checking is really bad
from .token import Token, TokenType

from llvmlite import ir


class Expr:
    
    def codegen(self, builder: ir.IRBuilder) -> None:...
    def pprint(self, indent: int = 0) -> None:...
    

    class Binary:

        def __init__(self, left, operator: Token, right) -> None: 
            self.left = left
            self.operator: Token = operator
            self.right = right

        def pprint(self, indent: int = 0) -> None:
            print(f"{' ' * indent}Expr.Binary(")
            self.left.pprint(indent + 4)
            self.operator.pprint(indent + 4)
            self.right.pprint(indent + 4)
            print(f"{' ' * indent})")


    class Prefix:

        def __init__(self, right, operator: Token) -> None:
            self.right = right
            self.operator: Token = operator

        def pprint(self, indent: int = 0) -> None:
            print(f"{' ' * indent}Expr.Prefix(")
            self.right.pprint(indent + 4)
            self.operator.pprint(indent + 4)
            print(f"{' ' * indent})")


    class Suffix:

        def __init__(self, left, operator: Token) -> None:
            self.left = left
            self.operator: Token = operator

        def pprint(self, indent: int = 0) -> None:
            print(f"{' ' * indent}Expr.Suffix(")
            self.left.pprint(indent + 4)
            self.operator.pprint(indent + 4)
            print(f"{' ' * indent})")


    class Literal:

        def __init__(self, value: int | float | bool) -> None:
            self.value: int | float | bool = value

        def pprint(self, indent: int = 0) -> None:
            print(f"{' ' * indent}Expr.Literal({self.value})")

    
    class Grouping:

        def __init__(self, expression) -> None:
            self.expression = expression

        def pprint(self, indent: int = 0) -> None:
            print(f"{' ' * indent}Expr.Grouping(")
            self.expression.pprint(indent + 4)
            print(f"{' ' * indent})")


    class Variable:

        def __init__(self, name: Token) -> None:
            self.name: Token = name

        def pprint(self, indent: int = 0) -> None:
            print(f"{' ' * indent}Expr.Variable({self.name.lexeme})")

    
    class Unwrap:

        def __init__(self, name: Token) -> None:
            self.name: Token = name

        def pprint(self, indent: int = 0) -> None:
            print(f"{' ' * indent}Expr.Unwrap(")
            self.name.pprint(indent + 4)
            print(f"{' ' * indent})")


class Stmt:

    class Expression:

        def __init__(self, expression: Expr) -> None:
            self.expression = expression

        def pprint(self, indent: int = 0) -> None:
            print(f"{' ' * indent}Stmt.Expression(")
            self.expression.pprint(indent + 4)
            print(f"{' ' * indent})")

    class If:

        def __init__(self, conditional: Expr, then_branch, else_branch) -> None:
            self.conditional = conditional
            self.then_branch = then_branch
            self.else_branch = else_branch

        def pprint(self, indent: int = 0) -> None:
            print(f"{' ' * indent}Stmt.If(")
            self.conditional.pprint(indent + 4)
            self.then_branch.pprint(indent + 4)
            self.else_branch.pprint(indent + 4)
            print(f"{' ' * indent})")

    
    class Assign:

        def __init__(self, name: Token, types: list[Token], value: Expr, infer: bool = False, const: bool = False) -> None:
            self.name = name
            self.types = types
            self.value = value
            self.infer = infer
            self.const = const

        def pprint(self, indent: int = 0):
            print(f"{' ' * indent}Stmt.Assign(")
            print(f"{' ' * (indent + 4)}Expr.Variable({self.name.lexeme})")
            for _type in self.types:
                _type.pprint(indent + 4)
            self.value.pprint(indent + 4)
            print(f"{' ' * indent})")

    class Reassign:

        def __init__(self, name: Token, value: Expr) -> None:
            self.name = name
            self.value = value

        def pprint(self, indent: int = 0) -> None:
            print(f"{' ' * indent}Stmt.Reassign(")
            print(f"{' ' * (indent + 4)}Expr.Variable({self.name.lexeme})")
            self.value.pprint(indent + 4)
            print(f"{' ' * indent})")