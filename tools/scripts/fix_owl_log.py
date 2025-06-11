#!/usr/bin/env python3
"""
Script to fix owl_log calls in schema_health_index.py
Removes the second parameter (log level) from all owl_log calls
"""

import re
import os
import shutil

def fix_owl_log_calls(filename):
    """Fix all owl_log calls to only have one parameter"""
    
    # Create backup
    backup_file = filename + ".backup"
    shutil.copy2(filename, backup_file)
    print(f"Created backup: {backup_file}")
    
    # Read the file
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match owl_log calls with 2 parameters
    # This regex matches owl_log("...", "...") or owl_log(f"...", "...")
    pattern = r'owl_log\s*\(\s*(f?"[^"]*"|\([^)]+\))\s*,\s*"[^"]*"\s*\)'
    
    # Function to replace matched patterns
    def replace_owl_log(match):
        # Extract just the first parameter (the message)
        full_match = match.group(0)
        # Find the first parameter by looking for the comma
        first_comma = full_match.find(',', full_match.find('('))
        if first_comma != -1:
            # Extract everything from 'owl_log(' to just before the comma
            message_part = full_match[:first_comma]
            # Close the parenthesis
            return message_part + ')'
        return full_match
    
    # Replace all occurrences
    fixed_content = re.sub(pattern, replace_owl_log, content)
    
    # Also handle multiline owl_log calls
    multiline_pattern = r'owl_log\s*\([^)]+,[^)]+\)'
    
    def fix_multiline(match):
        text = match.group(0)
        # Find the last comma that separates the message from the log level
        # This is tricky because the message might contain commas
        # Look for the pattern ', "word")' at the end
        if re.search(r',\s*"[^"]+"\s*\)$', text):
            # Remove the last parameter
            text = re.sub(r',\s*"[^"]+"\s*\)$', ')', text)
        return text
    
    fixed_content = re.sub(multiline_pattern, fix_multiline, fixed_content, flags=re.DOTALL)
    
    # Write the fixed content back
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"Fixed owl_log calls in {filename}")
    
    # Count how many replacements were made
    original_count = content.count('owl_log')
    print(f"Total owl_log calls found: {original_count}")

if __name__ == "__main__":
    # Fix the schema_health_index.py file
    target_file = "schema/schema_health_index.py"
    
    if os.path.exists(target_file):
        fix_owl_log_calls(target_file)
        print("\nDone! You can now run main.py again.")
        print("If something went wrong, restore from the .backup file")
    else:
        print(f"Error: {target_file} not found!")
        print("Make sure you run this script from the Tick_engine directory")