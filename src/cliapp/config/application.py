from cliapp.util.defaults import SHORTNAME, FULLNAME, AUTHOR
from cliapp.config.base import BaseConfig, ConfigValue
from cliapp.config.version import VersionConfig
from cliapp.config.theme import ThemeConfig
from cliapp.config.shell import ShellConfig

class ApplicationConfig(BaseConfig):
    shortname: str
    fullname: str
    author: str
    version: VersionConfig
    theme: ThemeConfig
    shell: ShellConfig
    
    values = [
        ConfigValue("shortname", SHORTNAME),
        ConfigValue("fullname", FULLNAME),
        ConfigValue("author", AUTHOR),
        ConfigValue("version", VersionConfig()),
        ConfigValue("theme", ThemeConfig()),
        ConfigValue("version", ShellConfig()),
    ]