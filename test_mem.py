import asyncio
from src.ai_interaction import do_manage_memory
from src.context_budget import _memory_manager

async def test():
    print(await do_manage_memory("add\nTest memory\nfact", owner=None))
    print("Memories:", _memory_manager.load(owner=None))

asyncio.run(test())
