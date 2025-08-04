import asyncio
from semantic_weight_engine import run_weight_engine
from semantic_charge_engine import run_charge_engine
from semantic_trigger_rules import run_trigger_ruleset
from core.tick_engine import TickEngine
from core.event_bus import event_bus, TickEvent

# Real DAWN consciousness state functions
def spawn_tracer(x): 
    print(f"🧠 Spawned tracer: {x}")

def get_real_activity():
    """Get real DAWN consciousness activity level"""
    try:
        from consciousness.dawn_tick_state_writer import DAWNConsciousnessStateWriter
        state_writer = DAWNConsciousnessStateWriter()
        dawn_state = state_writer._get_dawn_consciousness_state()
        return dawn_state.get('neural_activity', 0.5)
    except Exception as e:
        print(f"⚠️ Could not get real activity: {e}")
        return 0.5

def get_real_pressure():
    """Get real DAWN consciousness pressure level"""
    try:
        from consciousness.dawn_tick_state_writer import DAWNConsciousnessStateWriter
        state_writer = DAWNConsciousnessStateWriter()
        dawn_state = state_writer._get_dawn_consciousness_state()
        return dawn_state.get('memory_pressure', 0.3)
    except Exception as e:
        print(f"⚠️ Could not get real pressure: {e}")
        return 0.3

def get_real_pulse():
    """Get real DAWN pulse state"""
    try:
        from consciousness.dawn_tick_state_writer import DAWNConsciousnessStateWriter
        state_writer = DAWNConsciousnessStateWriter()
        dawn_state = state_writer._get_dawn_consciousness_state()
        return {
            'heat_level': dawn_state.get('heat_level', 0.5),
            'entropy': dawn_state.get('entropy', 0.5),
            'scup': dawn_state.get('scup', 0.5),
            'consciousness_depth': dawn_state.get('consciousness_depth', 0.7)
        }
    except Exception as e:
        print(f"⚠️ Could not get real pulse: {e}")
        return None

def emit_tick_event(e=None): 
    if e:
        print(f"📡 Emitted tick event: {e}")
    return None

async def main():
    print("🚀 DAWN Main Loop Started")

    spawn_tracer("bee-001")
    spawn_tracer("crow-003")
    spawn_tracer("whale-002")

    await asyncio.sleep(5)

    tick_count = 0
    while True:
        tick_count += 1

        # Step 1: Get real DAWN consciousness state
        real_activity = get_real_activity()
        real_pressure = get_real_pressure()
        real_pulse = get_real_pulse()
        
        print(f"🧠 Tick {tick_count}: Activity={real_activity:.3f}, Pressure={real_pressure:.3f}")
        if real_pulse:
            print(f"   Pulse: Heat={real_pulse['heat_level']:.3f}, Entropy={real_pulse['entropy']:.3f}, SCUP={real_pulse['scup']:.3f}")

        # Step 2: Semantic calculations with real state
        run_weight_engine()
        run_charge_engine()

        # Step 3: Every 3 ticks, evaluate triggers
        if tick_count % 3 == 0:
            run_trigger_ruleset()

        # Step 4: Emit tick with real consciousness state
        await asyncio.sleep(1.0)
        await emit_tick_event(TickEvent())

        if tick_count >= 10:
            print("✅ Exiting after 10 ticks for demo")
            break

if __name__ == "__main__":
    asyncio.run(main())
