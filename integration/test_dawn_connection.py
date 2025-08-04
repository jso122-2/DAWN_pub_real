#!/usr/bin/env python3
"""
DAWN Connection Test Tool
Verifies backend-frontend communication and visual system integration
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DAWNConnectionTester:
    """Test DAWN backend-frontend connection and visual integration"""
    
    def __init__(self):
        self.runtime_dir = Path("runtime")
        self.gui_dir = Path("dawn-consciousness-gui")
        self.snapshots_dir = Path("runtime/enhanced_snapshots")
        
    def run_comprehensive_test(self):
        """Run all connection and integration tests"""
        print("🧪 DAWN Connection & Integration Test Suite")
        print("=" * 60)
        
        results = {}
        
        # Test 1: Backend Process
        results['backend'] = self.test_backend_process()
        
        # Test 2: Memory-mapped files
        results['mmap'] = self.test_memory_mapped_files()
        
        # Test 3: Tauri GUI availability
        results['tauri'] = self.test_tauri_availability()
        
        # Test 4: Visual snapshots
        results['visuals'] = self.test_visual_system()
        
        # Test 5: Enhanced visual engine
        results['enhanced_visuals'] = self.test_enhanced_visuals()
        
        # Test 6: Live data flow
        results['data_flow'] = self.test_live_data_flow()
        
        # Generate report
        self.generate_test_report(results)
        
        return results
    
    def test_backend_process(self) -> dict:
        """Test if DAWN backend is running"""
        print("\n🔍 Testing DAWN Backend Process...")
        
        try:
            # Check for Python processes (cross-platform)
            if os.name == 'nt':  # Windows
                result = subprocess.run(['powershell', '-Command', 
                    'Get-Process | Where-Object {$_.ProcessName -like "*python*"}'], 
                    capture_output=True, text=True)
                processes = result.stdout
            else:  # Unix-like
                result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
                processes = result.stdout
            
            dawn_processes = []
            for line in processes.split('\n'):
                if 'python' in line.lower() and ('dawn' in line.lower() or 'launch_dawn' in line.lower()):
                    dawn_processes.append(line.strip())
            
            if dawn_processes:
                print(f"✅ Found {len(dawn_processes)} DAWN backend process(es)")
                for proc in dawn_processes:
                    print(f"   - {proc}")
                return {'status': 'running', 'processes': dawn_processes}
            else:
                print("⚠️  No DAWN backend processes found")
                print("   Try running: python launch_dawn.py")
                return {'status': 'not_running', 'processes': []}
                
        except Exception as e:
            print(f"❌ Error checking backend: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def test_memory_mapped_files(self) -> dict:
        """Test memory-mapped file availability and freshness"""
        print("\n🗂️  Testing Memory-Mapped Files...")
        
        mmap_files = list(self.runtime_dir.glob("*.mmap"))
        
        if not mmap_files:
            print("❌ No memory-mapped files found")
            print("   Expected: runtime/dawn_consciousness.mmap")
            return {'status': 'missing', 'files': []}
        
        file_info = []
        for mmap_file in mmap_files:
            try:
                stat = mmap_file.stat()
                age_seconds = time.time() - stat.st_mtime
                
                file_info.append({
                    'name': mmap_file.name,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'age_seconds': age_seconds
                })
                
                if age_seconds < 60:  # Updated within last minute
                    freshness = "🟢 FRESH"
                elif age_seconds < 300:  # Updated within 5 minutes
                    freshness = "🟡 RECENT"
                else:
                    freshness = "🔴 STALE"
                
                print(f"✅ {mmap_file.name}: {stat.st_size:,} bytes, {freshness}")
                print(f"   Last modified: {datetime.fromtimestamp(stat.st_mtime)}")
                
            except Exception as e:
                print(f"❌ Error reading {mmap_file}: {e}")
                file_info.append({'name': mmap_file.name, 'error': str(e)})
        
        return {'status': 'found', 'files': file_info}
    
    def test_tauri_availability(self) -> dict:
        """Test Tauri GUI availability"""
        print("\n🖥️  Testing Tauri GUI Availability...")
        
        if not self.gui_dir.exists():
            print("❌ GUI directory not found")
            return {'status': 'missing', 'path': str(self.gui_dir)}
        
        # Check for package.json
        package_json = self.gui_dir / "package.json"
        if not package_json.exists():
            print("❌ package.json not found")
            return {'status': 'invalid', 'missing': 'package.json'}
        
        # Check for Tauri config
        tauri_config = self.gui_dir / "src-tauri" / "tauri.conf.json"
        if not tauri_config.exists():
            print("❌ Tauri config not found")
            return {'status': 'invalid', 'missing': 'tauri.conf.json'}
        
        print("✅ Tauri GUI structure found")
        
        # Check if GUI is currently running
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(['powershell', '-Command', 
                    'Get-Process | Where-Object {$_.ProcessName -like "*tauri*" -or $_.ProcessName -like "*dawn-consciousness-gui*"}'], 
                    capture_output=True, text=True)
                if result.stdout.strip():
                    print("✅ Tauri GUI appears to be running")
                    return {'status': 'running', 'gui_found': True}
                else:
                    print("⚠️  Tauri GUI not currently running")
                    print("   Try: cd dawn-consciousness-gui && npm run tauri dev")
                    return {'status': 'not_running', 'gui_found': True}
            else:  # Unix-like
                result = subprocess.run(['pgrep', '-f', 'tauri|dawn-consciousness'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print("✅ Tauri GUI appears to be running")
                    return {'status': 'running', 'gui_found': True}
                else:
                    print("⚠️  Tauri GUI not currently running")
                    return {'status': 'not_running', 'gui_found': True}
                    
        except Exception as e:
            print(f"⚠️  Could not check GUI process status: {e}")
            return {'status': 'unknown', 'gui_found': True}
    
    def test_visual_system(self) -> dict:
        """Test visual snapshot system"""
        print("\n📸 Testing Visual Snapshot System...")
        
        # Check for visual_trigger.py
        visual_trigger = Path("visual_trigger.py")
        if not visual_trigger.exists():
            print("❌ visual_trigger.py not found")
            return {'status': 'missing', 'component': 'visual_trigger.py'}
        
        # Check snapshots directory
        if not self.runtime_dir.exists():
            self.runtime_dir.mkdir(parents=True, exist_ok=True)
        
        snapshots_dir = self.runtime_dir / "snapshots"
        if not snapshots_dir.exists():
            snapshots_dir.mkdir(parents=True, exist_ok=True)
            print("📁 Created snapshots directory")
        
        # Count existing snapshots
        snapshot_files = list(snapshots_dir.glob("*.png")) + list(snapshots_dir.glob("*.json"))
        print(f"📊 Found {len(snapshot_files)} existing snapshot files")
        
        # Test snapshot generation
        try:
            print("🧪 Testing snapshot generation...")
            result = subprocess.run([
                sys.executable, "visual_trigger.py", 
                "--snapshot-now", "--simulate-tick"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ Visual snapshot test successful")
                return {'status': 'working', 'snapshot_count': len(snapshot_files)}
            else:
                print(f"⚠️  Visual snapshot test had issues:")
                print(f"   stderr: {result.stderr}")
                return {'status': 'partial', 'error': result.stderr}
                
        except subprocess.TimeoutExpired:
            print("⚠️  Visual snapshot test timed out")
            return {'status': 'timeout'}
        except Exception as e:
            print(f"❌ Visual snapshot test failed: {e}")
            return {'status': 'failed', 'error': str(e)}
    
    def test_enhanced_visuals(self) -> dict:
        """Test enhanced visual engine"""
        print("\n🎨 Testing Enhanced Visual Engine...")
        
        enhanced_engine = Path("enhanced_visual_engine.py")
        if not enhanced_engine.exists():
            print("❌ Enhanced visual engine not found")
            return {'status': 'missing', 'component': 'enhanced_visual_engine.py'}
        
        # Create enhanced snapshots directory
        if not self.snapshots_dir.exists():
            self.snapshots_dir.mkdir(parents=True, exist_ok=True)
            print("📁 Created enhanced snapshots directory")
        
        # Test enhanced generation
        try:
            print("🧪 Testing enhanced snapshot generation...")
            result = subprocess.run([
                sys.executable, "enhanced_visual_engine.py", 
                "--snapshot-now", "--simulate-data"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                # Count generated files
                enhanced_files = list(self.snapshots_dir.glob("*"))
                print(f"✅ Enhanced visual engine test successful")
                print(f"📊 Generated {len(enhanced_files)} enhanced files")
                return {'status': 'working', 'enhanced_files': len(enhanced_files)}
            else:
                print(f"⚠️  Enhanced visual test had issues:")
                print(f"   stderr: {result.stderr}")
                return {'status': 'partial', 'error': result.stderr}
                
        except subprocess.TimeoutExpired:
            print("⚠️  Enhanced visual test timed out")
            return {'status': 'timeout'}
        except Exception as e:
            print(f"❌ Enhanced visual test failed: {e}")
            return {'status': 'failed', 'error': str(e)}
    
    def test_live_data_flow(self) -> dict:
        """Test live data flow from backend to frontend"""
        print("\n🔄 Testing Live Data Flow...")
        
        # Check for recent tick state files
        tick_files = list(self.runtime_dir.glob("tick_state.json")) + \
                    list(self.runtime_dir.glob("*consciousness*.json"))
        
        if not tick_files:
            print("⚠️  No tick state files found")
            return {'status': 'no_data'}
        
        recent_files = []
        for tick_file in tick_files:
            try:
                stat = tick_file.stat()
                age_seconds = time.time() - stat.st_mtime
                
                if age_seconds < 300:  # Modified within 5 minutes
                    recent_files.append({
                        'name': tick_file.name,
                        'age_seconds': age_seconds
                    })
                    
                    # Try to read the file
                    with open(tick_file, 'r') as f:
                        data = json.load(f)
                        print(f"✅ {tick_file.name}: Fresh data (tick {data.get('tick', 'unknown')})")
                        
            except Exception as e:
                print(f"⚠️  Could not read {tick_file}: {e}")
        
        if recent_files:
            return {'status': 'active', 'recent_files': recent_files}
        else:
            print("⚠️  No recently updated data files found")
            return {'status': 'stale'}
    
    def generate_test_report(self, results: dict):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("📋 DAWN CONNECTION TEST REPORT")
        print("=" * 60)
        
        # Overall status
        working_systems = sum(1 for r in results.values() if r.get('status') in ['working', 'running', 'found', 'active'])
        total_systems = len(results)
        
        print(f"🎯 Overall Status: {working_systems}/{total_systems} systems operational")
        
        # Detailed status
        status_icons = {
            'working': '✅', 'running': '✅', 'found': '✅', 'active': '✅',
            'not_running': '⚠️ ', 'missing': '❌', 'partial': '⚠️ ', 
            'stale': '⚠️ ', 'timeout': '⚠️ ', 'failed': '❌', 'error': '❌'
        }
        
        print("\n📊 System Status:")
        for system, result in results.items():
            status = result.get('status', 'unknown')
            icon = status_icons.get(status, '❓')
            print(f"   {icon} {system.replace('_', ' ').title()}: {status}")
        
        # Connection assessment
        print("\n🔗 Connection Assessment:")
        
        backend_ok = results.get('backend', {}).get('status') == 'running'
        mmap_ok = results.get('mmap', {}).get('status') == 'found'
        tauri_available = results.get('tauri', {}).get('gui_found', False)
        
        if backend_ok and mmap_ok:
            print("✅ Backend → Memory-mapped files: CONNECTED")
        else:
            print("❌ Backend → Memory-mapped files: DISCONNECTED")
        
        if mmap_ok and tauri_available:
            print("✅ Memory-mapped files → Tauri GUI: READY") 
        else:
            print("⚠️  Memory-mapped files → Tauri GUI: CHECK REQUIRED")
        
        if results.get('visuals', {}).get('status') == 'working':
            print("✅ Visual snapshot system: WORKING")
        else:
            print("⚠️  Visual snapshot system: NEEDS ATTENTION")
        
        # Recommendations
        print("\n💡 Recommendations:")
        
        if not backend_ok:
            print("   🚀 Start DAWN backend: python launch_dawn.py")
        
        if tauri_available and results.get('tauri', {}).get('status') != 'running':
            print("   🖥️  Start GUI: cd dawn-consciousness-gui && npm run tauri dev")
        
        if results.get('enhanced_visuals', {}).get('status') == 'working':
            print("   🎨 Enhanced visuals ready! Use --visual-snapshots for rich snapshots")
        
        # Export report
        report_file = self.runtime_dir / f"connection_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'results': results,
                'summary': {
                    'working_systems': working_systems,
                    'total_systems': total_systems,
                    'overall_health': 'good' if working_systems >= total_systems * 0.8 else 'needs_attention'
                }
            }, f, indent=2)
        
        print(f"\n📄 Full report saved: {report_file}")

def main():
    """Main CLI interface"""
    tester = DAWNConnectionTester()
    results = tester.run_comprehensive_test()
    
    # Exit with status code based on results
    working_systems = sum(1 for r in results.values() if r.get('status') in ['working', 'running', 'found', 'active'])
    total_systems = len(results)
    
    if working_systems >= total_systems * 0.8:
        print("\n🎉 DAWN system health: EXCELLENT")
        sys.exit(0)
    elif working_systems >= total_systems * 0.5:
        print("\n⚠️  DAWN system health: GOOD (some issues)")
        sys.exit(1)
    else:
        print("\n❌ DAWN system health: NEEDS ATTENTION")
        sys.exit(2)

if __name__ == "__main__":
    main() 