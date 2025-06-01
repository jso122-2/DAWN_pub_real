import asyncio
from tick_engine import TickEngine
from tick_listener import on_tick  # ensures listener is registered
from event_bus import event_bus, TickEvent

async def emit_tick():
    await event_bus.publish(TickEvent())

async def mock_activity():
    return 0.5  # placeholder, replace with dynamic activity later

async def mock_gas_pedal():
    return 1.0  # placeholder, replace with semantic pressure logic

async def main():
    engine = TickEngine(
        base_interval=1.0,
        alpha=0.2,
        activity_sensor=mock_activity,
        gas_pedal=mock_gas_pedal,
        emit_tick_event=emit_tick
    )
    await engine.start()

if __name__ == "__main__":
    asyncio.run(main())
