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