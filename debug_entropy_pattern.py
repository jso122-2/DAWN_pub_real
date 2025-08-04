#!/usr/bin/env python3
"""
Debug script to test entropy extraction pattern
"""

import re

# Test the pattern
test_text = "[2025-07-27 16:58:00] REFLECTION: I am experiencing contemplative consciousness at entropy 0.698"

patterns = [
    r'entropy (\d+\.\d+)',
    r'at entropy (\d+\.\d+)',
    r'entropy (\d+\.?\d*)',
    r'at entropy (\d+\.?\d*)'
]

print("Testing entropy extraction patterns:")
print(f"Text: {test_text}")
print()

for i, pattern in enumerate(patterns, 1):
    match = re.search(pattern, test_text, re.IGNORECASE)
    if match:
        print(f"Pattern {i}: {pattern}")
        print(f"  Match: {match.group(0)}")
        print(f"  Captured: {match.group(1)}")
        print()
    else:
        print(f"Pattern {i}: {pattern} - NO MATCH")
        print()

# Test with more variations
test_cases = [
    "I am experiencing contemplative consciousness at entropy 0.698",
    "entropy 0.702",
    "at entropy 0.693",
    "consciousness at entropy 0.675"
]

print("Testing with different text variations:")
for test_case in test_cases:
    print(f"\nText: {test_case}")
    match = re.search(r'at entropy (\d+\.\d+)', test_case, re.IGNORECASE)
    if match:
        print(f"  Match: {match.group(0)}")
        print(f"  Captured: {match.group(1)}")
    else:
        print("  NO MATCH") 