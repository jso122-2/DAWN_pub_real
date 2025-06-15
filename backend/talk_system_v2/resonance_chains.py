from typing import List, Dict, Any

class ResonanceChain:
    """Represents a chain of semantically linked glyphs (memories)."""
    def __init__(self, chain_id: str, glyph_ids: List[str], mood: str, created_tick: int):
        self.chain_id = chain_id
        self.glyph_ids = glyph_ids
        self.mood = mood
        self.created_tick = created_tick
        self.last_active_tick = created_tick
        self.metadata: Dict[str, Any] = {}

    def add_glyph(self, glyph_id: str, tick: int):
        self.glyph_ids.append(glyph_id)
        self.last_active_tick = tick

class ResonanceChainManager:
    """Manages resonance chains for DAWN's consciousness."""
    def __init__(self, glyph_memory):
        self.glyph_memory = glyph_memory
        self.chains: Dict[str, ResonanceChain] = {}

    def prune_inactive_chains(self, threshold: float = 0.1) -> int:
        # Stub: do nothing, return 0
        return 0

    def get_active_threads(self, mood: str, limit: int = 5) -> List[Dict]:
        # Return a list of active chains for the current mood
        return [
            {
                "chain_id": chain.chain_id,
                "glyph_ids": chain.glyph_ids,
                "mood": chain.mood,
                "last_active_tick": chain.last_active_tick
            }
            for chain in self.chains.values()
            if chain.mood == mood
        ][:limit]

    def extend_chains(self, user_input: str, glyph_id: str, resonance_strength: float, tick: int):
        # For now, just create or update a chain for the glyph
        chain_id = f"chain_{glyph_id}"
        if chain_id not in self.chains:
            self.chains[chain_id] = ResonanceChain(chain_id, [glyph_id], "UNKNOWN", tick)
        else:
            self.chains[chain_id].add_glyph(glyph_id, tick)
        return [self.chains[chain_id].__dict__] 