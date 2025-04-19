from cliapp.util.defaults import VERSION
from cliapp.config.base import BaseConfig, ConfigValue

class VersionConfig(BaseConfig):
    major: int
    minor: int
    patch: int
    
    values = [
        ConfigValue("major", VERSION),
        ConfigValue("minor", VERSION),
        ConfigValue("patch", VERSION)
    ]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.string = f"{self.major}.{self.minor}.{self.patch}"