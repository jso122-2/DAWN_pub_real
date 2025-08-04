#!/usr/bin/env python3
"""
Home Directory Cleanup Script
============================

Organizes files in the home directory into appropriate subdirectories:
- launchers/ - All launch scripts
- visual/ - Visualization related files
- conversation/ - Conversation system files
- demos/ - Demo and test files
- docs/ - Documentation files
- core/ - Core system files
- integration/ - Integration files
- backups/ - Backup files

Then updates all relevant imports to reflect the new structure.
"""

import os
import shutil
import re
import glob
from pathlib import Path

def create_directories():
    """Create necessary directories for organization"""
    directories = [
        'launchers',
        'visual',
        'conversation', 
        'demos',
        'docs',
        'core',
        'integration',
        'backups',
        'scripts',
        'config'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def categorize_files():
    """Categorize files for organization"""
    
    # Launcher files
    launcher_files = [
        'launch_dawn_beautiful.py',
        'launch_dawn_local.py', 
        'launch_dawn_complete.py',
        'launch_dawn_with_visuals.py',
        'launch_visual_gui.py',
        'launch_dawn.py',
        'launch_separated.py',
        'dawn_launcher.py',
        'quick_start.py'
    ]
    
    # Visual files
    visual_files = [
        'dawn_visual_beautiful.py',
        'dawn_visual_local.py',
        'dawn_visual_gui.py',
        'visual_api_server.py',
        'visual_integration.py',
        'gui_visualization_bridge.py',
        'visual_trigger.py',
        'enhanced_visual_engine.py',
        'visual_engine.py',
        'consciousness_visualization_service.py',
        'demo_visual_integration.py'
    ]
    
    # Conversation files
    conversation_files = [
        'cli_dawn_conversation.py',
        'conversation_input_enhanced.py',
        'conversation_response_enhanced.py',
        'simple_conversation.py',
        'standalone_conversation.py',
        'demo_conversation.py',
        'test_conversation.py',
        'conversation_input.py',
        'conversation_response.py',
        'conversation_response_backup_20250727_205903.py',
        'conversation_requirements.txt',
        'philosophical_conversation_demo.py',
        'integrate_philosophical_conversation.py',
        'test_enhanced_conversation_demo.py'
    ]
    
    # Demo files
    demo_files = [
        'demo_reset.py',
        'complete_integration_demo.py',
        'voice_symbolic_integration.py',
        'tick_integration.py'
    ]
    
    # Documentation files
    doc_files = [
        'ENHANCED_CONVERSATION_SYSTEM_SUMMARY.md',
        'CONVERSATION_SYSTEM_COMPLETE.md',
        'CONVERSATION_README.md',
        'CONSCIOUSNESS_VISUALIZATION_INTEGRATION_COMPLETE.md',
        'DAWN_VISUALIZATION_AUDIT_REPORT.md',
        'DAWN_UNIFIED_INTEGRATION_COMPLETE.md',
        'VISUAL_INTEGRATION_SUMMARY.md',
        'DAWN_UNIFIED_RUNNER_README.md',
        'SEMANTIC_TIME_MACHINE_COMPLETE.md',
        'EXPRESSIVE_COGNITION_LAYER_COMPLETE.md',
        'COMPLETE_SYMBOLIC_INTEGRATION_SUCCESS.md'
    ]
    
    # Core system files
    core_files = [
        'dawn_runner.py',
        'unified_backend.py',
        'semantic_anchor.py',
        'cognitive_gravity.py',
        'dawn_constitution.py',
        'shelter_vectors.py',
        'persephone_threads.py',
        'volcanic_dynamics.py',
        'soft_edges.py',
        'mr_wolf.py',
        'tracer_ecosystem.py',
        'fractal_memory.py',
        'platonic_pigment.py',
        'mycelial_network.py',
        'schema_health_monitor.py',
        'cognitive_formulas.py',
        'SymbolicTraceComposer.py',
        'voice_mood_modulation.py'
    ]
    
    # Integration files
    integration_files = [
        'fix_dawn_system.py',
        'test_dawn_connection.py'
    ]
    
    # Script files
    script_files = [
        'launch_config.yaml'
    ]
    
    # Backup files
    backup_files = [
        'conversation_response_backup_20250727_205903.py'
    ]
    
    return {
        'launchers': launcher_files,
        'visual': visual_files,
        'conversation': conversation_files,
        'demos': demo_files,
        'docs': doc_files,
        'core': core_files,
        'integration': integration_files,
        'scripts': script_files,
        'backups': backup_files
    }

def move_files(categories):
    """Move files to their appropriate directories"""
    moved_files = {}
    
    for directory, files in categories.items():
        moved_files[directory] = []
        for file in files:
            if os.path.exists(file):
                try:
                    destination = os.path.join(directory, file)
                    shutil.move(file, destination)
                    moved_files[directory].append(file)
                    print(f"✅ Moved {file} -> {directory}/")
                except Exception as e:
                    print(f"❌ Failed to move {file}: {e}")
            else:
                print(f"⚠️  File not found: {file}")
    
    return moved_files

def update_imports_in_file(file_path, moved_files):
    """Update imports in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update imports for moved files
        for directory, files in moved_files.items():
            for file in files:
                # Remove .py extension for import statements
                module_name = file.replace('.py', '')
                
                # Update various import patterns
                patterns = [
                    (f'import {module_name}', f'from {directory} import {module_name}'),
                    (f'from {module_name} import', f'from {directory}.{module_name} import'),
                    (f'import {module_name} as', f'from {directory} import {module_name} as'),
                ]
                
                for old_pattern, new_pattern in patterns:
                    content = content.replace(old_pattern, new_pattern)
        
        # Update relative imports
        content = re.sub(r'from \.([a-zA-Z_][a-zA-Z0-9_]*) import', r'from ..\1 import', content)
        content = re.sub(r'from \.\.([a-zA-Z_][a-zA-Z0-9_]*) import', r'from ...\1 import', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated imports in {file_path}")
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def update_all_imports(moved_files):
    """Update imports in all Python files"""
    print("\n🔄 Updating imports...")
    
    # Find all Python files
    python_files = glob.glob('**/*.py', recursive=True)
    
    updated_count = 0
    for file_path in python_files:
        if update_imports_in_file(file_path, moved_files):
            updated_count += 1
    
    print(f"✅ Updated imports in {updated_count} files")

def create_init_files():
    """Create __init__.py files in new directories"""
    directories = ['launchers', 'visual', 'conversation', 'demos', 'core', 'integration', 'scripts']
    
    for directory in directories:
        init_file = os.path.join(directory, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write(f'"""{directory.title()} module"""\n')
            print(f"✅ Created {init_file}")

def main():
    """Main cleanup function"""
    print("🧹 DAWN Home Directory Cleanup")
    print("=" * 40)
    
    # Create directories
    create_directories()
    
    # Categorize files
    categories = categorize_files()
    
    # Move files
    print("\n📁 Moving files to organized directories...")
    moved_files = move_files(categories)
    
    # Create __init__.py files
    print("\n📝 Creating __init__.py files...")
    create_init_files()
    
    # Update imports
    update_all_imports(moved_files)
    
    print("\n✅ Home directory cleanup complete!")
    print("\n📊 Summary of moved files:")
    for directory, files in moved_files.items():
        if files:
            print(f"   {directory}/: {len(files)} files")
    
    print("\n🎯 Next steps:")
    print("   1. Test the system to ensure imports work correctly")
    print("   2. Update any hardcoded paths in configuration files")
    print("   3. Update documentation to reflect new structure")

if __name__ == "__main__":
    main() 