# type: ignore
from .token import Token, TokenType
from .expr import Expr, Stmt

from .errors import ErrorPrinter

class Parser:

    def __init__(self, tokens: list[Token], lines: list[str]) -> None:
        self.tokens: list[Token] = tokens
        self.lines:  list[str] = lines

        self.index:  int = 0

    def error(self, message: str, token: Token) -> None:
        ErrorPrinter(self.lines, message, token).print_error()
        exit(1)

    def expect(self, token_type: TokenType, message: str) -> Token:
        if self.match(token_type):
            return self.previous()
        else:
            self.error(message, self.previous())

    def at_end(self) -> bool:
        return self.peek().token_type == TokenType.EOF
    
    def match(self, *token_types: TokenType) -> bool:
        for token_type in token_types:
            if self.peek().token_type == token_type:
                self.advance()
                return True
        return False
    
    def peek(self) -> Token:
        return self.tokens[self.index]

    def previous(self) -> Token:
        return self.tokens[self.index - 1]

    def advance(self) -> Token:
        if not self.at_end():
            self.index += 1
        return self.previous()

    def parse(self) -> list[Stmt]:
        statements: list[Stmt] = []
        while not self.at_end():
            statements.append(self.variables())
        return statements
    
    def variables(self) -> Stmt:
        if self.match(TokenType.LET) or (self.peek().token_type == TokenType.IDENT and self.tokens[self.index + 1].token_type == TokenType.EQUAL):
            return self.mutable()
        if self.match(TokenType.CONST):
            return self.immutable()
        return self.expression()
    
    def mutable(self) -> Stmt:
        name: Token = self.advance()
        if name.token_type != TokenType.IDENT:
            self.error("Found unexpected token in variable assignment", self.previous())
        types: list[Expr] = []
        value: Expr = None

        stmt: Stmt = None

        if self.match(TokenType.COLON):
            types.append(self.prefix())
            while self.match(TokenType.PIPE):
                types.append(self.prefix())
            self.expect(TokenType.EQUAL, "Expected assignment operator in variable definition")
            if self.peek().token_type == TokenType.SEMICOLON:
                self.error("Expected value in variable definition", self.peek())
            value = self.equality()
            stmt = Stmt.Assign(name, types, value, False, False)

        elif self.match(TokenType.COLON_EQUAL):
            value = self.equality()
            stmt = Stmt.Assign(name, types, value, True, False)
        
        elif self.match(TokenType.EQUAL):
            value = self.equality()
            stmt = Stmt.Reassign(name, value)

        else:
            self.error("Found unexpected token in variable definition", self.peek())

        self.expect(TokenType.SEMICOLON, "Expected semicolon after expression")
        return stmt

    def immutable(self) -> Stmt:
        name: Token = self.advance()
        types: list[Token] = []
        value: Expr = None

        if name.token_type != TokenType.IDENT:
            self.error("Found unexpected token in constant assignment", self.previous())

        stmt: Stmt = None

        if self.match(TokenType.COLON):
            types.append(self.prefix())
            while self.match(TokenType.PIPE):
                types.append(self.prefix())
            self.expect(TokenType.EQUAL, "Expected assignment operator in constant definition")
            if self.peek().token_type == TokenType.SEMICOLON:
                self.error("Expected value in constant definition", self.peek())
            value = self.equality()
            stmt = Stmt.Assign(name, types, value, False, True)

        elif self.match(TokenType.COLON_EQUAL):
            value = self.equality()
            stmt = Stmt.Assign(name, types, value, True, True)
        elif self.match(TokenType.EQUAL):
            self.error("Cannot reassign a constant's value", self.previous())
        else:
            self.error("Found unexpected token in constant definition", self.peek())

        self.expect(TokenType.SEMICOLON, "Expected semicolon after expression")
        return stmt
    
    def expression(self) -> Stmt:
        expr: Expr = self.equality()
        self.expect(TokenType.SEMICOLON, "Expected semicolon after the end of an expression")
        return Stmt.Expression(expr)
    
    def equality(self) -> Expr:
        expr: Expr = self.comparison()

        while self.match(TokenType.TYPE_EQUAL, TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL):
            operator: Token = self.previous()
            right: Expr = self.comparison()
            expr = Expr.Binary(expr, operator, right)
        
        return expr
    
    def comparison(self) -> Expr:
        expr: Expr = self.range()

        while self.match(TokenType.GT, TokenType.GT_EQUAL, TokenType.LT, TokenType.LT_EQUAL):
            operator: Token = self.previous()
            right: Expr = self.range()
            expr = Expr.Binary(expr, operator, right)

        return expr
    
    def range(self) -> Expr:
        expr: Expr = self.term()

        while self.match(TokenType.VARIADIC):
            operator: Token = self.previous()
            right: Expr = self.term()
            expr = Expr.Binary(expr, operator, right)

        return expr
    
    def term(self) -> Expr:
        expr: Expr = self.factor()

        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator: Token = self.previous()
            right: Expr = self.factor()
            expr = Expr.Binary(expr, operator, right)

        return expr
    
    def factor(self) -> Expr:
        expr: Expr = self.exp()

        while self.match(TokenType.MULT, TokenType.DIV):
            operator: Token = self.previous()
            right: Expr = self.exp()
            expr = Expr.Binary(expr, operator, right)

        return expr
    
    def exp(self) -> Expr:
        expr: Expr = self.suffix()

        while self.match(TokenType.MULT_MULT):
            operator: Token = self.previous()
            right: Expr = self.suffix()
            expr = Expr.Binary(expr, operator, right)

        return expr
    
    def suffix(self) -> Expr:
        expr: Expr = self.prefix()
        while self.match(TokenType.PLUS_PLUS, TokenType.MINUS_MINUS, TokenType.QUESTION, TokenType.BANG):
             operator: Token = self.previous()
             return Expr.Suffix(expr, operator)
        return expr
    
    def prefix(self) -> Expr:
        while self.match(TokenType.MINUS, TokenType.AMPERSAND, TokenType.MULT):
            operator: Token = self.previous()
            return Expr.Prefix(self.prefix(), operator)
        return self.literal()
    
    def literal(self) -> Expr:
        if self.match(TokenType.NIL):
            return Expr.Literal(None)
        
        if self.match(TokenType.TRUE):
            return Expr.Literal(True)
        
        if self.match(TokenType.FALSE):
            return Expr.Literal(False)
        
        if self.match(TokenType.NUMBER):
            return Expr.Literal(self.previous().lexeme)
        
        if self.match(TokenType.PIPE):
            expr = Expr.Unwrap(self.prefix())
            self.expect(TokenType.PIPE, "Expected expression to be wrapped in pipes")
            return expr

        if self.match(TokenType.L_PAREN):
            expr: Expr = self.equality()
            self.expect(TokenType.R_PAREN, "Expected closing parenthesis")
            return Expr.Grouping(expr)
        
        if self.match(TokenType.IDENT):
            return Expr.Variable(self.previous())
        
        self.error("Found unexpected token", self.peek())