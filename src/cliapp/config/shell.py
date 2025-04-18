from cliapp.util.defaults import PROMPT, INTRO, OUTRO
from cliapp.config.base import BaseConfig, ConfigValue

class ShellConfig(BaseConfig):
    prompt: str
    intro: str
    outro: str
    
    values = [
        ConfigValue("prompt", PROMPT, lambda val: f"{val} " if val[-1] != " " else val),
        ConfigValue("intro", INTRO),
        ConfigValue("outro", OUTRO)
    ]