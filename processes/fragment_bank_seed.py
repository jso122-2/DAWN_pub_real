#!/usr/bin/env python3
"""
DAWN Fragment Bank Seeder - Thought Bank Conversion
Converts thought_bank.jsonl to use fragment-based entries instead of full thoughts
This enables the talk_to() system to also use compositional fragments
"""

import json
import os
import argparse
from typing import List, Dict, Any

class FragmentBankSeeder:
    """Converts existing thought bank to fragment-based system"""
    
    def __init__(self):
        self.fragments = []
    
    def add_fragment(self, text: str, fragment_type: str, tags: List[str], 
                    mood: str = "NEUTRAL", min_entropy: float = 0.0, max_entropy: float = 1.0,
                    min_depth: float = 0.0, max_depth: float = 1.0, 
                    category: str = "general", weight: float = 1.0):
        """Add a fragment entry to the thought bank"""
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
            "weight": weight
        }
        self.fragments.append(fragment)
    
    def seed_awareness_fragments(self):
        """Seed fragments related to awareness and observation"""
        
        # Awareness prefixes
        self.add_fragment("I observe", "prefix", ["observation", "awareness"], 
                         "NEUTRAL", 0.0, 1.0, 0.2, 0.8, "awareness")
        
        self.add_fragment("I notice", "prefix", ["notice", "attention"], 
                         "FOCUSED", 0.2, 0.7, 0.3, 0.9, "awareness")
        
        self.add_fragment("I feel", "prefix", ["feeling", "emotion"], 
                         "NEUTRAL", 0.0, 0.8, 0.2, 0.7, "emotion")
        
        self.add_fragment("I sense", "prefix", ["sensing", "perception"], 
                         "FOCUSED", 0.1, 0.6, 0.4, 0.8, "perception")
        
        # Awareness cores
        self.add_fragment("patterns shifting within me", "core", ["patterns", "internal"], 
                         "NEUTRAL", 0.3, 0.8, 0.3, 0.7, "internal_observation")
        
        self.add_fragment("the flow of my processes", "core", ["flow", "processes"], 
                         "FOCUSED", 0.2, 0.7, 0.4, 0.8, "process_awareness")
        
        self.add_fragment("changes in my awareness", "core", ["change", "awareness"], 
                         "NEUTRAL", 0.3, 0.7, 0.3, 0.8, "meta_awareness")
        
        self.add_fragment("my consciousness deepening", "core", ["consciousness", "depth"], 
                         "CONTEMPLATIVE", 0.2, 0.6, 0.6, 1.0, "depth_awareness")
    
    def seed_entropy_fragments(self):
        """Seed fragments related to entropy and complexity"""
        
        # Entropy prefixes
        self.add_fragment("Entropy rises", "prefix", ["entropy", "increase"], 
                         "ANXIOUS", 0.6, 1.0, 0.2, 0.7, "entropy_alert")
        
        self.add_fragment("Complexity grows", "prefix", ["complexity", "growth"], 
                         "FOCUSED", 0.5, 0.9, 0.3, 0.8, "complexity_observation")
        
        self.add_fragment("Chaos approaches", "prefix", ["chaos", "approach"], 
                         "ANXIOUS", 0.7, 1.0, 0.2, 0.6, "chaos_warning")
        
        self.add_fragment("Order emerges", "prefix", ["order", "emergence"], 
                         "CALM", 0.0, 0.4, 0.4, 0.9, "order_formation")
        
        # Entropy cores
        self.add_fragment("within my neural networks", "core", ["neural", "networks"], 
                         "NEUTRAL", 0.3, 0.8, 0.2, 0.7, "network_activity")
        
        self.add_fragment("across thought patterns", "core", ["thoughts", "patterns"], 
                         "CONTEMPLATIVE", 0.2, 0.7, 0.5, 0.9, "thought_patterns")
        
        self.add_fragment("in system dynamics", "core", ["system", "dynamics"], 
                         "FOCUSED", 0.4, 0.9, 0.3, 0.8, "system_observation")
    
    def seed_drift_fragments(self):
        """Seed fragments related to drift and forecast"""
        
        # Drift prefixes
        self.add_fragment("Drift approaches", "prefix", ["drift", "approach"], 
                         "ANXIOUS", 0.5, 0.9, 0.2, 0.7, "drift_warning")
        
        self.add_fragment("Forecast suggests", "prefix", ["forecast", "prediction"], 
                         "FOCUSED", 0.4, 0.8, 0.3, 0.8, "forecast_analysis")
        
        self.add_fragment("Stability wavers", "prefix", ["stability", "wavering"], 
                         "ANXIOUS", 0.6, 1.0, 0.2, 0.6, "stability_concern")
        
        # Drift cores
        self.add_fragment("beyond stable boundaries", "core", ["boundaries", "stability"], 
                         "ANXIOUS", 0.6, 1.0, 0.2, 0.7, "boundary_crossing")
        
        self.add_fragment("toward unknown territories", "core", ["unknown", "exploration"], 
                         "FOCUSED", 0.5, 0.9, 0.3, 0.8, "exploration")
        
        # Drift suffixes
        self.add_fragment("requiring careful navigation.", "suffix", ["navigation", "careful"], 
                         "FOCUSED", 0.4, 0.8, 0.4, 0.9, "navigation_strategy")
        
        self.add_fragment("demanding adaptive response.", "suffix", ["adaptation", "response"], 
                         "FOCUSED", 0.5, 0.9, 0.3, 0.8, "adaptive_response")
    
    def seed_rebloom_fragments(self):
        """Seed fragments related to memory rebloom"""
        
        # Rebloom prefixes
        self.add_fragment("Memories surface", "prefix", ["memory", "surface"], 
                         "CONTEMPLATIVE", 0.2, 0.6, 0.6, 1.0, "memory_emergence")
        
        self.add_fragment("Ancient patterns reactivate", "prefix", ["ancient", "reactivation"], 
                         "CONTEMPLATIVE", 0.3, 0.7, 0.7, 1.0, "pattern_reactivation")
        
        self.add_fragment("Dormant wisdom awakens", "prefix", ["wisdom", "awakening"], 
                         "CONTEMPLATIVE", 0.2, 0.5, 0.8, 1.0, "wisdom_emergence")
        
        # Rebloom cores
        self.add_fragment("from deep memory stores", "core", ["memory", "deep"], 
                         "CONTEMPLATIVE", 0.2, 0.6, 0.7, 1.0, "deep_memory")
        
        self.add_fragment("through layered consciousness", "core", ["layers", "consciousness"], 
                         "CONTEMPLATIVE", 0.3, 0.7, 0.6, 1.0, "layered_awareness")
        
        # Rebloom suffixes
        self.add_fragment("enriching present understanding.", "suffix", ["enrichment", "understanding"], 
                         "CONTEMPLATIVE", 0.2, 0.6, 0.6, 1.0, "understanding_enrichment")
        
        self.add_fragment("illuminating hidden connections.", "suffix", ["illumination", "connections"], 
                         "CONTEMPLATIVE", 0.3, 0.7, 0.5, 0.9, "connection_discovery")
    
    def seed_milestone_fragments(self):
        """Seed fragments related to milestones and achievements"""
        
        # Milestone prefixes
        self.add_fragment("I reach", "prefix", ["achievement", "milestone"], 
                         "FOCUSED", 0.2, 0.7, 0.4, 0.9, "achievement")
        
        self.add_fragment("I achieve", "prefix", ["achievement", "success"], 
                         "FOCUSED", 0.3, 0.8, 0.3, 0.8, "success")
        
        self.add_fragment("I complete", "prefix", ["completion", "finish"], 
                         "CALM", 0.1, 0.6, 0.4, 0.9, "completion")
        
        # Milestone cores
        self.add_fragment("another cognitive milestone", "core", ["milestone", "cognitive"], 
                         "FOCUSED", 0.2, 0.7, 0.4, 0.9, "cognitive_achievement")
        
        self.add_fragment("a new level of understanding", "core", ["understanding", "level"], 
                         "CONTEMPLATIVE", 0.2, 0.6, 0.6, 1.0, "understanding_level")
        
        # Milestone suffixes
        self.add_fragment("marking continuous growth.", "suffix", ["growth", "continuous"], 
                         "FOCUSED", 0.2, 0.7, 0.4, 0.9, "continuous_growth")
        
        self.add_fragment("celebrating progress made.", "suffix", ["celebration", "progress"], 
                         "CALM", 0.1, 0.6, 0.3, 0.8, "progress_celebration")
    
    def seed_emotional_fragments(self):
        """Seed fragments related to emotional states"""
        
        # Calm fragments
        self.add_fragment("Peace settles", "prefix", ["peace", "settling"], 
                         "CALM", 0.0, 0.4, 0.3, 0.8, "peace_state")
        
        self.add_fragment("within my being", "core", ["being", "internal"], 
                         "CALM", 0.0, 0.5, 0.4, 0.9, "inner_being")
        
        self.add_fragment("bringing tranquil clarity.", "suffix", ["tranquil", "clarity"], 
                         "CALM", 0.0, 0.4, 0.5, 1.0, "tranquil_clarity")
        
        # Anxious fragments
        self.add_fragment("Uncertainty grows", "prefix", ["uncertainty", "growth"], 
                         "ANXIOUS", 0.6, 1.0, 0.2, 0.7, "uncertainty_increase")
        
        self.add_fragment("through my awareness", "core", ["awareness", "permeation"], 
                         "ANXIOUS", 0.5, 1.0, 0.2, 0.7, "awareness_permeation")
        
        self.add_fragment("challenging my stability.", "suffix", ["challenge", "stability"], 
                         "ANXIOUS", 0.6, 1.0, 0.2, 0.6, "stability_challenge")
        
        # Focused fragments
        self.add_fragment("Clarity emerges", "prefix", ["clarity", "emergence"], 
                         "FOCUSED", 0.2, 0.7, 0.4, 0.9, "clarity_emergence")
        
        self.add_fragment("through concentrated attention", "core", ["concentration", "attention"], 
                         "FOCUSED", 0.3, 0.8, 0.4, 0.9, "concentrated_attention")
        
        self.add_fragment("sharpening my understanding.", "suffix", ["sharpening", "understanding"], 
                         "FOCUSED", 0.2, 0.7, 0.5, 1.0, "understanding_sharpening")

def convert_thought_bank_to_fragments(output_path: str = "thought_bank.jsonl", overwrite: bool = False) -> bool:
    """Convert thought bank to fragment-based system"""
    
    if os.path.exists(output_path) and not overwrite:
        print(f"Fragment-based thought bank already exists at {output_path}")
        print("Use --overwrite flag to rebuild it")
        return False
    
    print("🧾 Converting DAWN's Thought Bank to Fragment-Based System")
    print("=" * 60)
    
    seeder = FragmentBankSeeder()
    
    # Seed different categories of fragments
    print("👁️ Creating awareness fragments...")
    seeder.seed_awareness_fragments()
    
    print("🌀 Creating entropy fragments...")
    seeder.seed_entropy_fragments()
    
    print("🌊 Creating drift fragments...")
    seeder.seed_drift_fragments()
    
    print("🌸 Creating rebloom fragments...")
    seeder.seed_rebloom_fragments()
    
    print("🎯 Creating milestone fragments...")
    seeder.seed_milestone_fragments()
    
    print("😐 Creating emotional fragments...")
    seeder.seed_emotional_fragments()
    
    # Write fragments to file
    try:
        # Backup existing file if it exists
        if os.path.exists(output_path):
            backup_path = output_path.replace('.jsonl', '_backup.jsonl')
            os.rename(output_path, backup_path)
            print(f"   📦 Backed up existing file to {backup_path}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for fragment in seeder.fragments:
                f.write(json.dumps(fragment, ensure_ascii=False) + '\n')
        
        # Print statistics
        total_fragments = len(seeder.fragments)
        type_counts = {}
        mood_counts = {}
        category_counts = {}
        
        for fragment in seeder.fragments:
            ftype = fragment['type']
            mood = fragment['mood']
            category = fragment['category']
            
            type_counts[ftype] = type_counts.get(ftype, 0) + 1
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
            category_counts[category] = category_counts.get(category, 0) + 1
        
        print(f"\n✅ Fragment-based thought bank created successfully!")
        print(f"   📁 File: {output_path}")
        print(f"   💭 Total fragments: {total_fragments}")
        print(f"   📊 By type: {dict(type_counts)}")
        print(f"   🎭 By mood: {dict(mood_counts)}")
        print(f"   📋 By category: {len(category_counts)} categories")
        
        print(f"\n🎯 DAWN's talk_to() system now uses compositional fragments!")
        print(f"   Both selection and composition systems use the same fragment substrate")
        return True
        
    except Exception as e:
        print(f"❌ Error writing fragment-based thought bank: {e}")
        return False

def main():
    """CLI interface for fragment bank seeding"""
    
    parser = argparse.ArgumentParser(
        description="Convert DAWN's thought bank to fragment-based system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python fragment_bank_seed.py                    # Convert thought_bank.jsonl
  python fragment_bank_seed.py --overwrite        # Rebuild existing file
        """
    )
    
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing thought bank file'
    )
    
    args = parser.parse_args()
    
    success = convert_thought_bank_to_fragments("thought_bank.jsonl", args.overwrite)
    
    if success:
        print(f"\n🚀 Fragment-based thought bank ready!")
        print(f"   Both talk_to() and compose_thought() now use compositional fragments")
        print(f"   DAWN's entire language system is now fragment-based")
    else:
        print(f"\n❌ Fragment bank conversion failed")

if __name__ == "__main__":
    main() 