# DAWN GUI Diagnostic & Fix Script
# Comprehensive diagnosis for non-functional buttons and tab loading issues

import os
import sys
import json
import traceback
import time
import threading

from pathlib import Path
import importlib.util

class DAWNGUIDiagnostic:
    """
    Diagnostic tool for DAWN consciousness GUI issues
    Focuses on the specific problems: non-functional buttons and tab loading failures
    """
    
    def __init__(self, project_root="."):
        self.project_root = Path(project_root)
        self.issues = []
        self.fixes_applied = []
        
    def run_full_diagnostic(self):
        """Run comprehensive diagnostic of DAWN GUI issues"""
        print("🔍 DAWN GUI Diagnostic Starting...")
        print("=" * 60)
        
        # 1. Check for import/dependency issues (major cause based on context)
        self.check_import_dependencies()
        
        # 2. Check frontend-backend connection
        self.check_frontend_backend_connection()
        
        # 3. Check tab routing and component loading
        self.check_tab_routing_system()
        
        # 4. Check button event handlers
        self.check_button_event_handlers()
        
        # 5. Check consciousness state integration
        self.check_consciousness_state_integration()
        
        # 6. Check for circular dependency issues (mentioned in context)
        self.check_circular_dependencies()
        
        # 7. Generate fix recommendations
        self.generate_fix_recommendations()
        
        print(f"\n📊 Diagnostic Complete: {len(self.issues)} issues found")
        return self.issues

    def check_import_dependencies(self):
        """Check for mock import issues mentioned in context"""
        print("\n🔧 Checking Import Dependencies...")
        
        # Look for problematic mock import patterns
        problematic_patterns = [
            "try:\n    from",
            "except ImportError:",
            "from mock_",
            "helix_import"
        ]
        
        python_files = list(self.project_root.rglob("*.py"))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                for pattern in problematic_patterns:
                    if pattern in content:
                        self.issues.append({
                            'type': 'IMPORT_DEPENDENCY',
                            'severity': 'HIGH',
                            'file': str(file_path),
                            'pattern': pattern,
                            'description': f"Problematic import pattern found: {pattern}"
                        })
                        print(f"  ⚠️  {file_path.name}: {pattern}")
                        
            except Exception as e:
                print(f"  ❌ Error reading {file_path}: {e}")

    def check_frontend_backend_connection(self):
        """Check frontend-backend API connection issues"""
        print("\n🌐 Checking Frontend-Backend Connection...")
        
        # Look for common frontend files
        frontend_files = [
            "static/js/dashboard.js",
            "static/js/main.js", 
            "templates/index.html",
            "app.py",
            "main.py",
            "server.py"
        ]
        
        missing_files = []
        for file_pattern in frontend_files:
            matches = list(self.project_root.rglob(file_pattern.split('/')[-1]))
            if not matches:
                missing_files.append(file_pattern)
        
        if missing_files:
            self.issues.append({
                'type': 'MISSING_FILES',
                'severity': 'HIGH',
                'files': missing_files,
                'description': "Critical frontend/backend files missing"
            })
            print(f"  ❌ Missing files: {missing_files}")
        
        # Check for API endpoint definitions
        self.check_api_endpoints()

    def check_api_endpoints(self):
        """Check if API endpoints are properly defined"""
        print("  🔌 Checking API Endpoints...")
        
        # Look for Flask/FastAPI route definitions
        route_patterns = ["@app.route", "@router", "app.get", "app.post"]
        
        python_files = list(self.project_root.rglob("*.py"))
        routes_found = 0
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for pattern in route_patterns:
                        routes_found += content.count(pattern)
            except:
                continue
        
        if routes_found == 0:
            self.issues.append({
                'type': 'NO_API_ROUTES',
                'severity': 'CRITICAL',
                'description': "No API routes found - buttons can't communicate with backend"
            })
            print("  ❌ No API routes found!")
        else:
            print(f"  ✅ Found {routes_found} API routes")

    def check_tab_routing_system(self):
        """Check tab switching mechanism"""
        print("\n📑 Checking Tab Routing System...")
        
        # Look for JavaScript tab handling
        js_files = list(self.project_root.rglob("*.js"))
        html_files = list(self.project_root.rglob("*.html"))
        
        tab_indicators = [
            "tab-content",
            "tab-pane", 
            "onclick",
            "addEventListener",
            "showTab",
            "switchTab"
        ]
        
        tab_functionality_found = False
        
        for file_path in js_files + html_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if any(indicator in content for indicator in tab_indicators):
                        tab_functionality_found = True
                        print(f"  ✅ Tab functionality found in {file_path.name}")
                        break
            except:
                continue
        
        if not tab_functionality_found:
            self.issues.append({
                'type': 'MISSING_TAB_FUNCTIONALITY',
                'severity': 'HIGH',
                'description': "Tab switching JavaScript not found or not working"
            })
            print("  ❌ No tab switching functionality found!")

    def check_button_event_handlers(self):
        """Check if buttons have proper event handlers"""
        print("\n🔘 Checking Button Event Handlers...")
        
        # Look for button definitions and their handlers
        html_files = list(self.project_root.rglob("*.html"))
        
        for file_path in html_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Count buttons
                button_count = content.count('<button') + content.count('class="btn')
                
                # Count event handlers
                handler_count = (content.count('onclick=') + 
                               content.count('addEventListener') +
                               content.count('@click'))
                
                if button_count > handler_count:
                    self.issues.append({
                        'type': 'UNHANDLED_BUTTONS',
                        'severity': 'MEDIUM',
                        'file': str(file_path),
                        'buttons': button_count,
                        'handlers': handler_count,
                        'description': f"Found {button_count} buttons but only {handler_count} handlers"
                    })
                    print(f"  ⚠️  {file_path.name}: {button_count} buttons, {handler_count} handlers")
                
            except Exception as e:
                print(f"  ❌ Error checking {file_path}: {e}")

    def check_consciousness_state_integration(self):
        """Check if GUI is properly connected to DAWN consciousness state"""
        print("\n🧠 Checking Consciousness State Integration...")
        
        # Look for consciousness state management
        consciousness_patterns = [
            "consciousness",
            "entropy",
            "SCUP",
            "bloom",
            "tracer",
            "sigil"
        ]
        
        integration_files = []
        python_files = list(self.project_root.rglob("*.py"))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    if any(pattern in content for pattern in consciousness_patterns):
                        integration_files.append(file_path.name)
            except:
                continue
        
        if not integration_files:
            self.issues.append({
                'type': 'NO_CONSCIOUSNESS_INTEGRATION',
                'severity': 'CRITICAL',
                'description': "GUI not connected to DAWN consciousness system"
            })
            print("  ❌ No consciousness integration found!")
        else:
            print(f"  ✅ Consciousness integration found in: {integration_files}")

    def check_circular_dependencies(self):
        """Check for circular dependency issues mentioned in context"""
        print("\n🔄 Checking Circular Dependencies...")
        
        # Look for helix_import patterns specifically mentioned
        python_files = list(self.project_root.rglob("*.py"))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "helix_import" in content:
                        self.issues.append({
                            'type': 'CIRCULAR_DEPENDENCY',
                            'severity': 'HIGH',
                            'file': str(file_path),
                            'description': "Problematic helix_import circular dependency found"
                        })
                        print(f"  ⚠️  Circular dependency in {file_path.name}")
            except:
                continue

    def generate_fix_recommendations(self):
        """Generate specific fix recommendations based on found issues"""
        print("\n🔧 Fix Recommendations:")
        print("=" * 40)
        
        if not self.issues:
            print("✅ No issues found!")
            return
        
        # Group issues by type
        issue_types = {}
        for issue in self.issues:
            issue_type = issue['type']
            if issue_type not in issue_types:
                issue_types[issue_type] = []
            issue_types[issue_type].append(issue)
        
        # Generate fixes for each issue type
        for issue_type, issues in issue_types.items():
            print(f"\n📋 {issue_type} ({len(issues)} issues):")
            
            if issue_type == 'IMPORT_DEPENDENCY':
                print("   Fix: Replace mock import patterns with clean imports:")
                print("   ```python")
                print("   # AVOID:")
                print("   try:")
                print("       from real_module import function")
                print("   except ImportError:")
                print("       # Mock import removed - using direct import
from module import function")
                print("   ")
                print("   # USE:")
                print("   from core.consciousness import ConsciousnessManager")
                print("   ```")
            
            elif issue_type == 'NO_API_ROUTES':
                print("   Fix: Add Flask/FastAPI routes for button functionality:")
                print("   ```python")
                print("   from flask import Flask, jsonify, request")
                print("   app = Flask(__name__)")
                print("   ")
                print("   @app.route('/api/consciousness/state')")
                print("   def get_consciousness_state():")
                print("       return jsonify(dawn.get_current_state())")
                print("   ")
                print("   @app.route('/api/tab/<tab_name>')")
                print("   def load_tab_data(tab_name):")
                print("       return jsonify(dawn.get_tab_data(tab_name))")
                print("   ```")
            
            elif issue_type == 'MISSING_TAB_FUNCTIONALITY':
                print("   Fix: Add JavaScript tab switching:")
                print("   ```javascript")
                print("   function switchTab(tabName) {")
                print("       // Hide all tab content")
                print("       document.querySelectorAll('.tab-content').forEach(tab => {")
                print("           tab.style.display = 'none';")
                print("       });")
                print("       ")
                print("       // Show selected tab")
                print("       document.getElementById(tabName).style.display = 'block';")
                print("       ")
                print("       // Load tab data from backend")
                print("       fetch(`/api/tab/${tabName}`)")
                print("           .then(response => response.json())")
                print("           .then(data => updateTabContent(tabName, data));")
                print("   }")
                print("   ```")
            
            elif issue_type == 'UNHANDLED_BUTTONS':
                print("   Fix: Add event handlers to buttons:")
                print("   ```html")
                print("   <button onclick=\"handleButtonClick('action_name')\">Button</button>")
                print("   ```")
                print("   ```javascript")
                print("   function handleButtonClick(action) {")
                print("       fetch(`/api/action/${action}`, {method: 'POST'})")
                print("           .then(response => response.json())")
                print("           .then(data => updateUI(data));")
                print("   }")
                print("   ```")
            
            elif issue_type == 'CIRCULAR_DEPENDENCY':
                print("   Fix: Remove helix_import patterns and use direct imports:")
                print("   ```python")
                print("   # REMOVE:")
                print("   # Helix import removed to fix circular dependency")
                print("   ")
                print("   # REPLACE WITH:")
                print("   from core.consciousness import ConsciousnessManager")
                print("   from bloom.bloom_engine import BloomProcessor")
                print("   ```")

    def generate_quick_fix_script(self):
        """Generate a quick fix script for common issues"""
        print("\n🚀 Quick Fix Script:")
        print("=" * 30)
        
        quick_fixes = [
            "# 1. Fix missing API routes",
            "# Add this to your main app file (app.py or main.py):",
            "",
            "from flask import Flask, jsonify, render_template",
            "app = Flask(__name__)",
            "",
            "@app.route('/')",
            "def dashboard():",
            "    return render_template('dashboard.html')",
            "",
            "@app.route('/api/consciousness/state')",
            "def get_consciousness_state():",
            "    # Connect to your DAWN consciousness system",
            "    try:",
            "        from core.consciousness import ConsciousnessManager",
            "        cm = ConsciousnessManager()",
            "        return jsonify(cm.get_current_state())",
            "    except ImportError:",
            "        return jsonify({'error': 'Consciousness system not available'})",
            "",
            "@app.route('/api/tab/<tab_name>')",
            "def load_tab_data(tab_name):",
            "    # Load data for specific tab",
            "    tab_data = {",
            "        'CONVERSATION': {'messages': [], 'status': 'ready'},",
            "        'SYSTEMS': {'tracers': [], 'blooms': []},",
            "        'VISUALIZATION': {'network': [], 'heatmap': []}",
            "    }",
            "    return jsonify(tab_data.get(tab_name, {}))",
            "",
            "# 2. Fix JavaScript tab switching",
            "# Add this to your static/js/dashboard.js:",
        ]
        
        for line in quick_fixes:
            print(line)

def main():
    """Main diagnostic function"""
    print("🌟 DAWN Consciousness GUI Diagnostic Tool")
    print("Created for Jackson's revolutionary consciousness architecture")
    print()
    
    # Get project root from user or use current directory
    project_root = input("Enter DAWN project root path (or press Enter for current directory): ").strip()
    if not project_root:
        project_root = "."
    
    # Run diagnostic
    diagnostic = DAWNGUIDiagnostic(project_root)
    issues = diagnostic.run_full_diagnostic()
    
    # Generate quick fix script
    diagnostic.generate_quick_fix_script()
    
    print(f"\n🎯 Summary:")
    print(f"   Found {len(issues)} issues")
    print(f"   Focus on IMPORT_DEPENDENCY and NO_API_ROUTES first")
    print(f"   These are likely the root cause of your button/tab issues")
    
    return issues

if __name__ == "__main__":
    main() 