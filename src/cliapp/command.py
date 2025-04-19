from argparse import ArgumentParser
from typing import Callable, Optional, Coroutine
import inspect
import shlex
from cliapp.util import synchronizer

class Command():
    def __init__(self, 
                 name: str,
                 executable: Callable | Coroutine = lambda *args, **kwargs: None):
        
        self.name = name
        self.__executable = executable
        
        self.__parser = ArgumentParser(prog=name)
        self.__parser.add_argument("input", nargs="*", help=f"An string input for {name}()")
        
        self.exec = lambda s: self._exec(s)
        self.help = lambda: self.__parser.print_help()
        
    def _exec(self, statement):
        try:
            argv = shlex.split(statement)
            args = self.__parser.parse_args(argv)
            
            kwargs = vars(args)
            input = kwargs.pop('input')
            
            
            if inspect.iscoroutinefunction(self.__executable):
                synchronizer.run(self.__executable, *input, **kwargs)
            else:
                self.__executable(*input, **kwargs)
            
        except BaseException as e:
            print(e)
            return
        
    def addFlag(self, short, full = None, help: Optional[str] = None):
        if help == None: help = f'a flag labeled "-{short}"'
        
        flags = [f"-{short}"]
        if full != None: flags.append(f"--{full}")
        
        self.__parser.add_argument(*flags, action="store_true", help=help)