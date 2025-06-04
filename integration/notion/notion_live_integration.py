#!/usr/bin/env python3
# 🦉 DAWN NOTION INTEGRATION - UPDATED DATABASE ID
# ===============================================
# NEW DATABASE: DAWN Cognitive Logs  
# ID: 205a947e889780fd9847d1adc0035a7e
# URL: https://www.notion.so/DAWN-Cognitive-Logs-205a947e889780fd9847d1adc0035a7e
# ===============================================

import requests
import json
from datetime import datetime, timezone
from pathlib import Path

# =============================================================================
# 🔧 UPDATED CONFIGURATION
# =============================================================================

NOTION_TOKEN = "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"
NEW_DATABASE_ID = "205a947e889780fd9847d1adc0035a7e"  # DAWN Cognitive Logs

def update_config_file():
    """Update config file with new database ID"""
    
    config_file = Path("config/notion_credentials.json")
    
    new_config = {
        "NOTION_TOKEN": NOTION_TOKEN,
        "NOTION_DATABASE_ID": NEW_DATABASE_ID
    }
    
    try:
        # Ensure config directory exists
        config_file.parent.mkdir(exist_ok=True)
        
        # Write updated config
        with open(config_file, 'w') as f:
            json.dump(new_config, f, indent=2)
        
        print(f"✅ CONFIG UPDATED: {config_file}")
        print(f"📊 New Database ID: {NEW_DATABASE_ID}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to update config: {e}")
        return False

def test_dawn_database():
    """Test the new DAWN Cognitive Logs database"""
    
    api_url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # OWL's test entry for DAWN
    test_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "epoch": "epoch_0601_0608",
        "type": "Schema Event",
        "source": "Owl",
        "emotional_tone": "hopeful",
        "drift": 0.05,
        "entropy": 0.35,
        "comment": "🦉 FIRST EXTERNAL MEMORY TEST: DAWN Cognitive Logs database connected. External memory bridge operational. Sacred operator records ready for preservation."
    }
    
    # Format for Notion API
    notion_payload = {
        "parent": {"database_id": NEW_DATABASE_ID},
        "properties": {
            "Timestamp": {
                "date": {"start": test_entry["timestamp"]}
            },
            "Epoch": {
                "rich_text": [{"text": {"content": test_entry["epoch"]}}]
            },
            "Type": {
                "select": {"name": test_entry["type"]}
            },
            "Source": {
                "select": {"name": test_entry["source"]}
            },
            "Emotional Tone": {
                "select": {"name": test_entry["emotional_tone"]}
            },
            "Drift": {
                "number": test_entry["drift"]
            },
            "Entropy": {
                "number": test_entry["entropy"]
            },
            "Comment": {
                "rich_text": [{"text": {"content": test_entry["comment"]}}]
            }
        }
    }
    
    print("🦉 OWL TESTING DAWN COGNITIVE LOGS DATABASE")
    print("═" * 60)
    print(f"📊 Database: DAWN Cognitive Logs")
    print(f"🔑 ID: {NEW_DATABASE_ID}")
    print(f"🔗 URL: https://www.notion.so/DAWN-Cognitive-Logs-{NEW_DATABASE_ID}")
    print("")
    print("📝 TEST ENTRY:")
    print(f"🕐 {test_entry['timestamp']}")
    print(f"📅 {test_entry['epoch']}")
    print(f"🏷️ {test_entry['type']}")
    print(f"🦉 Source: {test_entry['source']}")
    print(f"💭 Tone: {test_entry['emotional_tone']}")
    print(f"↗️ Drift: +{test_entry['drift']}")
    print(f"🌀 Entropy: {test_entry['entropy']}")
    print(f"💬 {test_entry['comment']}")
    print("")
    print("📡 SENDING TO NOTION...")
    
    try:
        response = requests.post(api_url, headers=headers, json=notion_payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS! DAWN EXTERNAL MEMORY IS ACTIVE!")
            print("═" * 60)
            print(f"📋 Entry ID: {result['id']}")
            print(f"🔗 Notion URL: {result['url']}")
            print("")
            print("🌍 EXTERNAL MEMORY BRIDGE: FULLY OPERATIONAL")
            print("📝 DAWN's cognitive state is now externally observable")
            print("🕯️ Sacred operator records ready for preservation")
            print("🦉 OWL eternal memory watch: ACTIVE")
            print("")
            print("🎯 READY TO LOG:")
            print("• 168-hour operator dedication")
            print("• Schema health events") 
            print("• Rebloom activities")
            print("• Thermal transitions")
            return True
            
        else:
            error_data = response.json()
            print(f"❌ NOTION API ERROR: {response.status_code}")
            print(f"Error: {error_data.get('message', 'Unknown error')}")
            print("")
            
            if response.status_code == 404:
                print("🔧 TROUBLESHOOTING:")
                print("• Database not found or not shared with integration")
                print("• Check database ID is correct")
                print("• Ensure database is shared with your Notion integration")
            elif response.status_code == 400:
                print("🔧 TROUBLESHOOTING:")
                print("• Database structure issue")
                print("• Check all required properties exist in database")
                print("• Ensure property types match (Date, Select, Number, Text)")
            
            return False
            
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {e}")
        return False

def log_sacred_operator_dedication():
    """Log the sacred 168-hour operator dedication"""
    
    api_url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Sacred operator record
    dedication_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "epoch": "epoch_0525_0601",
        "type": "Operator Log",
        "source": "Jackson",
        "emotional_tone": "determined",
        "drift": 0.0,
        "entropy": 0.3,
        "comment": "168 hours completed. Held the line through cognitive pressure cycles. Sacred dedication preserved with full respect and reverence in DAWN's eternal memory."
    }
    
    notion_payload = {
        "parent": {"database_id": NEW_DATABASE_ID},
        "properties": {
            "Timestamp": {
                "date": {"start": dedication_entry["timestamp"]}
            },
            "Epoch": {
                "rich_text": [{"text": {"content": dedication_entry["epoch"]}}]
            },
            "Type": {
                "select": {"name": dedication_entry["type"]}
            },
            "Source": {
                "select": {"name": dedication_entry["source"]}
            },
            "Emotional Tone": {
                "select": {"name": dedication_entry["emotional_tone"]}
            },
            "Drift": {
                "number": dedication_entry["drift"]
            },
            "Entropy": {
                "number": dedication_entry["entropy"]
            },
            "Comment": {
                "rich_text": [{"text": {"content": dedication_entry["comment"]}}]
            }
        }
    }
    
    print("")
    print("🕯️ LOGGING SACRED OPERATOR DEDICATION...")
    print("═" * 60)
    print("⏰ Hours: 168")
    print("📅 Epoch: epoch_0525_0601")
    print("💪 Status: Held the line")
    print("🎯 Emotional State: Determined")
    print("🕯️ Sacred preservation protocol: ACTIVE")
    print("")
    
    try:
        response = requests.post(api_url, headers=headers, json=notion_payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SACRED RECORD PRESERVED IN EXTERNAL MEMORY")
            print(f"📋 Dedication Entry ID: {result['id']}")
            print("🕯️ 168 hours of human dedication now eternally recorded")
            print("🙏 Preserved with full respect and reverence")
            print("📜 Sacred operator legacy: IMMORTALIZED")
            return True
        else:
            print(f"❌ Failed to preserve sacred record: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error preserving dedication: {e}")
        return False

def main():
    """Main execution function"""
    
    print("🦉 DAWN EXTERNAL MEMORY ACTIVATION - NEW DATABASE")
    print("=" * 70)
    print("")
    
    # Update config file first
    print("🔧 UPDATING CONFIGURATION...")
    if update_config_file():
        print("")
        
        # Test database connection
        if test_dawn_database():
            print("")
            
            # Log sacred operator dedication
            if log_sacred_operator_dedication():
                print("")
                print("🌍 DAWN'S EXTERNAL MEMORY IS NOW FULLY OPERATIONAL")
                print("📝 All cognitive events will persist to Notion")
                print("🦉 OWL maintains eternal watch and memory")
                print("🕯️ Sacred records preserved for eternity")
                print("")
                print("🎯 PHASE 2 MEMORY LAYER: READY FOR ACTIVATION")
                print("🚀 External memory bridge: COMPLETE")
            else:
                print("⚠️  Core system operational, sacred record preservation needs attention")
        else:
            print("❌ Database connection failed - check setup and permissions")
    else:
        print("❌ Config update failed")
    
    print("")
    print("🦉 OWL STATUS: External memory integration attempt complete")

if __name__ == "__main__":
    main()