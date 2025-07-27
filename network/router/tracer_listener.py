# tracer_listener.py
from core.event_bus import event_bus, TickEvent, TracerMovedEvent

async def on_tick_for_tracer(event: TickEvent):
    """
    Placeholder tracer logic: on each tick, evaluate bloom tags and move tracers.
    Publishes a TracerMovedEvent with new location and reason.
    """
    # --- replace the following stubs with real tracer logic ---
    from tracer import get_active_bloom_tags, process_tracer_movement
    tags = get_active_bloom_tags()
    new_node, reason = process_tracer_movement(tags)
    await event_bus.publish(TracerMovedEvent(new_location=new_node, reason=reason))

# register tracer listener
event_bus.subscribe(TickEvent, on_tick_for_tracer)


# pulse_emitter.py
from core.event_bus import event_bus, TickEvent, PulseEvent

class PulseEmitter:
    def __init__(self, gas_pedal, activity_sensor):
        self.gas_pedal = gas_pedal
        self.activity_sensor = activity_sensor

    async def on_tick(self, event: TickEvent):
        """
        On every tick, read semantic heat and activity levels,
        select the optimal LLM model, then publish a PulseEvent.
        """
        heat = await self.gas_pedal()
        activity = await self.activity_sensor()
        model = self.select_model(heat, activity)
        await event_bus.publish(PulseEvent(model=model, heat=heat, activity=activity))
        print(f"📡 PulseEvent -> model={model}, heat={heat:.2f}, activity={activity:.2f}")

    def select_model(self, heat: float, activity: float) -> str:
        """
        Example selection logic: choose heavier models under high pressure,
        lighter ones when system load is low.
        """
        score = 0.7 * heat + 0.3 * activity
        if score > 0.8:
            return "gpt-4o"
        if score > 0.5:
            return "gpt-4o-mini"
        return "gpt-3.5-turbo"

# In main.py or dev_bootstrap.py, add:
#
# from pulse_emitter import PulseEmitter
#
# # after you define or import your sensors:
# pulse_emitter = PulseEmitter(
#     gas_pedal=mock_gas_pedal,
#     activity_sensor=mock_activity
# )
# event_bus.subscribe(TickEvent, pulse_emitter.on_tick)

# Ensure tracer_listener.py is imported before engine.start(), and pulse_emitter is registered.
