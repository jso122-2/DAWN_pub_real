# bloom_event.py

class BloomEmitted:
    def __init__(self, source: str, mood_tag: str, semantic_seeds: list[str]):
        self.source = source
        self.mood_tag = mood_tag
        self.semantic_seeds = semantic_seeds
