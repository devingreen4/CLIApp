from cliapp import Application
from cliapp import Command
import asyncio

async def test(*args, n=False, t=False):
    print(*args)
    await asyncio.sleep(5)

if __name__ == "__main__":
    app = Application(config="tests/config.json")
    
    command = Command("test", test)
    command.addFlag("n", help="Should show number result")
    command.addFlag("t")
    
    app.add(command)
    
    app.run()
    
    
# sub-zero, larry3d, ansi_shadow, ansi_regular, big-money-ne