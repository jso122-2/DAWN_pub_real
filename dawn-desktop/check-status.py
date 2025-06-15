#!/usr/bin/env python3
"""
DAWN System Status Checker
Verifies that both backend and frontend services are running properly
"""

import requests
import socket
import json
from datetime import datetime

def check_port(host, port):
    """Check if a port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def check_backend():
    """Check DAWN backend status"""
    print("🧠 Checking DAWN Backend (Port 8000)...")
    
    if not check_port('localhost', 8000):
        print("❌ Backend not responding on port 8000")
        return False
    
    try:
        # Try to get status from the API - try both root and status endpoints
        for endpoint in ['/', '/status']:
            try:
                response = requests.get(f'http://localhost:8000{endpoint}', timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Backend online - Endpoint: {endpoint}")
                    if 'tick' in data:
                        print(f"   Tick: {data.get('tick', 'N/A')}")
                    if 'consciousness' in data:
                        consciousness = data['consciousness']
                        print(f"   SCUP: {consciousness.get('scup', 'N/A')}%")
                        print(f"   Mood: {consciousness.get('mood', 'N/A')}")
                    if 'service' in data:
                        print(f"   Service: {data.get('service', 'Unknown')}")
                    return True
            except:
                continue
        
        print(f"⚠️ Backend responding but no valid endpoints found")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend API error: {e}")
        return False

def check_frontend():
    """Check React frontend status"""
    print("\n🌐 Checking React Frontend (Port 3000)...")
    
    if not check_port('localhost', 3000):
        print("❌ Frontend not responding on port 3000")
        return False
    
    try:
        # Try to get the main page
        response = requests.get('http://localhost:3000/', timeout=5)
        if response.status_code == 200:
            print("✅ Frontend online and serving content")
            return True
        else:
            print(f"⚠️ Frontend responding but returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend error: {e}")
        return False

def check_websocket():
    """Check WebSocket connectivity"""
    print("\n🔌 Checking WebSocket Connection...")
    
    # Just check if the port is open for WebSocket
    if check_port('localhost', 8000):
        print("✅ WebSocket port (8000) is accessible")
        return True
    else:
        print("❌ WebSocket port (8000) not accessible")
        return False

def main():
    print("=" * 50)
    print("🚀 DAWN System Status Check")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    backend_ok = check_backend()
    frontend_ok = check_frontend()
    websocket_ok = check_websocket()
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    if backend_ok and frontend_ok and websocket_ok:
        print("🎉 All systems operational!")
        print("\n🌐 Access Points:")
        print("   • Dashboard: http://localhost:3000/dashboard")
        print("   • Backend API: http://localhost:8000/")
        print("   • WebSocket: ws://localhost:8000/ws")
        return 0
    else:
        print("⚠️ Some systems are not responding:")
        if not backend_ok:
            print("   • Backend (Port 8000) - Run: python start-dawn.py")
        if not frontend_ok:
            print("   • Frontend (Port 3000) - Run: npm run dev")
        if not websocket_ok:
            print("   • WebSocket connection issues")
        return 1

if __name__ == "__main__":
    exit(main()) 