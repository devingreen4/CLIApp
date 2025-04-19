from cmd2 import CommandSet, categorize
from cmd2.constants import HELP_FUNC_PREFIX, COMMAND_FUNC_PREFIX
from typing import Optional, List, Callable
from cliapp.config import ApplicationConfig
from cliapp.interface import Interface
from cliapp.command import Command

class ApplicationCommandSet(CommandSet): 
    def __init__(self):
        super().__init__()

class Application():
    def __init__(self, config: Optional[str] = None):
        self.__config: ApplicationConfig = ApplicationConfig.fromPath(config)
        self.__interface = Interface(self.__config)
        
        self.commands: List[Command] = []
        
        # signal.signal(signal.SIGINT, self.signal_handler)
        
        # intro = Text(
        #     self.c.shell.intro, 
        #     color=self.c.theme.color.secondary, 
        #     padding=0
        # ).render()
        # self.intro = intro
        
        # name = self.c.theme.color.primary.format(self.c.shortname)
        # prompt = self.c.shell.prompt
        # self.prompt = f"{name} {prompt}"
        # self.ruler = self.c.theme.color.primary.format("=")
        
        # self.doc_header = self.c.theme.color.secondary.format(f"{self.c.shortname} Commands")
        # self.undoc_header = self.c.theme.color.secondary.format("Experimental Commands")
        # self.misc_header = self.c.theme.color.secondary.format("Additional Help Items")
    
    def __setMethod(self, name: str, exec: Callable):        
        setattr(self.__interface, name, exec)
        func = getattr(self.__interface, name)
        categorize(func, f"{self.__config.shortname} Commands")
    
    def __reloadMethods(self):
        for command in self.commands:
            self.__setMethod(COMMAND_FUNC_PREFIX + command.name, command.exec)
            self.__setMethod(HELP_FUNC_PREFIX + command.name, command.help)
    
    def add(self, command: Command):
        self.commands.append(command)
        self.__reloadMethods()
        
    def run(self):
        self.__interface.cmdloop()
        
    
    