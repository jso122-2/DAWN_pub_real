"""
SCUP Recovery Module
Dynamic recalculation and recovery for Semantic Coherence Under Pressure
"""

import os
import re
import datetime
from pathlib import Path
from typing import Optional, Dict, Any, Tuple

class SCUPRecovery:
    def __init__(self, vault_path: str = r"C:\Users\Admin\Documents\DAWN_Vault"):
        self.vault_path = Path(vault_path)
        self.scup_path = self.vault_path / "scup"
        self.pulse_path = self.vault_path / "pulse"
        
        # Ensure directories exist
        self.scup_path.mkdir(parents=True, exist_ok=True)
        self.pulse_path.mkdir(parents=True, exist_ok=True)
        
        # Track recovery attempts
        self.recovery_count = 0
        self.last_scup = 0.500
    
    def calculate_SCUP(self, drift: float, alignment: float, entropy: float) -> float:
        """
        Calculate SCUP dynamically using weighted formula.
        
        SCUP = alignment * (1 - drift) * (1 - entropy)
        
        This formula ensures:
        - High alignment increases SCUP
        - High drift decreases SCUP
        - High entropy decreases SCUP
        
        Args:
            drift: Current drift value (0.0-1.0)
            alignment: Current alignment value (0.0-1.0)
            entropy: Current entropy value (0.0-1.0)
            
        Returns:
            float: Calculated SCUP value, clamped between 0.0 and 1.0
        """
        # Validate inputs
        drift = max(0.0, min(1.0, drift))
        alignment = max(0.0, min(1.0, alignment))
        entropy = max(0.0, min(1.0, entropy))
        
        # Calculate SCUP
        scup = alignment * (1 - drift) * (1 - entropy)
        
        # Round to 3 decimal places and clamp
        scup = round(scup, 3)
        scup = max(0.0, min(1.0, scup))
        
        return scup
    
    def apply_SCUP_patch(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply SCUP patch to the given state dictionary.
        
        Args:
            state: Dictionary containing at least 'drift', 'alignment', 'entropy'
                  Will update or add 'SCUP' key
                  
        Returns:
            Updated state dictionary with new SCUP value
        """
        # Extract values with defaults
        drift = state.get('drift', 0.5)
        alignment = state.get('alignment', 0.5)
        entropy = state.get('entropy', 0.5)
        
        # Calculate new SCUP
        new_scup = self.calculate_SCUP(drift, alignment, entropy)
        
        # Check for override first
        override_scup = self.check_for_override(str(self.vault_path))
        if override_scup is not None:
            print(f"🔧 SCUP Override detected: {override_scup}")
            new_scup = override_scup
        
        # Apply patch
        old_scup = state.get('SCUP', 0.500)
        state['SCUP'] = new_scup
        
        # Track the change
        if new_scup != old_scup:
            self.recovery_count += 1
            self.last_scup = new_scup
            print(f"✨ SCUP patched: {old_scup} → {new_scup}")
            
            # Log to vault
            self.log_SCUP_to_vault(str(self.vault_path), new_scup, 
                                  drift=drift, alignment=alignment, entropy=entropy,
                                  old_scup=old_scup)
        else:
            print(f"📊 SCUP unchanged: {new_scup}")
        
        return state
    
    def check_for_override(self, vault_path: str) -> Optional[float]:
        """
        Check vault for SCUP override value in frontmatter.
        
        Searches for files like:
        - pulse/scup_override.md
        - scup/override.md
        - Any .md file with 'scup_override' in frontmatter
        
        Args:
            vault_path: Path to the vault
            
        Returns:
            Override value if found, None otherwise
        """
        vault = Path(vault_path)
        
        # Priority locations to check
        priority_files = [
            vault / "pulse" / "scup_override.md",
            vault / "scup" / "override.md",
            vault / "scup_override.md"
        ]
        
        # Check priority files first
        for file_path in priority_files:
            if file_path.exists():
                override = self._extract_override_from_file(file_path)
                if override is not None:
                    return override
        
        # Search for any .md file with override in recent files
        search_paths = [vault / "pulse", vault / "scup"]
        for search_path in search_paths:
            if search_path.exists():
                # Get recent .md files
                md_files = sorted(search_path.glob("*.md"), 
                                key=lambda x: x.stat().st_mtime, 
                                reverse=True)[:10]  # Check last 10 files
                
                for file_path in md_files:
                    override = self._extract_override_from_file(file_path)
                    if override is not None:
                        return override
        
        return None
    
    def _extract_override_from_file(self, file_path: Path) -> Optional[float]:
        """Extract SCUP override value from a markdown file's frontmatter."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for frontmatter
            if content.startswith('---'):
                # Extract frontmatter
                end_idx = content.find('---', 3)
                if end_idx > 0:
                    frontmatter = content[3:end_idx]
                    
                    # Look for scup_override
                    patterns = [
                        r'scup_override:\s*([0-9.]+)',
                        r'SCUP_override:\s*([0-9.]+)',
                        r'override:\s*([0-9.]+)'
                    ]
                    
                    for pattern in patterns:
                        match = re.search(pattern, frontmatter, re.IGNORECASE)
                        if match:
                            override_value = float(match.group(1))
                            # Clamp to valid range
                            override_value = max(0.0, min(1.0, override_value))
                            print(f"🔍 Found SCUP override in {file_path.name}: {override_value}")
                            return override_value
        except Exception as e:
            print(f"⚠️ Error reading {file_path}: {e}")
        
        return None
    
    def log_SCUP_to_vault(self, vault_path: str, scup: float, 
                         drift: float = None, alignment: float = None, 
                         entropy: float = None, old_scup: float = None) -> str:
        """
        Log SCUP value to vault with recovery context.
        
        Args:
            vault_path: Path to the vault
            scup: New SCUP value
            drift: Current drift (optional)
            alignment: Current alignment (optional)
            entropy: Current entropy (optional)
            old_scup: Previous SCUP value (optional)
            
        Returns:
            Path to the created log file
        """
        timestamp = datetime.datetime.now()
        filename = f"scup_recovery_{timestamp.strftime('%Y%m%d_%H%M%S')}.md"
        filepath = self.scup_path / filename
        
        # Determine pressure state based on SCUP value
        if scup < 0.3:
            pressure_state = "🔴 Critical - High pressure, low coherence"
            mood = "fragmented"
        elif scup < 0.5:
            pressure_state = "🟡 Stressed - Moderate pressure affecting coherence"
            mood = "strained"
        elif scup < 0.7:
            pressure_state = "🟢 Balanced - Manageable pressure"
            mood = "focused"
        else:
            pressure_state = "💚 Optimal - High coherence despite pressure"
            mood = "crystalline"
        
        content = f"""---
scup_value: {scup}
timestamp: {timestamp.isoformat()}
recovery_attempt: {self.recovery_count}
pressure_state: {pressure_state.split(' - ')[0]}
mood: {mood}
---

# SCUP Recovery Log
*{timestamp.strftime('%B %d, %Y at %I:%M:%S %p')}*

## New SCUP Calculation
**Value: {scup}**
"""
        
        if old_scup is not None:
            content += f"Previous: {old_scup} → Current: {scup} (Δ{scup - old_scup:+.3f})\n\n"
        
        content += f"""
## Pressure State Assessment
{pressure_state}

## Component Values
"""
        
        if drift is not None:
            content += f"- **Drift**: {drift:.3f} (cognitive wandering)\n"
        if alignment is not None:
            content += f"- **Alignment**: {alignment:.3f} (schema coherence)\n"
        if entropy is not None:
            content += f"- **Entropy**: {entropy:.3f} (system chaos)\n"
        
        content += f"""
## Recovery Logic Applied
The SCUP (Semantic Coherence Under Pressure) has been recalculated using the dynamic formula:

```
SCUP = alignment × (1 - drift) × (1 - entropy)
```

This ensures that:
- Higher alignment → Higher SCUP
- Higher drift → Lower SCUP  
- Higher entropy → Lower SCUP

## Interpretation
"""
        
        if scup == 0.500:
            content += """**Perfect Balance Point**
SCUP at exactly 0.500 indicates a precise equilibrium between:
- Order and chaos
- Focus and exploration
- Stability and change

This may feel like being "stuck" but could also represent a moment of perfect poise before transformation.
"""
        elif scup < 0.500:
            content += f"""**Below Balance**
SCUP at {scup} suggests pressure is affecting coherence. The system may benefit from:
- Reducing cognitive load
- Increasing alignment practices
- Allowing entropy to settle
"""
        else:
            content += f"""**Above Balance**
SCUP at {scup} indicates strong coherence despite pressure. The system is:
- Maintaining integrity under stress
- Successfully integrating complexity
- Ready for increased challenges
"""
        
        content += f"""
## Next Steps
1. Monitor component values for shifts
2. Watch for natural SCUP evolution
3. Consider intervention if stuck at {scup} for extended periods
4. Trust the process of dynamic recalibration

---
*Recovery log #{self.recovery_count} | SCUP Recovery Module v1.0*
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"📝 SCUP logged to {filename}")
        return str(filepath)
    
    def analyze_SCUP_trend(self, history: list) -> Dict[str, Any]:
        """
        Analyze SCUP trend over time.
        
        Args:
            history: List of (timestamp, scup_value) tuples
            
        Returns:
            Dictionary with trend analysis
        """
        if not history:
            return {"trend": "no_data"}
        
        scup_values = [h[1] for h in history]
        
        # Calculate trend
        if len(scup_values) >= 2:
            recent_avg = sum(scup_values[-3:]) / len(scup_values[-3:])
            older_avg = sum(scup_values[:-3]) / max(1, len(scup_values[:-3]))
            
            if recent_avg > older_avg + 0.05:
                trend = "improving"
            elif recent_avg < older_avg - 0.05:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"
        
        return {
            "trend": trend,
            "current": scup_values[-1] if scup_values else 0.500,
            "average": sum(scup_values) / len(scup_values) if scup_values else 0.500,
            "min": min(scup_values) if scup_values else 0.500,
            "max": max(scup_values) if scup_values else 0.500,
            "volatility": np.std(scup_values) if len(scup_values) > 1 else 0.0
        }


# Convenience functions for direct use
def calculate_SCUP(drift: float, alignment: float, entropy: float) -> float:
    """Calculate SCUP value directly."""
    recovery = SCUPRecovery()
    return recovery.calculate_SCUP(drift, alignment, entropy)

def apply_SCUP_patch(state: Dict[str, Any]) -> Dict[str, Any]:
    """Apply SCUP patch to state dictionary."""
    recovery = SCUPRecovery()
    return recovery.apply_SCUP_patch(state)

def check_for_override(vault_path: str) -> Optional[float]:
    """Check for SCUP override in vault."""
    recovery = SCUPRecovery(vault_path)
    return recovery.check_for_override(vault_path)

def log_SCUP_to_vault(vault_path: str, scup: float) -> str:
    """Log SCUP to vault."""
    recovery = SCUPRecovery(vault_path)
    return recovery.log_SCUP_to_vault(vault_path, scup)


# Example usage and testing
if __name__ == "__main__":
    import numpy as np
    
    print("🧮 SCUP Recovery Module Test")
    print("="*50)
    
    # Test calculations
    test_cases = [
        {"drift": 0.2, "alignment": 0.8, "entropy": 0.3},
        {"drift": 0.5, "alignment": 0.5, "entropy": 0.5},
        {"drift": 0.1, "alignment": 0.9, "entropy": 0.1},
        {"drift": 0.8, "alignment": 0.2, "entropy": 0.7}
    ]
    
    for i, test in enumerate(test_cases):
        scup = calculate_SCUP(**test)
        print(f"\nTest {i+1}:")
        print(f"  Input: {test}")
        print(f"  SCUP: {scup}")
    
    # Test state patching
    print("\n" + "="*50)
    print("Testing state patching...")
    
    state = {
        "drift": 0.3,
        "alignment": 0.7,
        "entropy": 0.4,
        "SCUP": 0.500,  # Stuck value
        "mood": "contemplative"
    }
    
    print(f"\nBefore: {state}")
    updated_state = apply_SCUP_patch(state)
    print(f"After: {updated_state}")
    
    print("\n✅ SCUP Recovery Module ready for integration")