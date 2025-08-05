#!/usr/bin/env python3
"""
Validate Consolidated GUI File
Check for common issues that could prevent the server from loading it
"""

from pathlib import Path
import json

def validate_html_structure(content):
    """Check basic HTML structure"""
    issues = []
    
    if not content.strip().startswith('<!DOCTYPE html>'):
        issues.append("Missing or incorrect DOCTYPE declaration")
    
    if '<html' not in content:
        issues.append("Missing <html> tag")
    
    if '<head>' not in content:
        issues.append("Missing <head> section")
    
    if '<body>' not in content:
        issues.append("Missing <body> section")
        
    if '</html>' not in content:
        issues.append("Missing closing </html> tag")
    
    return issues

def validate_javascript(content):
    """Check for basic JavaScript syntax issues"""
    issues = []
    
    # Count opening and closing braces
    open_braces = content.count('{')
    close_braces = content.count('}')
    
    if open_braces != close_braces:
        issues.append(f"Mismatched braces: {open_braces} open vs {close_braces} close")
    
    # Count opening and closing parentheses in script sections
    script_start = content.find('<script>')
    if script_start != -1:
        script_end = content.find('</script>', script_start)
        if script_end != -1:
            script_content = content[script_start:script_end]
            open_parens = script_content.count('(')
            close_parens = script_content.count(')')
            
            if open_parens != close_parens:
                issues.append(f"Mismatched parentheses in script: {open_parens} open vs {close_parens} close")
    
    return issues

def validate_encoding(file_path):
    """Test reading the file with different encodings"""
    encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            return encoding, content, None
        except Exception as e:
            if encoding == encodings[-1]:  # Last encoding
                return None, None, str(e)
    
    return None, None, "All encodings failed"

def main():
    print("🔍 VALIDATING CONSOLIDATED GUI")
    print("=" * 50)
    
    gui_file = Path('dawn_consolidated_gui.html')
    
    if not gui_file.exists():
        print("❌ dawn_consolidated_gui.html not found!")
        return 1
    
    print(f"✅ File exists: {gui_file}")
    print(f"📊 Size: {gui_file.stat().st_size:,} bytes")
    print()
    
    # Test encoding
    print("🔍 Testing file encoding...")
    encoding, content, error = validate_encoding(gui_file)
    
    if error:
        print(f"❌ Encoding error: {error}")
        return 1
    
    print(f"✅ Successfully read with encoding: {encoding}")
    print(f"📊 Content length: {len(content):,} characters")
    print()
    
    # Validate HTML structure
    print("🔍 Validating HTML structure...")
    html_issues = validate_html_structure(content)
    
    if html_issues:
        print("❌ HTML Issues found:")
        for issue in html_issues:
            print(f"   • {issue}")
    else:
        print("✅ HTML structure looks good")
    print()
    
    # Validate JavaScript
    print("🔍 Validating JavaScript...")
    js_issues = validate_javascript(content)
    
    if js_issues:
        print("❌ JavaScript Issues found:")
        for issue in js_issues:
            print(f"   • {issue}")
    else:
        print("✅ JavaScript structure looks good")
    print()
    
    # Check title
    title_start = content.find('<title>') + 7
    title_end = content.find('</title>')
    if title_start > 6 and title_end > title_start:
        title = content[title_start:title_end]
        print(f"📝 Title: {title}")
        
        if 'Consolidated' in title:
            print("✅ Title indicates consolidated GUI")
        else:
            print("⚠️ Title doesn't mention 'Consolidated'")
    else:
        print("❌ No title found")
    print()
    
    # Check for critical functions
    print("🔍 Checking for critical functions...")
    critical_functions = [
        'switchTab',
        'initializeGUI',
        'updateGUIWithRealData'
    ]
    
    missing_functions = []
    for func in critical_functions:
        if f'function {func}' not in content and f'{func} =' not in content:
            missing_functions.append(func)
    
    if missing_functions:
        print("⚠️ Missing functions:")
        for func in missing_functions:
            print(f"   • {func}")
    else:
        print("✅ All critical functions present")
    print()
    
    # Summary
    total_issues = len(html_issues) + len(js_issues) + len(missing_functions)
    
    if total_issues == 0:
        print("🎉 FILE VALIDATION PASSED!")
        print("   The consolidated GUI should load without issues")
    else:
        print(f"⚠️ Found {total_issues} potential issues")
        print("   These might prevent the server from loading the GUI")
    
    return total_issues

if __name__ == "__main__":
    exit(main()) 