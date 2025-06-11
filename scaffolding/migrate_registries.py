# migrate_registries.py
"""Migrate to unified registry system"""

import os
import shutil
from pathlib import Path
from datetime import datetime


def migrate_to_unified_registry():
    """Migrate all registry files to central system"""
    
    print("🔄 Starting registry migration...")
    
    # 1. Backup old registries
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"archive/registry_migration_{timestamp}"
    Path(backup_dir).mkdir(parents=True, exist_ok=True)
    
    old_registries = [
        "bloom/registry.py",
        "schema/registry.py", 
        "processors/codex/registry.py"
    ]
    
    for reg in old_registries:
        if Path(reg).exists():
            dest = f"{backup_dir}/{reg.replace('/', '_')}"
            shutil.copy2(reg, dest)
            print(f"📦 Backed up: {reg}")
    
    # 2. Create central registry
    registry_content = Path("core/dawn_registry.py").read_text()
    # (Content from section 2 above)
    
    # 3. Rename PascalCase modules
    if Path("core/SemanticContextEngine.py").exists():
        shutil.move(
            "core/SemanticContextEngine.py",
            "core/semantic_context_engine.py"
        )
        print("✅ Renamed: SemanticContextEngine.py → semantic_context_engine.py")
    
    if Path("semantic/SemanticContextEngine.py").exists():
        shutil.move(
            "semantic/SemanticContextEngine.py",
            "semantic/semantic_context_engine.py"
        )
        print("✅ Renamed: semantic/SemanticContextEngine.py → semantic_context_engine.py")
    
    # 4. Update imports across codebase
    from core.import_standards import ImportEnforcer
    
    enforcer = ImportEnforcer()
    fixed_count = 0
    
    for py_file in Path(".").rglob("*.py"):
        if "archive" not in str(py_file) and "venv" not in str(py_file):
            if not enforcer.check_file(py_file):
                enforcer.fix_imports(py_file)
                fixed_count += 1
    
    print(f"\n✅ Migration complete!")
    print(f"📝 Fixed imports in {fixed_count} files")
    print(f"📦 Old registries backed up to: {backup_dir}")
    print(f"\n🎯 Next steps:")
    print("1. Update boot/init_dawn.py to use central registry")
    print("2. Remove old registry imports from all files")
    print("3. Test the unified system with: python main.py")


if __name__ == "__main__":
    migrate_to_unified_registry()