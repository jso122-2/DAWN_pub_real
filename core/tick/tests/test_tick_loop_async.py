import asyncio
import pytest
from core.tick.tick_loop import TickLoop

async def test_sync_vs_async_no_crash():
    loop = TickLoop(tick_rate=0.01)
    called = {"sync": 0, "async": 0}

    def sync_handler(delta):
        called["sync"] += 1

    async def async_handler(delta):
        called["async"] += 1

    loop.register_subsystem("sync", sync_handler)
    loop.register_subsystem("async", async_handler)

    task = asyncio.create_task(loop.start())
    await asyncio.sleep(0.05)   # run a few ticks
    await loop.stop()
    await task

    assert called["sync"] > 0 and called["async"] > 0 