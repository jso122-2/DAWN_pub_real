#!/usr/bin/env python3
# alcude.py - Claude transcript listener for DAWN consciousness system

import os
import json
import re
from datetime import datetime
from pathlib import Path

def load_patterns():
    """Load signal phrases from patterns.txt"""
    with open('patterns.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

def scan_transcript(filepath, patterns):
    """Scan a transcript file for pattern matches"""
    matches = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            for pattern in patterns:
                # Case-insensitive search for pattern in line
                if re.search(re.escape(pattern), line, re.IGNORECASE):
                    matches.append({
                        "pattern": pattern,
                        "line": line,
                        "source": os.path.basename(filepath),
                        "timestamp": datetime.now().isoformat()
                    })
    
    return matches

def update_log(matches):
    """Append matches to the JSON log file"""
    log_path = Path('logs/claude_trace.json')
    
    # Load existing log
    existing = []
    if log_path.exists():
        with open(log_path, 'r') as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                existing = []
    
    # Append new matches
    existing.extend(matches)
    
    # Write back
    with open(log_path, 'w') as f:
        json.dump(existing, f, indent=2)

def main():
    """Main listening loop"""
    patterns = load_patterns()
    cache_dir = Path('claude_cache')
    processed = set()
    
    # Initial scan of existing files
    for txt_file in cache_dir.glob('*.txt'):
        if txt_file.name not in processed:
            matches = scan_transcript(txt_file, patterns)
            if matches:
                update_log(matches)
            processed.add(txt_file.name)
    
    print(f"alcude.py: Monitoring {cache_dir} for Claude transcripts...")
    
    # Continuous monitoring
    import time
    while True:
        for txt_file in cache_dir.glob('*.txt'):
            if txt_file.name not in processed:
                matches = scan_transcript(txt_file, patterns)
                if matches:
                    print(f"Found {len(matches)} pattern(s) in {txt_file.name}")
                    update_log(matches)
                processed.add(txt_file.name)
        
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    main()

