import os
from typing import Optional
from pyfiglet import Figlet
from cmd2.ansi import strip_style

def terminalWidth() -> int:
    return os.get_terminal_size().columns
    
def asciiArt(value: str, font: str, width: Optional[int] = None) -> str:
    width = terminalWidth() if width == None else width
    
    figlet = Figlet(font=font, width=width)
    render = figlet.renderText(value)
    
    lines = render.splitlines()
    while lines and not strip_style(lines[0]).strip():
        lines.pop(0)
    while lines and not strip_style(lines[-1]).strip():
        lines.pop()
    
    NEW_LINE = "\n"
    return NEW_LINE + NEW_LINE.join(lines) + NEW_LINE * 2