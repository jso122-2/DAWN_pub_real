"""
Unified Bloom Memory System
Consolidates all memory-related functionality for the DAWN bloom system
"""

import os
import json
import shutil
import random
from datetime import datetime
from typing import Dict, Optional, List, Any
from dataclasses import dataclass

# ============== Core Memory Functions ==============

class BloomMemoryManager:
    """Unified manager for all bloom memory operations"""
    
    def __init__(self, base_dir: str = "juliet_flowers"):
        self.base_dir = base_dir
        self.sealed_dir = os.path.join(base_dir, "sealed")
        self.metadata_dir = os.path.join(base_dir, "bloom_metadata")
        self.ensure_directories()
        
    def ensure_directories(self):
        """Ensure all required directories exist"""
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.sealed_dir, exist_ok=True)
        os.makedirs(self.metadata_dir, exist_ok=True)
        
    def write_bloom_memory(self, bloom: Any, fractal_path: str) -> str:
        """
        Save bloom memory metadata as JSON file
        Unified version of bloom_memory.py and memory_bloom.py
        """
        # Extract bloom attributes
        mood = getattr(bloom, 'mood', bloom.get('mood', 'neutral'))
        seed = getattr(bloom, 'seed', bloom.get('seed', 'unknown'))
        bloom_id = getattr(bloom, 'bloom_id', bloom.get('bloom_id', f'bloom_{int(datetime.now().timestamp())}'))
        
        # Create directory structure
        folder = os.path.join(self.base_dir, seed, mood)
        os.makedirs(folder, exist_ok=True)
        
        # Prepare memory dictionary
        memory = {
            "bloom_id": bloom_id,
            "lineage_depth": getattr(bloom, 'lineage_depth', bloom.get('lineage_depth', 0)),
            "entropy_score": getattr(bloom, 'entropy_score', bloom.get('entropy_score', 0.0)),
            "mood": mood,
            "bloom_factor": getattr(bloom, 'bloom_factor', bloom.get('bloom_factor', 1.0)),
            "timestamp": datetime.now().isoformat(),
            "fractal_path": fractal_path,
            "seed": seed,
            "connections": getattr(bloom, 'connections', bloom.get('connections', [])),
            "resonance": getattr(bloom, 'resonance', bloom.get('resonance', 1.0)),
            "decay_rate": getattr(bloom, 'decay_rate', bloom.get('decay_rate', 0.1))
        }
        
        # Write JSON file
        file_path = os.path.join(folder, f"{bloom_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=2)
        
        print(f"📝 Bloom memory saved: {file_path}")
        return file_path
        
    def unseal_memories(self, seed: str) -> int:
        """
        Unseal memories for a specific seed
        Returns number of unsealed files
        """
        sealed_path = os.path.join(self.sealed_dir, seed)
        active_path = os.path.join(self.base_dir, seed)
        
        if not os.path.exists(sealed_path):
            return 0
            
        unsealed_count = 0
        for fname in os.listdir(sealed_path):
            src = os.path.join(sealed_path, fname)
            
            # Determine destination based on file structure
            if os.path.isdir(src):
                # Handle mood subdirectories
                dst = os.path.join(active_path, fname)
                if not os.path.exists(dst):
                    shutil.move(src, dst)
                    print(f"[Memory] 🔓 Unsealed directory {fname} into {seed}/")
                    unsealed_count += 1
            else:
                # Handle individual files
                dst = os.path.join(active_path, fname)
                if not os.path.exists(dst):
                    os.makedirs(active_path, exist_ok=True)
                    shutil.move(src, dst)
                    print(f"[Memory] 🔓 Unsealed {fname} into {seed}/")
                    unsealed_count += 1
                    
        return unsealed_count
        
    def seal_memories(self, seed: str, mood: Optional[str] = None) -> int:
        """
        Seal memories for a specific seed/mood combination
        Returns number of sealed files
        """
        if mood:
            source_path = os.path.join(self.base_dir, seed, mood)
            sealed_path = os.path.join(self.sealed_dir, seed, mood)
        else:
            source_path = os.path.join(self.base_dir, seed)
            sealed_path = os.path.join(self.sealed_dir, seed)
            
        if not os.path.exists(source_path):
            return 0
            
        os.makedirs(sealed_path, exist_ok=True)
        sealed_count = 0
        
        for fname in os.listdir(source_path):
            src = os.path.join(source_path, fname)
            dst = os.path.join(sealed_path, fname)
            shutil.move(src, dst)
            print(f"[Memory] 🔒 Sealed {fname} from {seed}/")
            sealed_count += 1
            
        return sealed_count
        
    def load_bloom_memory(self, seed: str, bloom_id: str, mood: Optional[str] = None) -> Optional[Dict]:
        """Load a specific bloom memory"""
        if mood:
            file_path = os.path.join(self.base_dir, seed, mood, f"{bloom_id}.json")
        else:
            # Search all mood directories
            for mood_dir in os.listdir(os.path.join(self.base_dir, seed)):
                file_path = os.path.join(self.base_dir, seed, mood_dir, f"{bloom_id}.json")
                if os.path.exists(file_path):
                    break
            else:
                return None
                
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
        
    def get_memory_stats(self, seed: Optional[str] = None) -> Dict[str, Any]:
        """Get statistics about stored memories"""
        stats = {
            "total_memories": 0,
            "by_seed": {},
            "by_mood": {},
            "oldest_memory": None,
            "newest_memory": None
        }
        
        # Scan directories
        seeds = [seed] if seed else os.listdir(self.base_dir)
        
        for seed_dir in seeds:
            if seed_dir == "sealed" or seed_dir == "bloom_metadata":
                continue
                
            seed_path = os.path.join(self.base_dir, seed_dir)
            if not os.path.isdir(seed_path):
                continue
                
            seed_count = 0
            for mood_dir in os.listdir(seed_path):
                mood_path = os.path.join(seed_path, mood_dir)
                if not os.path.isdir(mood_path):
                    continue
                    
                mood_count = len([f for f in os.listdir(mood_path) if f.endswith('.json')])
                seed_count += mood_count
                
                stats["by_mood"][mood_dir] = stats["by_mood"].get(mood_dir, 0) + mood_count
                
            stats["by_seed"][seed_dir] = seed_count
            stats["total_memories"] += seed_count
            
        return stats


# ============== Memory Mutation ==============

class MemoryMutator:
    """Handles mutation of suppressed blooms into new forms"""
    
    def __init__(self, memory_manager: BloomMemoryManager):
        self.memory_manager = memory_manager
        
    def mutate_suppressed_bloom(self, bloom: Any, entropy_cutoff: float = 0.5) -> Optional[Dict]:
        """
        Extracts lower-entropy sentences from a suppressed bloom and mutates them
        """
        if not getattr(bloom, "suppressed", False):
            return None
            
        original_sentences = getattr(bloom, "sentences", [])
        entropy_scores = getattr(bloom, "entropy_map", {})
        seed_id = getattr(bloom, "seed_id", "unknown")
        
        # Filter retained sentences
        retained = [
            s for s in original_sentences
            if entropy_scores.get(s, 1.0) <= entropy_cutoff
        ]
        
        if not retained:
            self._log(f"[Mutation Failed] ❌ No viable sentences found in {seed_id}")
            return None
            
        random.shuffle(retained)
        
        # Calculate new parameters
        adjusted_factor = round(getattr(bloom, "bloom_factor", 1.0) * 0.95, 3)
        new_mood = self._mutate_mood(getattr(bloom, "mood", "neutral"))
        
        mutant_seed = {
            "seed_id": f"{seed_id}::mutant",
            "sentences": retained,
            "origin": seed_id,
            "mutation_tag": "suppression_salvage",
            "lineage_depth": getattr(bloom, "lineage_depth", 0) + 1,
            "entropy_score": round(
                sum(entropy_scores.get(s, 0.5) for s in retained) / len(retained), 3
            ),
            "bloom_factor": adjusted_factor,
            "mood": new_mood,
            "belief_resonance": getattr(bloom, "belief_resonance", {}),
            "timestamp": datetime.now().isoformat()
        }
        
        self._log(f"[Mutation] 🧬 {seed_id} salvaged → mutant ({len(retained)} sentences, mood={new_mood}, factor={adjusted_factor})")
        
        # Save mutant memory
        self._save_mutant_memory(mutant_seed)
        
        return mutant_seed
        
    def _mutate_mood(self, original_mood: str) -> str:
        """Mutate mood based on suppression recovery"""
        mood_mutations = {
            "anxious": "curious",
            "overload": "reflective",
            "agitated": "focused",
            "sad": "contemplative"
        }
        return mood_mutations.get(original_mood, "curious")
        
    def _save_mutant_memory(self, mutant_data: Dict):
        """Save mutant bloom memory"""
        file_path = os.path.join(
            self.memory_manager.metadata_dir,
            f"mutant_{mutant_data['seed_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(mutant_data, f, indent=2)
            
        print(f"[Mutation] 💾 Mutant memory saved: {file_path}")
        
    def _log(self, message: str):
        """Log mutation events"""
        try:
            from owl.owl_tracer_log import owl_log
            owl_log(message)
        except ImportError:
            print(message)


# ============== Global Functions ==============

# Create global instance
memory_manager = BloomMemoryManager()
memory_mutator = MemoryMutator(memory_manager)

# Convenience functions for backward compatibility
def write_bloom_json(bloom, fractal_path):
    """Legacy function name compatibility"""
    return memory_manager.write_bloom_memory(bloom, fractal_path)

def unseal_if_needed(seed):
    """Legacy function name compatibility"""
    return memory_manager.unseal_memories(seed)

def mutate_suppressed_bloom(bloom, entropy_cutoff=0.5):
    """Legacy function name compatibility"""
    return memory_mutator.mutate_suppressed_bloom(bloom, entropy_cutoff)

def get_memory_statistics(seed=None):
    """Get memory system statistics"""
    return memory_manager.get_memory_stats(seed)


# ============== Test Functions ==============

if __name__ == "__main__":
    print("🧠 Bloom Memory System Test")
    print("=" * 50)
    
    # Test bloom data
    test_bloom = {
        "bloom_id": "test_bloom_001",
        "seed": "test_seed",
        "mood": "curious",
        "lineage_depth": 3,
        "entropy_score": 0.7,
        "bloom_factor": 1.5
    }
    
    # Test memory writing
    print("\n1. Testing memory write...")
    memory_path = write_bloom_json(test_bloom, "test_fractal.png")
    print(f"   ✓ Memory saved to: {memory_path}")
    
    # Test memory loading
    print("\n2. Testing memory load...")
    loaded = memory_manager.load_bloom_memory("test_seed", "test_bloom_001", "curious")
    if loaded:
        print(f"   ✓ Loaded memory: {loaded['bloom_id']}")
    
    # Test statistics
    print("\n3. Testing memory statistics...")
    stats = get_memory_statistics()
    print(f"   Total memories: {stats['total_memories']}")
    print(f"   By seed: {stats['by_seed']}")
    print(f"   By mood: {stats['by_mood']}")
    
    print("\n✅ Memory system test complete!")