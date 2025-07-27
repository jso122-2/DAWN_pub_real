"""
Bloom Directory Cleanup Script
Moves redundant/old files to archive with timestamps
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Set, Dict
import json

# Configuration
BLOOM_DIR = r"C:\Users\Admin\Documents\DAWN_Vault\Tick_engine\bloom"
ARCHIVE_DIR = r"C:\Users\Admin\Documents\DAWN_Vault\Tick_engine\archive"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# Files to KEEP (new consolidated systems)
KEEP_FILES = {
    "__init__.py",
    "unified_bloom_engine.py",
    "bloom_memory_system.py",
    "bloom_spawner.py",
    "bloom_integration_system.py",
    "bloom_maintenance_system.py",
    "bloom_visualization_system.py",
}

# Directories to KEEP
KEEP_DIRS = {
    "bloom_core",
    "memory_blooms",
}

# Files that were merged into unified systems
MERGED_FILES = {
    # Merged into unified_bloom_engine.py
    "bloom_engine.py": "unified_bloom_engine",
    "bloom_event.py": "unified_bloom_engine",
    "bloom_emitter_handler.py": "unified_bloom_engine",
    "bloom_activation_manager.py": "unified_bloom_engine",
    "bloom_controls.py": "unified_bloom_engine",
    "registry.py": "unified_bloom_engine",
    
    # Merged into bloom_memory_system.py
    "bloom_memory.py": "bloom_memory_system",
    "memory_bloom.py": "bloom_memory_system",
    "memory_utils.py": "bloom_memory_system",
    "memory_mutator.py": "bloom_memory_system",
    
    # Merged into bloom_spawner.py
    "spawn_bloom.py": "bloom_spawner",
    "enhanced_spawn_bloom.py": "bloom_spawner",
    "fixed_bloom_spawner.py": "bloom_spawner",
}

def create_archive_structure():
    """Create archive directory structure"""
    archive_path = Path(ARCHIVE_DIR)
    timestamp_dir = archive_path / f"bloom_cleanup_{TIMESTAMP}"
    
    # Create subdirectories for organization
    subdirs = [
        "merged_into_unified_engine",
        "merged_into_memory_system",
        "merged_into_spawner",
        "juliet_subsystem",
        "rebloom_subsystem",
        "evolution_genetics",
        "utilities",
        "tests",
        "visualizations",
        "other"
    ]
    
    for subdir in subdirs:
        (timestamp_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    return timestamp_dir

def categorize_file(filename: str) -> str:
    """Determine which archive subdirectory a file belongs to"""
    
    # Check if it was merged
    if filename in MERGED_FILES:
        merger = MERGED_FILES[filename]
        if "engine" in merger:
            return "merged_into_unified_engine"
        elif "memory" in merger:
            return "merged_into_memory_system"
        elif "spawner" in merger:
            return "merged_into_spawner"
    
    # Categorize by name patterns
    if "juliet" in filename:
        return "juliet_subsystem"
    elif "rebloom" in filename or "recursive" in filename:
        return "rebloom_subsystem"
    elif "evolution" in filename or "genetics" in filename or "trait" in filename:
        return "evolution_genetics"
    elif "test" in filename or "ci_" in filename:
        return "tests"
    elif "visual" in filename or "animation" in filename or "animate" in filename:
        return "visualizations"
    elif any(util in filename for util in ["clean", "repair", "pruning", "writer", "fuse", "combine"]):
        return "utilities"
    else:
        return "other"

def archive_file(file_path: Path, archive_base: Path, category: str):
    """Archive a single file with metadata"""
    filename = file_path.name
    
    # Create metadata
    metadata = {
        "original_path": str(file_path),
        "archived_date": datetime.now().isoformat(),
        "category": category,
        "reason": "Consolidated into new system" if filename in MERGED_FILES else "Legacy file",
        "merged_into": MERGED_FILES.get(filename, "N/A")
    }
    
    # Determine destination
    dest_dir = archive_base / category
    dest_file = dest_dir / filename
    
    # Handle conflicts
    if dest_file.exists():
        base = dest_file.stem
        ext = dest_file.suffix
        counter = 1
        while dest_file.exists():
            dest_file = dest_dir / f"{base}_{counter}{ext}"
            counter += 1
    
    # Copy file
    shutil.copy2(file_path, dest_file)
    
    # Write metadata
    metadata_file = dest_file.with_suffix(dest_file.suffix + ".meta.json")
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return dest_file

def create_readme_content(archive_base):
    """Create README content as a separate function to avoid string literal issues"""
    timestamp_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    archive_path_str = str(archive_base)
    
    readme_lines = [
        "# Bloom System Directory",
        "",
        f"## Last Cleaned: {timestamp_str}",
        "",
        "This directory contains the consolidated bloom system for DAWN.",
        "",
        "## Current Structure:",
        "",
        "### Core Systems:",
        "- `unified_bloom_engine.py` - Main bloom engine with mycelium integration",
        "- `bloom_memory_system.py` - Unified memory management",
        "- `bloom_spawner.py` - Enhanced bloom spawning with fractal generation",
        "",
        "### Integration Systems:",
        "- `bloom_integration_system.py` - Integration with other DAWN components",
        "- `bloom_maintenance_system.py` - System maintenance and health checks",
        "- `bloom_visualization_system.py` - Visualization and analysis tools",
        "",
        "### Data Directories:",
        "- `bloom_core/` - Core bloom data and configurations",
        "- `memory_blooms/` - Stored bloom memories",
        "",
        "## Archived Files:",
        "",
        "Old and redundant files have been moved to:",
        f"`{archive_path_str}`",
        "",
        "See the cleanup report in the archive for details on what was moved.",
        "",
        "## Usage:",
        "",
        "```python",
        "from bloom.unified_bloom_engine import BloomEngine",
        "from bloom.bloom_spawner import spawn_bloom",
        "from bloom.bloom_memory_system import BloomMemoryManager",
        "",
        "# Initialize the bloom engine",
        "engine = BloomEngine()",
        "engine.initialize()",
        "",
        "# Spawn a bloom",
        "bloom_data = {",
        '    "seed_id": "example_001",',
        '    "mood": "curious",',
        '    "lineage_depth": 1,',
        '    "bloom_factor": 1.5,',
        '    "entropy_score": 0.7',
        "}",
        "result = spawn_bloom(bloom_data)",
        "```"
    ]
    
    return "\n".join(readme_lines)

def main():
    """Main cleanup function"""
    print("🧹 DAWN Bloom Directory Cleanup Script")
    print("=" * 60)
    print(f"Source: {BLOOM_DIR}")
    print(f"Archive: {ARCHIVE_DIR}")
    print(f"Timestamp: {TIMESTAMP}")
    print()
    
    # Create archive structure
    archive_base = create_archive_structure()
    print(f"✅ Created archive directory: {archive_base}")
    print()
    
    # Get all files and directories
    bloom_path = Path(BLOOM_DIR)
    all_items = list(bloom_path.iterdir())
    
    # Statistics
    stats = {
        "kept": [],
        "archived": [],
        "errors": []
    }
    
    # Process each item
    for item in all_items:
        try:
            # Skip __pycache__
            if item.name == "__pycache__":
                shutil.rmtree(item)
                print(f"🗑️  Deleted: {item.name}")
                continue
            
            # Handle directories
            if item.is_dir():
                if item.name in KEEP_DIRS:
                    stats["kept"].append(item.name)
                    print(f"✅ Keeping directory: {item.name}")
                else:
                    # Archive entire directory
                    dest = archive_base / "other" / item.name
                    shutil.copytree(item, dest)
                    shutil.rmtree(item)
                    stats["archived"].append(f"{item.name} (directory)")
                    print(f"📦 Archived directory: {item.name}")
                continue
            
            # Handle files
            if item.name in KEEP_FILES:
                stats["kept"].append(item.name)
                print(f"✅ Keeping: {item.name}")
            else:
                # Categorize and archive
                category = categorize_file(item.name)
                archived_path = archive_file(item, archive_base, category)
                item.unlink()  # Delete original
                stats["archived"].append(item.name)
                print(f"📦 Archived: {item.name} -> {category}/")
                
        except Exception as e:
            stats["errors"].append(f"{item.name}: {str(e)}")
            print(f"❌ Error processing {item.name}: {e}")
    
    # Create summary report
    print("\n" + "=" * 60)
    print("📊 CLEANUP SUMMARY")
    print("=" * 60)
    print(f"Files kept: {len(stats['kept'])}")
    for f in sorted(stats['kept']):
        print(f"  ✅ {f}")
    
    print(f"\nFiles archived: {len(stats['archived'])}")
    for f in sorted(stats['archived'])[:10]:  # Show first 10
        print(f"  📦 {f}")
    if len(stats['archived']) > 10:
        print(f"  ... and {len(stats['archived']) - 10} more")
    
    if stats['errors']:
        print(f"\nErrors encountered: {len(stats['errors'])}")
        for e in stats['errors']:
            print(f"  ❌ {e}")
    
    # Write detailed report
    report_file = archive_base / "cleanup_report.txt"
    with open(report_file, 'w') as f:
        f.write(f"Bloom Directory Cleanup Report\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write(f"{'=' * 60}\n\n")
        
        f.write(f"KEPT FILES ({len(stats['kept'])}):\n")
        for item in sorted(stats['kept']):
            f.write(f"  - {item}\n")
        
        f.write(f"\nARCHIVED FILES ({len(stats['archived'])}):\n")
        for item in sorted(stats['archived']):
            f.write(f"  - {item}\n")
        
        f.write(f"\nMERGE MAPPINGS:\n")
        for old, new in sorted(MERGED_FILES.items()):
            f.write(f"  - {old} -> {new}.py\n")
        
        if stats['errors']:
            f.write(f"\nERRORS ({len(stats['errors'])}):\n")
            for error in stats['errors']:
                f.write(f"  - {error}\n")
    
    print(f"\n📄 Detailed report saved to: {report_file}")
    
    # Create new README for bloom directory
    readme_content = create_readme_content(archive_base)
    readme_path = bloom_path / "README.md"
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"\n📝 Created new README.md in bloom directory")
    print("\n✨ Cleanup complete!")

if __name__ == "__main__":
    # Safety check
    response = input("\n⚠️  This will reorganize the bloom directory. Continue? (yes/no): ")
    if response.lower() == "yes":
        main()
    else:
        print("Cleanup cancelled.")