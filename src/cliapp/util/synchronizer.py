import asyncio
from typing import *

def run(method: Coroutine, *args, **kwargs):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(method(*args, **kwargs))
    loop.close()
    
async def resolve(futures: List[asyncio.Future]):
    return await asyncio.gather(*futures)

async def execute(function: Callable, *args, **kwargs):
    def blockingFn():
        return function(*args, **kwargs)
    
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, blockingFn)