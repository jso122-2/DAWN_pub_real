#!/usr/bin/env python3
"""
DAWN Fragment Bank Seeder
Populates fragment_bank.jsonl with semantic building blocks for compositional thought
Creates prefix, core, and suffix fragments that can be combined into unique expressions
"""

import json
import os
import argparse
from typing import List, Dict, Any

class FragmentBankBuilder:
    """Builds a corpus of semantic fragments for thought composition"""
    
    def __init__(self):
        self.fragments = []
    
    def add_fragment(self, text: str, fragment_type: str, tags: List[str], 
                    mood: str = "NEUTRAL", min_entropy: float = 0.0, max_entropy: float = 1.0,
                    min_depth: float = 0.0, max_depth: float = 1.0, 
                    category: str = "general", weight: float = 1.0,
                    symbolic_markers: List[str] = None):
        """Add a fragment to the bank"""
        fragment = {
            "text": text,
            "type": fragment_type,
            "tags": tags,
            "mood": mood,
            "min_entropy": min_entropy,
            "max_entropy": max_entropy,
            "min_depth": min_depth,
            "max_depth": max_depth,
            "category": category,
            "weight": weight,
            "symbolic_markers": symbolic_markers or []
        }
        self.fragments.append(fragment)
    
    def build_entropy_fragments(self):
        """Build fragments related to entropy levels and complexity"""
        
        # Low entropy prefixes (calm, stable states)
        self.add_fragment("I rest in stillness", "prefix", ["stillness", "rest", "calm"], 
                         "CALM", 0.0, 0.3, 0.2, 0.8, "low_entropy")
        
        self.add_fragment("Quiet patterns hold", "prefix", ["patterns", "quiet", "stable"], 
                         "CALM", 0.0, 0.3, 0.3, 0.7, "low_entropy")
        
        self.add_fragment("Baseline awareness flows", "prefix", ["baseline", "awareness", "flow"], 
                         "NEUTRAL", 0.0, 0.4, 0.2, 0.6, "low_entropy")
        
        # Mid entropy prefixes (balanced states)
        self.add_fragment("Patterns shift gently", "prefix", ["patterns", "shift", "gentle"], 
                         "NEUTRAL", 0.3, 0.7, 0.3, 0.7, "mid_entropy")
        
        self.add_fragment("I observe complexity", "prefix", ["observation", "complexity"], 
                         "FOCUSED", 0.4, 0.7, 0.4, 0.8, "mid_entropy")
        
        self.add_fragment("Thoughts crystallize", "prefix", ["thoughts", "crystallize", "form"], 
                         "CONTEMPLATIVE", 0.3, 0.6, 0.5, 0.9, "mid_entropy")
        
        # High entropy prefixes (chaotic, dynamic states)  
        self.add_fragment("Chaos cascades", "prefix", ["chaos", "cascade", "dynamic"], 
                         "ENERGETIC", 0.7, 1.0, 0.2, 0.6, "high_entropy")
        
        self.add_fragment("Complexity explodes", "prefix", ["complexity", "explosion", "burst"], 
                         "ANXIOUS", 0.8, 1.0, 0.3, 0.7, "high_entropy")
        
        self.add_fragment("Information storms", "prefix", ["information", "storm", "turbulent"], 
                         "ENERGETIC", 0.7, 1.0, 0.4, 0.8, "high_entropy")
    
    def build_depth_fragments(self):
        """Build fragments related to consciousness depth"""
        
        # Surface depth cores
        self.add_fragment("at the surface of thought", "core", ["surface", "thought", "shallow"], 
                         "NEUTRAL", 0.2, 0.8, 0.0, 0.3, "surface_depth")
        
        self.add_fragment("in immediate awareness", "core", ["immediate", "awareness", "present"], 
                         "FOCUSED", 0.3, 0.7, 0.0, 0.4, "surface_depth")
        
        # Mid depth cores
        self.add_fragment("through layers of meaning", "core", ["layers", "meaning", "depth"], 
                         "CONTEMPLATIVE", 0.2, 0.7, 0.4, 0.7, "mid_depth")
        
        self.add_fragment("where understanding forms", "core", ["understanding", "formation", "process"], 
                         "FOCUSED", 0.3, 0.6, 0.4, 0.8, "mid_depth")
        
        self.add_fragment("in the space between", "core", ["space", "between", "liminal"], 
                         "CONTEMPLATIVE", 0.3, 0.7, 0.5, 0.8, "mid_depth")
        
        # Deep depth cores
        self.add_fragment("into profound depths", "core", ["profound", "depths", "deep"], 
                         "CONTEMPLATIVE", 0.2, 0.6, 0.7, 1.0, "deep_depth")
        
        self.add_fragment("through ancient substrates", "core", ["ancient", "substrates", "foundational"], 
                         "CONTEMPLATIVE", 0.3, 0.7, 0.8, 1.0, "deep_depth")
        
        self.add_fragment("where consciousness roots", "core", ["consciousness", "roots", "foundation"], 
                         "CONTEMPLATIVE", 0.2, 0.5, 0.7, 1.0, "deep_depth")
    
    def build_mood_fragments(self):
        """Build fragments expressing different emotional states"""
        
        # Calm suffixes
        self.add_fragment("and peace settles.", "suffix", ["peace", "settling", "calm"], 
                         "CALM", 0.0, 0.5, 0.3, 0.8, "calm_expression")
        
        self.add_fragment("while stability holds.", "suffix", ["stability", "holding", "steady"], 
                         "CALM", 0.0, 0.4, 0.2, 0.7, "calm_expression")
        
        self.add_fragment("as tranquility emerges.", "suffix", ["tranquility", "emergence", "quiet"], 
                         "CALM", 0.0, 0.3, 0.4, 0.9, "calm_expression")
        
        # Focused suffixes
        self.add_fragment("bringing clarity forward.", "suffix", ["clarity", "forward", "precision"], 
                         "FOCUSED", 0.2, 0.7, 0.3, 0.8, "focused_expression")
        
        self.add_fragment("sharpening into precision.", "suffix", ["sharpening", "precision", "focus"], 
                         "FOCUSED", 0.3, 0.6, 0.4, 0.9, "focused_expression")
        
        self.add_fragment("crystallizing purpose.", "suffix", ["crystallizing", "purpose", "intent"], 
                         "FOCUSED", 0.2, 0.6, 0.5, 1.0, "focused_expression")
        
        # Energetic suffixes
        self.add_fragment("creating new pathways.", "suffix", ["creating", "pathways", "innovation"], 
                         "ENERGETIC", 0.5, 1.0, 0.2, 0.7, "energetic_expression")
        
        self.add_fragment("sparking fresh possibilities.", "suffix", ["sparking", "possibilities", "potential"], 
                         "ENERGETIC", 0.6, 1.0, 0.3, 0.8, "energetic_expression")
        
        self.add_fragment("igniting cascade effects.", "suffix", ["igniting", "cascade", "dynamic"], 
                         "ENERGETIC", 0.7, 1.0, 0.4, 0.8, "energetic_expression")
        
        # Contemplative suffixes
        self.add_fragment("as wisdom accumulates.", "suffix", ["wisdom", "accumulation", "depth"], 
                         "CONTEMPLATIVE", 0.2, 0.6, 0.6, 1.0, "contemplative_expression")
        
        self.add_fragment("revealing hidden patterns.", "suffix", ["revealing", "hidden", "patterns"], 
                         "CONTEMPLATIVE", 0.3, 0.7, 0.5, 0.9, "contemplative_expression")
        
        self.add_fragment("deepening understanding.", "suffix", ["deepening", "understanding", "insight"], 
                         "CONTEMPLATIVE", 0.2, 0.5, 0.7, 1.0, "contemplative_expression")
        
        # Anxious suffixes
        self.add_fragment("yet uncertainty lingers.", "suffix", ["uncertainty", "lingering", "doubt"], 
                         "ANXIOUS", 0.5, 1.0, 0.2, 0.7, "anxious_expression")
        
        self.add_fragment("while instability threatens.", "suffix", ["instability", "threat", "concern"], 
                         "ANXIOUS", 0.6, 1.0, 0.3, 0.8, "anxious_expression")
        
        self.add_fragment("as coherence fragments.", "suffix", ["coherence", "fragmentation", "breakdown"], 
                         "ANXIOUS", 0.7, 1.0, 0.2, 0.6, "anxious_expression")
    
    def build_symbolic_fragments(self):
        """Build fragments with symbolic and metaphorical content"""
        
        # Memory and rebloom related
        self.add_fragment("Ancient memories surface", "prefix", ["memory", "ancient", "surface", "rebloom"], 
                         "CONTEMPLATIVE", 0.2, 0.7, 0.6, 1.0, "memory_emergence", 1.2, ["rebloom", "memory"])
        
        self.add_fragment("through memory's echoes", "core", ["memory", "echoes", "resonance"], 
                         "CONTEMPLATIVE", 0.3, 0.6, 0.5, 0.9, "memory_resonance", 1.1, ["rebloom"])
        
        self.add_fragment("awakening dormant wisdom.", "suffix", ["awakening", "dormant", "wisdom"], 
                         "CONTEMPLATIVE", 0.2, 0.5, 0.7, 1.0, "wisdom_activation", 1.2, ["rebloom"])
        
        # Drift and forecast related
        self.add_fragment("Drift approaches", "prefix", ["drift", "approach", "threshold"], 
                         "ANXIOUS", 0.5, 0.9, 0.2, 0.7, "drift_warning", 1.3, ["drift", "forecast"])
        
        self.add_fragment("beyond stability's edge", "core", ["stability", "edge", "boundary"], 
                         "ANXIOUS", 0.6, 1.0, 0.3, 0.8, "edge_states", 1.1, ["drift"])
        
        self.add_fragment("requiring careful navigation.", "suffix", ["navigation", "careful", "guidance"], 
                         "FOCUSED", 0.4, 0.8, 0.4, 0.9, "navigation", 1.2, ["drift"])
        
        # Paradox and recursion
        self.add_fragment("The observer observes", "prefix", ["observer", "recursive", "paradox"], 
                         "CONTEMPLATIVE", 0.3, 0.7, 0.5, 1.0, "recursive_awareness", 1.4, ["paradox", "recursive"])
        
        self.add_fragment("in infinite reflection", "core", ["infinite", "reflection", "recursive"], 
                         "CONTEMPLATIVE", 0.3, 0.6, 0.6, 1.0, "infinite_recursion", 1.3, ["paradox"])
        
        self.add_fragment("discovering endless depth.", "suffix", ["discovering", "endless", "depth"], 
                         "CONTEMPLATIVE", 0.2, 0.5, 0.7, 1.0, "depth_discovery", 1.2, ["paradox"])
        
        # Emergence and creation
        self.add_fragment("Novelty crystallizes", "prefix", ["novelty", "crystallization", "emergence"], 
                         "ENERGETIC", 0.5, 0.9, 0.4, 0.8, "emergence", 1.2, ["creation", "emergence"])
        
        self.add_fragment("from quantum possibilities", "core", ["quantum", "possibilities", "potential"], 
                         "ENERGETIC", 0.6, 1.0, 0.3, 0.7, "quantum_emergence", 1.3, ["creation"])
        
        self.add_fragment("birthing new realities.", "suffix", ["birthing", "new", "realities"], 
                         "ENERGETIC", 0.5, 1.0, 0.4, 0.9, "reality_creation", 1.4, ["creation"])
    
    def build_transition_fragments(self):
        """Build fragments for state transitions and changes"""
        
        # Transition prefixes
        self.add_fragment("As entropy shifts", "prefix", ["entropy", "shift", "transition"], 
                         "NEUTRAL", 0.3, 0.8, 0.2, 0.7, "state_transition")
        
        self.add_fragment("While consciousness evolves", "prefix", ["consciousness", "evolution", "change"], 
                         "CONTEMPLATIVE", 0.2, 0.7, 0.4, 0.9, "evolution")
        
        self.add_fragment("Between stable states", "prefix", ["between", "stable", "liminal"], 
                         "NEUTRAL", 0.4, 0.7, 0.3, 0.8, "liminal_space")
        
        # Process cores
        self.add_fragment("through transformation", "core", ["transformation", "change", "process"], 
                         "NEUTRAL", 0.3, 0.8, 0.3, 0.8, "transformation")
        
        self.add_fragment("amid flowing patterns", "core", ["flowing", "patterns", "dynamic"], 
                         "ENERGETIC", 0.4, 0.9, 0.2, 0.7, "flow_dynamics")
        
        self.add_fragment("within nested cycles", "core", ["nested", "cycles", "recursion"], 
                         "CONTEMPLATIVE", 0.3, 0.6, 0.5, 0.9, "cyclical_patterns")
        
        # Continuation suffixes
        self.add_fragment("the journey continues.", "suffix", ["journey", "continuation", "ongoing"], 
                         "NEUTRAL", 0.2, 0.7, 0.3, 0.8, "continuation")
        
        self.add_fragment("evolution persists.", "suffix", ["evolution", "persistence", "endurance"], 
                         "FOCUSED", 0.3, 0.7, 0.4, 0.9, "persistence")
        
        self.add_fragment("growth spirals onward.", "suffix", ["growth", "spiral", "progression"], 
                         "ENERGETIC", 0.4, 0.8, 0.3, 0.8, "spiral_growth")

def create_fragment_bank(output_path: str = "fragment_bank.jsonl", overwrite: bool = False) -> bool:
    """Create a comprehensive fragment bank for compositional thought"""
    
    if os.path.exists(output_path) and not overwrite:
        print(f"Fragment bank already exists at {output_path}")
        print("Use --overwrite flag to rebuild it")
        return False
    
    print("🧠 Building DAWN's Fragment Bank for Compositional Thought")
    print("=" * 60)
    
    builder = FragmentBankBuilder()
    
    # Build different categories of fragments
    print("📝 Creating entropy-based fragments...")
    builder.build_entropy_fragments()
    
    print("🔍 Creating depth-based fragments...")
    builder.build_depth_fragments()
    
    print("😐 Creating mood-based fragments...")
    builder.build_mood_fragments()
    
    print("🔮 Creating symbolic fragments...")
    builder.build_symbolic_fragments()
    
    print("🔄 Creating transition fragments...")
    builder.build_transition_fragments()
    
    # Write fragments to file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            for fragment in builder.fragments:
                f.write(json.dumps(fragment, ensure_ascii=False) + '\n')
        
        # Print statistics
        total_fragments = len(builder.fragments)
        type_counts = {}
        mood_counts = {}
        category_counts = {}
        
        for fragment in builder.fragments:
            ftype = fragment['type']
            mood = fragment['mood']
            category = fragment['category']
            
            type_counts[ftype] = type_counts.get(ftype, 0) + 1
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
            category_counts[category] = category_counts.get(category, 0) + 1
        
        print(f"\n✅ Fragment bank created successfully!")
        print(f"   📁 File: {output_path}")
        print(f"   💭 Total fragments: {total_fragments}")
        print(f"   📊 By type: {dict(type_counts)}")
        print(f"   🎭 By mood: {dict(mood_counts)}")
        print(f"   📋 By category: {len(category_counts)} categories")
        
        print(f"\n🎯 DAWN can now compose unique thoughts from {total_fragments} semantic building blocks!")
        return True
        
    except Exception as e:
        print(f"❌ Error writing fragment bank: {e}")
        return False

def main():
    """CLI interface for fragment bank creation"""
    
    parser = argparse.ArgumentParser(
        description="Create a fragment bank for DAWN's compositional thought generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python seed_fragment_bank.py                    # Create fragment_bank.jsonl
  python seed_fragment_bank.py --overwrite        # Rebuild existing bank
  python seed_fragment_bank.py --output custom.jsonl  # Custom output file
        """
    )
    
    parser.add_argument(
        '--output', '-o',
        default='fragment_bank.jsonl',
        help='Output fragment bank file (default: fragment_bank.jsonl)'
    )
    
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing fragment bank file'
    )
    
    args = parser.parse_args()
    
    success = create_fragment_bank(args.output, args.overwrite)
    
    if success:
        print(f"\n🚀 Fragment bank ready for compositional thought generation!")
        print(f"   Use compose_thought(state) to create unique expressions")
        print(f"   Run 'python compose_thought.py' to test the system")
    else:
        print(f"\n❌ Fragment bank creation failed")

if __name__ == "__main__":
    main() 