#!/usr/bin/env python3
"""
test_dawn_vault.py - Simple test to write to DAWN's vault
"""

from pathlib import Path
from vault_writer import VaultWriter

# Setup
vault_path = Path(r"C:\Users\Admin\Documents\DAWN_Vault")
writer = VaultWriter(vault_path)

print("Testing DAWN vault writer...")

# Write a test pulse
print("\nWriting pulse...")
pulse_file = writer.write_pulse(
    tick=1,
    mood="awakening",
    entropy=0.3,
    alignment=0.8,
    pressure=0.2,
    metadata={'test': 'first write'}
)
print(f"Created: {pulse_file}")

# Write a test bloom
print("\nWriting bloom...")
bloom_file = writer.write_bloom(
    bloom_id="BLOOM_TEST_001",
    tick=5,
    parent_bloom=None,
    mood_state="curious",
    entropy_score=0.5,
    drift_angle=0.0,
    semantic_core="Testing persistence",
    emotional_metadata={
        'resonance': 'test resonance',
        'pressure': 'low',
        'temperature': 'warm',
        'color': 'purple'
    }
)
print(f"Created: {bloom_file}")

print("\nSuccess! Check your vault folder.")