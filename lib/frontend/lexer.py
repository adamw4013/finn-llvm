from .token import TokenType, Token
from .errors import ErrorPrinter

class Lexer:

    def __init__(self, source: str, filename: str, lines: list[str]) -> None:
        self.source:   str = source
        self.filename: str = filename
        self.lines: list[str] = lines

        self.index:    int = 0
        self.start:    int = 0

        self.line:     int = 1
        self.start_cursor: int = 1
        self.end_cursor: int = 1
        self.cursor:   int = 1

        self.keywords: dict[str, TokenType] = {
            "import"    : TokenType.IMPORT,
            "return"    : TokenType.RETURN,

            "func"      : TokenType.FUNC,
            "struct"    : TokenType.STRUCT,
            "enum"      : TokenType.ENUM,
            "class"     : TokenType.CLASS,
            "interface" : TokenType.INTERFACE,

            "type"      : TokenType.TYPE,
            
            "where"     : TokenType.WHERE,

            "let"       : TokenType.LET,
            "const"     : TokenType.CONST,

            "while"     : TokenType.WHILE,
            "for"       : TokenType.FOR,

            "if"        : TokenType.IF,
            "else"      : TokenType.ELSE,

            "public"    : TokenType.PUBLIC,
            "private"   : TokenType.PRIVATE,

            "self"      : TokenType.SELF,
            "new"       : TokenType.NEW,

            "true"      : TokenType.TRUE,
            "false"     : TokenType.FALSE,
            "nil"       : TokenType.NIL
        }

        self.output:   list[Token] = []

    # region "Helper Functions"
    def at_end(self) -> bool:
        return self.index >= len(self.source)
    
    def match(self, target: str) -> bool:
        if self.at_end() or target != self.peek():
            return False
        else:
            self.advance()
            return True
    
    def advance(self) -> str:
        character: str = self.source[self.index]
        self.index += 1
        self.end_cursor += 1
        return character
    
    def peek(self) -> str:
        if self.at_end():
            return self.source[self.index - 1]
        return self.source[self.index]
    
    def peek_next(self) -> str:
        if self.index + 1 >= len(self.source):
            return self.peek()
        return self.source[self.index + 1]
    
    def create_token(self, token_type: TokenType, lexeme: str, token_kind: TokenType) -> None:
        self.output.append(Token(token_type, lexeme, token_kind, (self.line, (self.start_cursor, self.end_cursor)), self.filename))

    def isalpha(self, character: str) -> bool:
        return (character >= "a" and character <= "z") or (character >= "A" and character <= "Z") or character == "_"
    
    def isdigit(self, character: str) -> bool:
        try:
            int(character)
            return True
        except:
            return False
    
    def isalnum(self, character: str) -> bool:
        return self.isdigit(character) or self.isalpha(character)
    # endregion

    # region "Main Functions"
    def handle_multiline_comment(self) -> None:
        is_looping: bool = True
        while not self.at_end() and is_looping:

            match self.peek(): 

                case "*":
                    self.advance()
                    if self.peek() == "/":
                        is_looping = False
                        self.advance()

                case "\n":
                    self.line += 1
                    self.cursor = 1
                    self.advance()

                case _:
                    self.advance()

    def number(self) -> None:
        while not self.at_end() and self.isdigit(self.peek()):
            self.advance()

        is_float: bool = False

        if self.peek() == ".":
            is_float = True
            while not self.at_end() or self.isdigit(self.peek()):
                self.advance()

        if is_float:
            self.create_token(TokenType.NUMBER, self.source[self.start:self.index], TokenType.FLOAT)
        else:
            self.create_token(TokenType.NUMBER, self.source[self.start:self.index], TokenType.INT)

    def identifier(self) -> None:
        while not self.at_end() and self.isalnum(self.peek()):
            self.advance()
        
        identifier: str = self.source[self.start:self.index]

        if identifier not in self.keywords.keys():
            self.create_token(TokenType.IDENT, identifier, TokenType.INTRINSIC)
        else:
            self.create_token(self.keywords[identifier], identifier, TokenType.INTRINSIC)

    def lex_token(self) -> None:
        character: str = self.advance()

        match character:

            case "(":
                self.create_token(TokenType.L_PAREN, "(", TokenType.OPERATOR)

            case ")":
                self.create_token(TokenType.R_PAREN, ")", TokenType.OPERATOR)

            case "[":
                self.create_token(TokenType.L_SQUARE, "[", TokenType.OPERATOR)

            case "]":
                self.create_token(TokenType.R_SQUARE, "]", TokenType.OPERATOR)

            case "{":
                self.create_token(TokenType.L_BRACE, "(", TokenType.OPERATOR)

            case "}":
                self.create_token(TokenType.R_BRACE, "}", TokenType.OPERATOR)

            case ".":
                if self.match("."):
                    self.create_token(TokenType.VARIADIC, "..", TokenType.OPERATOR)
                else:
                    self.create_token(TokenType.DOT, ".", TokenType.OPERATOR)

            case "&":
                self.create_token(TokenType.AMPERSAND, "&", TokenType.OPERATOR)

            case ",":
                self.create_token(TokenType.COMMA, ",", TokenType.OPERATOR)

            case "|":
                self.create_token(TokenType.PIPE, "|", TokenType.OPERATOR)

            case "+":
                if self.match("+"):
                    self.create_token(TokenType.PLUS_PLUS, "++", TokenType.OPERATOR)
                elif self.match("="):
                    self.create_token(TokenType.PLUS_EQUAL, "+=", TokenType.OPERATOR)
                else:
                    self.create_token(TokenType.PLUS, "+", TokenType.OPERATOR)

            case "-":
                if self.match("-"):
                    self.create_token(TokenType.MINUS_MINUS, "--", TokenType.OPERATOR)
                elif self.match("="):
                    self.create_token(TokenType.MINUS_EQUAL, "-=", TokenType.OPERATOR)
                else:
                    self.create_token(TokenType.MINUS, "-", TokenType.OPERATOR)

            case "*":
                if self.match("*"):
                    self.create_token(TokenType.MULT_MULT, "**", TokenType.OPERATOR)
                elif self.match("="):
                    self.create_token(TokenType.MULT_EQUAL, "*=", TokenType.OPERATOR)
                else:
                    self.create_token(TokenType.MULT, "*", TokenType.OPERATOR)

            case "/":
                if self.match("/"):
                    while not self.at_end() and self.peek() != "\n":
                        self.advance()
                    self.line += 1
                    self.end_cursor = 1
                elif self.match("*"):
                    self.handle_multiline_comment()
                elif self.match("="):
                    self.create_token(TokenType.DIV_EQUAL, "/=", TokenType.OPERATOR)
                else:
                    self.create_token(TokenType.DIV, "/", TokenType.OPERATOR)

            case "<":
                if self.match("<"):
                    self.create_token(TokenType.SHL, "<<", TokenType.OPERATOR)
                elif self.match("="):
                    if self.match(">"):
                        self.create_token(TokenType.TYPE_EQUAL, "<=>", TokenType.OPERATOR)
                    else:
                        self.create_token(TokenType.LT_EQUAL, "<=", TokenType.OPERATOR)
                else:
                    self.create_token(TokenType.LT, "<", TokenType.OPERATOR)

            case ">":
                if self.match(">"):
                    self.create_token(TokenType.SHR, ">>", TokenType.OPERATOR)
                elif self.match("="):
                    self.create_token(TokenType.GT_EQUAL, ">=", TokenType.OPERATOR)
                else:
                    self.create_token(TokenType.GT, ">", TokenType.OPERATOR)

            case "!":
                if self.match("="):
                    self.create_token(TokenType.NOT_EQUAL, "!=", TokenType.OPERATOR)
                else:
                    self.create_token(TokenType.BANG, "!", TokenType.OPERATOR)

            case "=":
                if self.match("="):
                    self.create_token(TokenType.EQUAL_EQUAL, "==", TokenType.OPERATOR)
                elif self.match(">"):
                    self.create_token(TokenType.FAT_ARROW, "=>", TokenType.OPERATOR)
                else:
                    self.create_token(TokenType.EQUAL, "=", TokenType.OPERATOR)

            case "?":
                self.create_token(TokenType.QUESTION, "?", TokenType.OPERATOR)

            case ":":
                if self.match(":"):
                    self.create_token(TokenType.SCOPE, "::", TokenType.OPERATOR)
                elif self.match("="):
                    self.create_token(TokenType.COLON_EQUAL, ":=", TokenType.OPERATOR)
                else:
                    self.create_token(TokenType.COLON, ":", TokenType.OPERATOR)

            case ";":
                self.create_token(TokenType.SEMICOLON, ";", TokenType.OPERATOR)

            case "\r" | "\t" | " ":
                ...

            case "\n":
                self.line += 1
                self.end_cursor = 1

            case _:
                if self.isdigit(character):
                    self.number()
                if self.isalpha(character):
                    self.identifier()
                if not (self.isalpha(character) or self.isdigit(character)):
                    ErrorPrinter(self.lines, "Found unknown character", Token(TokenType.NIL, "", TokenType.NIL, (self.line, (self.start_cursor, self.end_cursor)), self.filename)).print_error()
                    exit(1)

    def lex(self) -> list[Token]:
        while not self.at_end():
            self.start = self.index
            self.start_cursor = self.end_cursor
            self.lex_token()
        self.create_token(TokenType.EOF, "", TokenType.INTRINSIC)
        return self.output
    # endregion