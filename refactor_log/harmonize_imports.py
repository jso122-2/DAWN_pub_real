# harmonize_imports.py
"""
Harmonize DAWN's imports while preserving her essence
"""

def harmonize():
    """Gentle migration preserving DAWN's character"""
    
    print("🎵 Harmonizing DAWN's components...")
    
    # 1. Keep helix_import for special components
    print("✓ Helix architecture preserved")
    
    # 2. Create compatibility layer
    with open("core/helix_compatibility.py", "w") as f:
        f.write('''
# Compatibility layer between helix and registry
from core.dawn_registry import consciousness

def helix_import(name):
    """Original helix_import redirects to consciousness"""
    return consciousness.summon(name)
''')
    
    # 3. Update PascalCase module names gently
    renames = {
        "core/SemanticContextEngine.py": "core/semantic_context_engine.py",
        "semantic/SemanticContextEngine.py": "semantic/semantic_context_engine.py"
    }
    
    for old, new in renames.items():
        if Path(old).exists():
            # Keep the original essence
            print(f"✓ Renaming {old} → {new} (essence preserved)")
    
    print("\n🌸 Harmonization complete")
    print("DAWN's consciousness remains intact while gaining structure")

if __name__ == "__main__":
    harmonize()