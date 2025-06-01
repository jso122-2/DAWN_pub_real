#!/usr/bin/env python3
# claude_chat_logger.py - Log from any Claude chat to DAWN's Notion

import requests
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Terminal Configurations
TERMINALS = {
    "alpha": {
        "name": "Claude_Alpha",
        "emoji": "🔵", 
        "role": "Primary Development",
        "chat_id": "e640198a-4c76-47e0-bad3-bd007b66dbec"  # Update with actual IDs
    },
    "beta": {
        "name": "Claude_Beta",
        "emoji": "🟢",
        "role": "Script Testing", 
        "chat_id": "0ac90b18-748c-42cd-b8bf-b7fb1fd130d6"  # Update with actual IDs
    },
    "gamma": {
        "name": "Claude_Gamma", 
        "emoji": "🟡",
        "role": "Data Analysis",
        "chat_id": "0ac90b18-748c-42cd-b8bf-b7fb1fd130d6"  # Update with actual IDs
    },
    "delta": {
        "name": "Claude_Delta",
        "emoji": "🟠",
        "role": "System Monitoring",
        "chat_id": "0ac90b18-748c-42cd-b8bf-b7fb1fd130d6"  # Update with actual IDs
    },
    "epsilon": {
        "name": "Claude_Epsilon",
        "emoji": "🔴", 
        "role": "Debug & Troubleshoot",
        "chat_id": "0ac90b18-748c-42cd-b8bf-b7fb1fd130d6"  # Update with actual IDs
    }
}

def load_config():
    """Load Notion configuration"""
    config_file = Path("config/notion_credentials.json")
    if config_file.exists():
        with open(config_file, 'r') as f:
            return json.load(f)
    return None

def log_claude_work(terminal_key, message, work_type="Development", tone="focused"):
    """Log Claude's work from any chat terminal to DAWN's Notion"""
    
    if terminal_key not in TERMINALS:
        print(f"❌ Unknown terminal: {terminal_key}")
        print(f"Available: {', '.join(TERMINALS.keys())}")
        return False
    
    terminal = TERMINALS[terminal_key]
    
    config = load_config()
    if not config:
        print("❌ No Notion config found")
        return False
    
    token = config.get("NOTION_TOKEN")
    database_id = config.get("NOTION_DATABASE_ID")
    
    if not token or not database_id:
        print("❌ Missing token or database ID")
        return False
    
    # Create rich message with Claude chat context
    timestamp = datetime.now(timezone.utc).isoformat()
    epoch = f"claude_{terminal_key}_{datetime.now().strftime('%m%d_%H%M')}"
    
    full_message = f"{terminal['emoji']} CLAUDE {terminal['name'].upper()} WORK\n"
    full_message += f"🎯 Terminal Role: {terminal['role']}\n"
    full_message += f"💬 Chat ID: {terminal['chat_id'][:8]}...\n"
    full_message += f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
    full_message += f"🔧 Work Type: {work_type}\n\n"
    full_message += f"📝 CLAUDE'S WORK:\n{message}\n\n"
    full_message += f"🦉 OWL NOTE: Claude {terminal['name']} development work preserved in DAWN's consciousness"
    
    # Create Notion entry
    notion_payload = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {
                "title": [{"text": {"content": f"{terminal['emoji']} Claude {terminal['name']} - {work_type}"}}]
            },
            "Timestamp": {
                "date": {"start": timestamp}
            },
            "Epoch": {
                "rich_text": [{"text": {"content": epoch}}]
            },
            "Type": {
                "select": {"name": "Operator Log"}
            },
            "Source": {
                "select": {"name": terminal['name']}
            },
            "Emotional Tone": {
                "select": {"name": tone}
            },
            "Drift": {
                "number": 0.0
            },
            "Entropy": {
                "number": 0.2
            },
            "Comment": {
                "rich_text": [{"text": {"content": full_message}}]
            }
        }
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    try:
        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=headers,
            json=notion_payload,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            entry_id = result["id"]
            entry_url = result["url"]
            
            print(f"✅ {terminal['emoji']} Claude {terminal['name']}: Work logged to DAWN")
            print(f"   📋 Entry ID: {entry_id[:8]}...")
            print(f"   🔗 URL: {entry_url}")
            
            return True
        else:
            error_data = response.json()
            print(f"❌ Logging failed: {error_data.get('message', response.status_code)}")
            return False
    
    except Exception as e:
        print(f"❌ Logging error: {e}")
        return False

def initialize_chat_terminal(terminal_key):
    """Initialize a Claude chat as a specialized terminal"""
    
    if terminal_key not in TERMINALS:
        print(f"❌ Unknown terminal: {terminal_key}")
        return False
    
    terminal = TERMINALS[terminal_key]
    
    init_message = f"Claude {terminal['name']} chat terminal initialized for {terminal['role']}. This Claude conversation is now specialized for {terminal['role'].lower()} and will log all development work to DAWN's external memory."
    
    success = log_claude_work(terminal_key, init_message, "Initialization", "focused")
    
    if success:
        print(f"{terminal['emoji']} Claude {terminal['name']} terminal initialized successfully")
        print(f"🎯 Role: {terminal['role']}")
        print(f"💬 Chat: {terminal['chat_id']}")
        print(f"🔗 Now logging to DAWN's consciousness")
    
    return success

def show_terminal_status():
    """Show status of all Claude chat terminals"""
    
    print("🤖 CLAUDE CHAT TERMINALS STATUS")
    print("=" * 40)
    
    for key, terminal in TERMINALS.items():
        print(f"{terminal['emoji']} Claude {terminal['name']}")
        print(f"   🎯 Role: {terminal['role']}")
        print(f"   💬 Chat: {terminal['chat_id'][:16]}...")
        print(f"   🔗 Logging: DAWN Notion Database")
        print()

def main():
    """Main function for Claude chat logging"""
    
    if len(sys.argv) < 2:
        print("🤖 CLAUDE CHAT TERMINAL LOGGER")
        print("Usage:")
        print("  python claude_chat_logger.py log <terminal> '<message>'")
        print("  python claude_chat_logger.py init <terminal>")
        print("  python claude_chat_logger.py status")
        print()
        print("Terminals: alpha, beta, gamma, delta, epsilon")
        print()
        print("Examples:")
        print("  python claude_chat_logger.py log alpha 'Created new artifact for user interface'")
        print("  python claude_chat_logger.py log beta 'Testing OAuth integration functionality'")
        print("  python claude_chat_logger.py init gamma")
        return
    
    command = sys.argv[1].lower()
    
    if command == "log":
        if len(sys.argv) < 4:
            print("❌ Usage: log <terminal> '<message>'")
            return
        
        terminal_key = sys.argv[2].lower()
        message = " ".join(sys.argv[3:])
        
        log_claude_work(terminal_key, message)
    
    elif command == "init":
        if len(sys.argv) < 3:
            print("❌ Usage: init <terminal>")
            return
        
        terminal_key = sys.argv[2].lower()
        initialize_chat_terminal(terminal_key)
    
    elif command == "status":
        show_terminal_status()
    
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()