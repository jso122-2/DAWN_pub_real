from helix_import_architecture import helix_import
from substrate import pulse_heat
import asyncio
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.tick_engine import TickEngine
from core.tick_hook_autonomous import AutonomousFieldTrigger
from semantic.semantic_weight_engine import run_weight_engine
from core.event_bus import event_bus, TickEvent

engine = TickEngine(...)
engine.tick_hook = AutonomousFieldTrigger().on_tick

async def activity_sensor():
    return 0.7  # placeholder for dynamic activity

async def pressure_sensor():
    return PulseHeat.get_instance().current_pressure

async def emit_tick_event():
    await event_bus.publish(TickEvent())

async def main():
    print("[DAWN] 🚀 Starting TickEngine with semantic weighting...")
    engine = TickEngine(
        base_interval=1.0,
        alpha=0.3,
        beta=0.4,
        activity_sensor=activity_sensor,
        pressure_sensor=pressure_sensor,
        emit_tick_event=emit_tick_event
    )

    await run_weight_engine(engine)

if __name__ == "__main__":
    asyncio.run(main())
