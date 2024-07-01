# type: ignore
from importlib.util import find_spec

if find_spec("llvmlite") is None:
    print("[ ERR ] LLVMLite : Attempting to install llvmlite")
    from subprocess import call
    call("pip install llvmlite")
    call(f"python {__file__}")
else:
    print("[ OK ] LLVMLite")

from sys import argv
from os.path import exists

init: bool = False
time: bool = False

path: str = ""

for arg in argv:

    match arg:

        case "init":
            init = True

        case "-t":
            time = True

        case _:
            if exists(arg):
                path = arg
            else:
                print(f"Invalid command: \"{arg}\"")
                exit(1)

from lib.frontend.token import Token
from lib.frontend.lexer import Lexer
from lib.frontend.parser import Parser

with open(path, "r") as file:
    contents: str = file.read()
    lines: list[str] = contents.splitlines()
    tokens: list[Token] = Lexer(contents, path, lines).lex()
    expr = Parser(tokens, lines).parse()
    for guh in expr:
        guh.pprint()