from typing import Optional

class Color():
    __default = "\033[0m"

    def __init__(self, value: Optional[str] = None):
        if value == None:
            self.value = self.__default
            
        elif value.startswith("\033"):
            self.value = value
            
        elif value.startswith("#"):
            value = value.lstrip("#")
            r = int(value[0:2], 16)
            g = int(value[2:4], 16)
            b = int(value[4:6], 16)
            self.value = f"\033[38;2;{r};{g};{b}m"
            
        else:
            raise Exception(f'Tried to initialize an invalid color: "{value}".')

    def format(self, input) -> str:
        return f'{self.value}{input}{self.__default}'