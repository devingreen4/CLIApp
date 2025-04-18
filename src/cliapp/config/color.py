from cliapp.util.defaults import COLOR
from cliapp.util.color import Color
from cliapp.config.base import BaseConfig, ConfigValue

class ColorConfig(BaseConfig):
    primary: Color
    secondary: Color
    text: Color
    
    values = [
        ConfigValue("primary", COLOR, Color),
        ConfigValue("secondary", COLOR, Color),
        ConfigValue("text", COLOR, Color)
    ]