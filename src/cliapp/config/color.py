from cliapp.util.defaults import COLOR
from cliapp.config.base import BaseConfig, ConfigValue
from cmd2 import RgbFg

def color(hex: str) -> RgbFg:
    value = hex.lstrip("#")
    r = int(value[0:2], 16)
    g = int(value[2:4], 16)
    b = int(value[4:6], 16)
    return RgbFg(r, g, b)

class ColorConfig(BaseConfig):
    primary: RgbFg
    secondary: RgbFg
    text: RgbFg
    
    values = [
        ConfigValue("primary", COLOR, color),
        ConfigValue("secondary", COLOR, color),
        ConfigValue("text", COLOR, color)
    ]