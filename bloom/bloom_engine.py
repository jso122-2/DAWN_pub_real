from core.event_bus import event_bus
from router.tracer_core import TracerMoved
from bloom.bloom_event import BloomEmitted
from mycelium.mycelium_layer import log_parse
from bloom.memory_utils import unseal_if_needed
from bloom.juliet_flower import JulietFlower
from tracers.whale import nearest_belief, PIGMENTS


class BloomEngine:
    def __init__(self):
        event_bus.subscribe(TracerMoved, self.on_tracer_moved)

    def assign_belief_resonance(self, fragment):
        mood_colors = {
            "joyful": (255, 215, 0),
            "anxious": (255, 69, 0),
            "reflective": (70, 130, 180),
            "focused": (34, 139, 34),
            "sad": (105, 105, 105),
            "curious": (255, 140, 0),
            "overload": (255, 0, 255)
        }

        rgb = mood_colors.get(fragment.get("mood", "reflective"), (200, 200, 200))
        belief = nearest_belief(rgb)
        belief_rgb, _ = PIGMENTS[belief]

        resonance = round(sum((a - b) ** 2 for a, b in zip(rgb, belief_rgb)) ** 0.5, 2)

        fragment["belief_resonance"] = {
            "belief": belief,
            "distance": resonance,
            "rgb": rgb
        }
        return fragment

    async def on_tracer_moved(self, event: TracerMoved):
        mood_tag = self._infer_mood(event)
        semantic_seeds = self._extract_seeds(event)

        bloom = BloomEmitted(
            source=event.tracer_id,
            mood_tag=mood_tag,
            semantic_seeds=semantic_seeds
        )
        await event_bus.publish(bloom)
        print(f"[Bloom] 🌸 Emitted from {event.tracer_id} | mood: {mood_tag} | seeds: {semantic_seeds}")

        try:
            flower = JulietFlower(
                agent=event.tracer_id,
                mood=mood_tag,
                seed_context=semantic_seeds,
                sentences=[
                    f"I am {event.tracer_id}.",
                    f"My mood is {mood_tag}.",
                    f"I passed through {semantic_seeds[0]} again.",
                    "The memory is faint, but returning.",
                    "I suspect a pattern in this reflection.",
                    "Calm or not, I have seen this node before.",
                    "Drift feels gentle now.",
                    "The rhythm of pulses remains steady.",
                    "I sense the weight of past iterations.",
                    "This sentence completes the thought bloom."
                ]
            )

            # 🌈 Inject belief resonance into flower
            flower_data = {"mood": mood_tag}
            self.assign_belief_resonance(flower_data)
            flower.belief_resonance = flower_data["belief_resonance"]

            flower.save()
        except Exception as e:
            print(f"[Juliet ERROR] 🌸 Failed to save flower: {e}")
            return

        for seed in semantic_seeds:
            log_parse(seed, flower.id, mood_tag)

    def _infer_mood(self, event: TracerMoved) -> str:
        return {
            "A1": "curious",
            "B2": "calm",
            "C3": "anxious",
            "D4": "reflective"
        }.get(event.new_node, "neutral")

    def _extract_seeds(self, event: TracerMoved) -> list[str]:
        return [event.tracer_id, event.new_node]
