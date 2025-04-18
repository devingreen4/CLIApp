# CLIApp

CLIApp is a Python framework designed to help you build interactive command-line applications quickly. It leverages the powerful [`cmd2`](https://cmd2.readthedocs.io/) library, providing a solid foundation with features like configuration loading, theme customization, and easy integration of custom commands.

## Features

### Interactive Shell
Robust command parsing, history, and editing powered by `cmd2`.

### Configuration Driven
Load application settings (names, author, version) and appearance from a JSON file.

### Defaults Included
Runs with sensible defaults if no configuration file is provided, making it easy to get started.

### Themeable
Customize shell prompts, intro/outro messages, fonts, and colors (primary, secondary, text) via configuration.

### Modular Commands
Integrate your own commands seamlessly using `cmd2`'s `CommandSet` feature.

### Built-in Commands
Includes essential commands like `exit`, `clear`, `help`, and `welcome`.

### Asynchronous Core
Designed with async operations in mind.

### Graceful Exit
Handles `Ctrl+C` (SIGINT) for a clean shutdown.

## Installation

Make sure you have Python and pip installed.

```bash
pip install cliapp
````

## Configuration

CLIApp uses a JSON file (e.g., `config.json`) to manage settings. You can specify the path to this file when creating the `Application` instance.

If no `configPath` is provided, the application will initialize with built-in default values, allowing you to run a basic version immediately or generate a starting point.

**Example `config.json`:**

```json
{
    "shortname": "MyApp",
    "fullname": "My Awesome CLI Application",
    "author": "Your Name <your.email@example.com>",
    "version": {
        "major": 1,        
        "minor": 0,     
        "patch": 0     
    },
    "theme": {
        "color": {
            "primary": "#5F9EA0",   
            "secondary": "#B0C4DE", 
            "text": "#FFFFFF"       
        },
        "font": "standard" 
    },
    "shell": {
        "prompt": ">>",
        "intro": "Welcome to MyApp! Type 'help' for commands.",
        "outro": "Exiting MyApp. Goodbye!"
    }
}
```

  * `shortname`, `fullname`, `author`: Basic application metadata.
  * `version`: Defines the application version (major, minor, patch). The application code may internally derive a version string.
  * `theme`: Controls visual aspects.
      * `color`: Define hex codes or color names (ensure compatibility with your terminal/color library) for primary elements (banners, prompt), secondary elements (headers), and standard text.
      * `font`: Specifies the font for the banner (refer to underlying library, e.g., `pyfiglet`, for available fonts).
  * `shell`: Customizes interactive elements like the prompt, intro message, and exit message.

## Usage

Create a main script (e.g., `main.py`) to instantiate your commands and the application, then run it.

```python
#!/usr/bin/env python
import sys
from cliapp import Application  # Your main application class
from cmd2 import CommandSet, with_default_category, Cmd2ArgumentParser, with_argparser

# --- Define Custom Commands using CommandSet ---
@with_default_category('My Custom Commands')
class MyCommands(CommandSet):

    def __init__(self):
        super().__init__()

    # Example command using argparser
    argparser = Cmd2ArgumentParser()
    argparser.add_argument('-p', '--prefix', default='Pong:', help='Prefix for the reply')
    @with_argparser(argparser)
    def do_ping(self, args):
        """Check if the application is responsive."""
        self.app.emit(f"{args.prefix} Application is running!") # Use self.app to access Application methods like emit

    def do_status(self, args):
        """Show some status."""
        self.app.emit("Status: OK")
        self.app.emit(f"Configured name: {self.app.c.fullname}") # Access config via self.app.c

# --- Main Application Execution ---
if __name__ == "__main__":
    # Optionally specify the path to your configuration file
    # If None, default config values will be used.
    config_path = "config.json"  # Or set to None

    # Pass command line arguments and optional config path
    app = Application(sys.argv, configPath=config_path)

    # --- Register Command Sets ---
    my_command_set = MyCommands()
    app.register_command_set(my_command_set)
    # Register other command sets here...

    # Run the application's main loop
    app.run()
```

Run your application from the terminal:

```bash
python main.py
```

This will start the interactive shell where you can use built-in commands and any custom commands you registered via `CommandSet`s.

## Adding Custom Commands

As shown in the [Usage](https://www.google.com/search?q=%23usage) example, custom commands should be organized into classes that inherit from `cmd2.CommandSet`.

1.  **Create a `CommandSet` Class:** Define methods starting with `do_` (e.g., `do_mycommand`) within this class.
2.  **Access Application:** Within your command methods, you can access the main `Application` instance via `self.app`. This allows you to use methods like `self.app.emit()` for output or access the configuration via `self.app.c`.
3.  **Register the `CommandSet`:** Instantiate your `CommandSet` and register it with the `Application` instance using `app.register_command_set(your_command_set_instance)`.

For more details on creating commands, argument parsing (`@with_argparser`), and advanced `CommandSet` features, refer to the [**`cmd2` Documentation**](https://www.google.com/search?q=https://cmd2.readthedocs.io/en/latest/features/command_sets.html).

## Built-in Commands

These commands are provided directly by the `Application` class:

  * `help [command]`: Displays help information. Shows available commands (including those from registered `CommandSet`s) if no specific command is given.
  * `exit`: Exits the application gracefully.
  * `clear`: Clears the terminal screen.
  * `welcome`: Displays the initial welcome banner and messages again.

## Dependencies

  * [cmd2](https://cmd2.readthedocs.io/): For the core interactive shell, command parsing, and `CommandSet` functionality.
  * [pyfiglet](https://github.com/pwaller/pyfiglet): For converting ASCII text into ASCII art.

## License

Distributed under the **MIT License**. See `LICENSE` file for more information.

## Contributing

Contributions are welcome\! Please feel free to open an issue on the repository to discuss bugs or feature requests, or submit a pull request.