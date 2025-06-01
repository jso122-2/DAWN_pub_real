import sys

# List of key modules to check
modules_to_check = [
    'core.system_state',
    'owl.owl_auditor',
    'tracers.spider',
    'rhizome.rhizome_map',
    'schema.scup_loop',
    'codex.sigil_emitter'
]

# Function to check if the modules can be imported
def check_imports(modules):
    for module in modules:
        try:
            __import__(module)
            print(f"[Success] {module} imported successfully!")
        except ImportError as e:
            print(f"[Error] Failed to import {module}: {e}")

# Run the import checks
check_imports(modules_to_check)
