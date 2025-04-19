import os
from functools import partial
from cmd2 import Cmd, style, DEFAULT_SHORTCUTS
from cmd2.table_creator import Column, SimpleTable
from cmd2.utils import align_center
from typing import Optional, List
from cliapp.util.tools import asciiArt
from cliapp.config import ApplicationConfig
from cliapp.command import Command

class Interface(Cmd):
    def __init__(self, config: ApplicationConfig):
        shortcuts = dict(DEFAULT_SHORTCUTS)
        shortcuts.pop("@")
        shortcuts.pop("@@")
        
        super().__init__(shortcuts=shortcuts, auto_load_commands=False)
        del Cmd.do_alias
        del Cmd.do_macro
        del Cmd.do_run_pyscript
        del Cmd.do_run_script
        del Cmd.do_set
        
        self.__config = config
        
        self.intro = self.__introBanner()
        self.prompt = f"{style(self.__config.shortname, fg=self.__config.theme.color.primary)} {style(self.__config.shell.prompt, fg=self.__config.theme.color.text)}"
        self.editor = "code"
        self.debug = True
        self.continuation_prompt = "> "
        self.default_category = 'Default Commands'
        self.default_error = "Unknown command: {}."
    
    def precmd(self, statement):
        self.doc_header = self.__helpBanner()
        return super().precmd(statement)
        
    def poutput(self, msg = '', *, end = '\n'):
        style_text = partial(style, fg=self.__config.theme.color.text)
        return self.print_to(self.stdout, msg, end=end, style=style_text)
        
    def __introBanner(self) -> str:
        banner = asciiArt(self.__config.shortname, self.__config.theme.font)
        banner = align_center(banner)
        banner = style(banner, fg=self.__config.theme.color.primary)
        
        title = f"Welcome to {self.__config.fullname}!"
        subtitle = f"Version {self.__config.version.string}. Created by {self.__config.author}."
        message = "\n".join([title, subtitle]) + "\n"
        message = align_center(message)
        message = style(message, fg=self.__config.theme.color.text)
        
        intro = style(self.__config.shell.intro, fg=self.__config.theme.color.secondary)
        
        return "\n".join([banner, message, intro])
    
    def __helpBanner(self) -> str:
        banner = asciiArt("Help", "sub-zero")#self.__config.theme.font)
        banner = align_center(banner)
        banner = style(banner, fg=self.__config.theme.color.secondary)
        
        message = "Documented commands (use 'help -v' for verbose/'help <topic>' for details):"
        message = align_center(message)
        message = style(message, fg=self.__config.theme.color.text)
        
        return "\n".join([banner, message])
        
    def do_quit(self, statement):
        """Exit this application"""
        print()
        outro = style(self.__config.shell.outro, fg=self.__config.theme.color.secondary)
        print(outro)
        return super().do_quit(statement)
    
    def do_exit(self, statement):
        """Exit this application"""
        return self.do_quit(statement)
    
    def do_clear(self, _):
        'Clear the terminal screen'
        os.system('clear')
    
    
    
    
    
    
    
    #
    # Manipulate the help-menu table by overriding the original functionality
    #
            
    def print_topics(self, header: str, cmds: Optional[List[str]], _: int, maxcol: int) -> None:
        """
        Print groups of commands and topics in columns and an optional header
        Override of cmd's print_topics() to handle headers with newlines, ANSI style sequences, and wide characters

        :param header: string to print above commands being printed
        :param cmds: list of topics to print
        :param cmdlen: unused, even by cmd's version
        :param maxcol: max number of display columns to fit into
        """
        from cmd2.utils import align_left
        from cliapp.util.tools import terminalWidth
        
        if cmds:
            header = style(header, fg=self.__config.theme.color.secondary)
            self.poutput(header)
            if self.ruler:
                divider = align_left('', fill_char=self.ruler, width=terminalWidth())
                divider = style(divider, fg=self.__config.theme.color.primary)
                self.poutput(divider)
            self.columnize(cmds, maxcol - 1)
            self.poutput()
        
    
    def _print_topics(self, header: str, cmds: List[str], verbose: bool) -> None:
        """Customized version of print_topics that can switch between verbose or traditional output"""
        import io
        from typing import TextIO, cast
        from contextlib import redirect_stdout
        from cmd2 import constants, ansi
        from cmd2.utils import strip_doc_annotations
        from cliapp.util.tools import terminalWidth

        if cmds:
            if not verbose:
                self.print_topics(header, cmds, 15, 80)
            else:
                # Find the widest command
                widest = max([ansi.style_aware_wcswidth(command) for command in cmds])
                
                column_spacing = 2
                name_column_width = max(widest, 20)
                desc_column_width = terminalWidth() - name_column_width - column_spacing

                # Define the table structure
                name_column = Column('', width=name_column_width)
                desc_column = Column('', width=desc_column_width)

                topic_table = SimpleTable([name_column, desc_column], column_spacing=column_spacing, divider_char=self.ruler)

                # Build the topic table
                table_str_buf = io.StringIO()
                if header:
                    header = style(header, fg=self.__config.theme.color.secondary)
                    table_str_buf.write(header + "\n")

                divider = topic_table.generate_divider()
                divider = style(divider, fg=self.__config.theme.color.primary)
                if divider:
                    table_str_buf.write(divider + "\n")

                # Try to get the documentation string for each command
                topics = self.get_help_topics()
                for command in cmds:
                    if (cmd_func := self.cmd_func(command)) is None:
                        continue

                    doc: Optional[str]

                    # If this is an argparse command, use its description.
                    if (cmd_parser := self._command_parsers.get(cmd_func)) is not None:
                        doc = cmd_parser.description

                    # Non-argparse commands can have help_functions for their documentation
                    elif command in topics:
                        help_func = getattr(self, constants.HELP_FUNC_PREFIX + command)
                        result = io.StringIO()

                        # try to redirect system stdout
                        with redirect_stdout(result):
                            # save our internal stdout
                            stdout_orig = self.stdout
                            try:
                                # redirect our internal stdout
                                self.stdout = cast(TextIO, result)
                                help_func()
                            finally:
                                # restore internal stdout
                                self.stdout = stdout_orig
                        doc = result.getvalue()

                    else:
                        doc = cmd_func.__doc__

                    # Attempt to locate the first documentation block
                    cmd_desc = strip_doc_annotations(doc) if doc else ''

                    # Add this command to the table
                    table_row = topic_table.generate_data_row([command, cmd_desc])
                    table_str_buf.write(table_row + '\n')

                self.poutput(table_str_buf.getvalue())
    