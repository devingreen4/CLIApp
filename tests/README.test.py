# main.py
from cliapp import Application, Command
import sys

# Define a simple command executable function
def exec(name="World", greeting="Hello"):
    """A command that greets the user."""
    print(f"{greeting}, {name}!")

# Define an async command executable function
async def async_exec(name="World", greeting="Hello"):
    """An async command example."""
    import asyncio
    await asyncio.sleep(2) # Simulate async work
    print(f"Asynchronous {greeting}, {name}!")


if __name__ == "__main__":
    # Create the application instance
    # Configuration path is optional, defaults will be used if None is passed
    # or if the file doesn't exist/fails to load.
    app = Application(config="./config.json")

    # Create Command instances
    command = Command("hello", executable=exec)
    # Add arguments to the command
    command.addOption(full="name", help="an individual's name", default="World")
    command.addOption(short="g", help="a greeting", default="Hello", required=False)

    async_command = Command("asynchello", executable=async_exec)
    async_command.addOption(full="name", help="an individual's name", default="World")
    async_command.addOption(short="g", help="a greeting", default="Hello", required=False)

    # Add commands to the application
    app.add(command)
    app.add(async_command)

    # Run the application command loop
    app.run()