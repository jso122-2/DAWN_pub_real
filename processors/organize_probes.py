# organize_probes.py
"""
Organize probe files into a proper module structure
"""

from pathlib import Path
import shutil

def organize_probes():
    """Create probes module with organized structure"""
    
    schema_dir = Path("schema")
    probes_dir = schema_dir / "probes"
    probes_dir.mkdir(exist_ok=True)
    
    # Create __init__.py
    init_content = '''"""
DAWN Probe System
=================
Specialized monitoring probes for different aspects of the schema
"""

from .alignment_probe import (
    AlignmentProbe, 
    get_current_alignment,
    check_alignment_anomalies,
    apply_alignment_correction
)

from .constitution_monitor import (
    ConstitutionMonitor,
    ConstitutionalGenome,
    AdvancedConstitutionalGuard
)

from .pressure_reflex import pressure_reflex

from .sigil_probe import probe_sigil

__all__ = [
    'AlignmentProbe',
    'ConstitutionMonitor', 
    'pressure_reflex',
    'probe_sigil',
    'get_current_alignment',
    'check_alignment_anomalies',
    'apply_alignment_correction'
]
'''
    
    with open(probes_dir / "__init__.py", 'w', encoding='utf-8') as f:
        f.write(init_content)
    
    print(f"✅ Created {probes_dir}/__init__.py")
    
    # Move probe files
    probe_files = [
        "alignment_probe.py",
        "constitution_monitor.py", 
        "pressure_reflex.py",
        "sigil_probe.py"
    ]
    
    for filename in probe_files:
        src = schema_dir / filename
        if src.exists():
            dst = probes_dir / filename
            shutil.move(str(src), str(dst))
            print(f"📦 Moved {filename} to probes/")
    
    print("\n✅ Probe organization complete!")
    print("   Large specialized probes kept separate but organized")
    
    return probes_dir

if __name__ == "__main__":
    organize_probes()