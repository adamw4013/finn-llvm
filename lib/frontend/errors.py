from .token import Token

from rich.console import Console

class ErrorPrinter:

    def __init__(self, lines: list[str], message: str, token: Token) -> None:
        self.lines = lines
        self.message = message
        self.token = token

        self.padding: int = 2
        self.console = Console()

        self.output: str = ""


    def construct_message(self) -> None:
        buffer_lines: list[str] = []
        count: int = 0
        for i in range(self.token.position[0] - 1, len(self.lines)):
            try:
                if count <= 3:
                    buffer_lines.append(self.lines[i])
                    count += 1
            except:
                pass
        line_number_padding: int = 4 + len(str(self.token.position[0]))
        self.output += f"[bold]{self.token.filename}[/]:[bold blue]{self.token.position[0]}[/][white]:[/][bold blue]{self.token.position[1][0]}[/]: \n{' ' * line_number_padding}│\n"
        self.output += f"{' ' * self.padding} [bold blue]{self.token.position[0]}[/] │ {buffer_lines[0]}\n"
        self.output += f"{' ' * line_number_padding}│{' ' * self.token.position[1][0]}{'^' * (self.token.position[1][1] - self.token.position[1][0])}\n"
        self.output += f"{' ' * line_number_padding}│{' ' * self.token.position[1][0]}{self.message}\n"
        self.output += f"{' ' * line_number_padding}│\n"
        for count in range(1, len(buffer_lines)):
            self.output += f"{' ' * self.padding} [bold blue]{self.token.position[0] + count}[/] │ {buffer_lines[count]}\n"

    def print_error(self) -> None:
        self.construct_message()
        self.console.print(self.output)