from enum import Enum, auto

class TokenType(Enum):
    STRING = auto()

    NUMBER = auto()

    FLOAT = auto()
    F32 = auto()
    F64 = auto()
    F128 = auto()

    UFLOAT = auto()
    UF32 = auto()
    UF64 = auto()
    UF128 = auto()

    INT = auto()
    I8 = auto()
    I16 = auto()
    I32 = auto()
    I64 = auto()
    I128 = auto()

    BOOL = auto() # i1
    TRUE = auto()
    FALSE = auto()

    UINT = auto()
    U8 = auto()
    U16 = auto()
    U32 = auto()
    U64 = auto()
    U128 = auto()

    PLUS = auto()
    PLUS_PLUS = auto()
    PLUS_EQUAL = auto()

    MINUS = auto()
    MINUS_MINUS = auto()
    MINUS_EQUAL = auto()

    DIV = auto()
    DIV_EQUAL = auto()

    MULT = auto()
    MULT_MULT = auto()
    MULT_EQUAL = auto()

    EQUAL = auto()
    EQUAL_EQUAL = auto()
    NOT_EQUAL = auto()
    TYPE_EQUAL = auto()
    COLON_EQUAL = auto()

    PIPE = auto()
    COMMA = auto()
    COLON = auto()
    SCOPE = auto()
    SEMICOLON = auto()

    LET = auto()
    CONST = auto()

    LT = auto()
    LT_EQUAL = auto()
    SHL = auto()

    GT = auto()
    GT_EQUAL = auto()
    FAT_ARROW = auto()
    SHR = auto()

    VARIADIC = auto()
    DOT = auto()
    AMPERSAND = auto()

    BANG = auto()
    QUESTION = auto()

    L_PAREN = auto()
    R_PAREN = auto()

    L_BRACE = auto()
    R_BRACE = auto()

    L_SQUARE = auto()
    R_SQUARE = auto()

    FOR = auto()
    WHILE = auto()
    IF = auto()
    ELSE = auto()

    IMPORT = auto()
    RETURN = auto()

    TYPE = auto()

    FUNC = auto()
    CLASS = auto()
    ENUM = auto()
    STRUCT = auto()
    INTERFACE = auto()

    NIL = auto()
    NEW = auto()

    PUBLIC = auto()
    PRIVATE = auto()
    SELF = auto()

    WHERE = auto()

    IDENT = auto()
    OPERATOR = auto()
    INTRINSIC = auto()

    EOF = auto()


class Token:

    def __init__(self, token_type: TokenType | None, lexeme: str, token_kind: TokenType | None, position: tuple[int, tuple[int, int]], filename: str) -> None:
        self.token_type = token_type
        self.lexeme = lexeme
        self.token_kind = token_kind
        self.position = position
        self.filename = filename

    def pprint(self, indent: int) -> None:
        print(f"{' ' * indent}Operator({self.lexeme})")