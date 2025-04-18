from cliapp.util.defaults import FONT
from cliapp.config.base import BaseConfig, ConfigValue
from cliapp.config.color import ColorConfig

class ThemeConfig(BaseConfig):
    color: ColorConfig
    font: str
    
    values = [
        ConfigValue("color", ColorConfig()),
        ConfigValue("font", FONT)
    ]