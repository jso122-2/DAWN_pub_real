import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from substrate.helix.helix_import_architecture import helix_import
    print("Successfully imported helix_import")
except Exception as e:
    print(f"Error importing helix_import: {e}")
    print(f"Python path: {sys.path}") 