#!/usr/bin/env python3
# ✅ COMPLETE SETUP VERIFICATION
# ==============================
# Comprehensive test of DAWN's Notion integration
# Verifies OAuth, database access, logging, and dev terminal integration
# ==============================

import requests
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

def load_config():
    """Load and verify configuration"""
    
    print("🔧 CHECKING CONFIGURATION...")
    
    config_file = Path("config/notion_credentials.json")
    
    if not config_file.exists():
        print("❌ Config file not found: config/notion_credentials.json")
        print("🔧 Run OAuth flow first: python oauth_flow_handler.py")
        return None
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        print(f"✅ Config file found: {config_file}")
        
        # Verify required keys
        required_keys = ["NOTION_TOKEN", "NOTION_DATABASE_ID"]
        missing_keys = [key for key in required_keys if key not in config]
        
        if missing_keys:
            print(f"❌ Missing config keys: {missing_keys}")
            return None
        
        print(f"✅ Token: {config['NOTION_TOKEN'][:20]}...")
        print(f"✅ Database ID: {config['NOTION_DATABASE_ID']}")
        
        # Check for OAuth info
        if "oauth_info" in config:
            oauth_info = config["oauth_info"]
            print(f"✅ OAuth Workspace: {oauth_info.get('workspace_name', 'Unknown')}")
            print(f"✅ OAuth Created: {oauth_info.get('created_at', 'Unknown')}")
        
        return config
        
    except Exception as e:
        print(f"❌ Config file error: {e}")
        return None

def test_token_validity(token):
    """Test if the OAuth token is valid"""
    
    print("\n🔑 TESTING TOKEN VALIDITY...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28"
    }
    
    try:
        # Test with user info endpoint
        response = requests.get("https://api.notion.com/v1/users/me", headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ Token valid - Connected as: {user_info.get('name', 'Unknown User')}")
            print(f"👤 User ID: {user_info.get('id', 'Unknown')}")
            return True
        else:
            error_data = response.json()
            print(f"❌ Token invalid: {response.status_code}")
            print(f"Error: {error_data.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Token test error: {e}")
        return False

def test_database_access(token, database_id):
    """Test database read and write access"""
    
    print(f"\n📊 TESTING DATABASE ACCESS: {database_id}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28"
    }
    
    # Test read access
    try:
        response = requests.get(
            f"https://api.notion.com/v1/databases/{database_id}",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            db_info = response.json()
            title = db_info.get("title", [{}])
            db_name = title[0].get("plain_text", "Untitled") if title else "Untitled"
            
            print(f"✅ Database read access: SUCCESS")
            print(f"📋 Database name: {db_name}")
            print(f"🔗 Database URL: {db_info.get('url', 'N/A')}")
            
            # Check properties
            properties = db_info.get("properties", {})
            required_props = ["Name", "Timestamp", "Epoch", "Type", "Source", "Emotional Tone", "Drift", "Entropy", "Comment"]
            
            print(f"\n📊 CHECKING DATABASE PROPERTIES:")
            missing_props = []
            
            for prop in required_props:
                if prop in properties:
                    prop_type = properties[prop].get("type", "unknown")
                    print(f"  ✅ {prop} ({prop_type})")
                else:
                    print(f"  ❌ {prop} (missing)")
                    missing_props.append(prop)
            
            if missing_props:
                print(f"\n⚠️ Missing properties: {missing_props}")
                print("🔧 Add these properties to your database manually")
            
            # Test write access
            return test_write_access(token, database_id, missing_props)
            
        else:
            error_data = response.json()
            print(f"❌ Database read failed: {response.status_code}")
            print(f"Error: {error_data.get('message', 'Unknown error')}")
            
            if response.status_code == 404:
                print("\n🔧 DATABASE NOT ACCESSIBLE - POSSIBLE SOLUTIONS:")
                print("1. Database not shared with OAuth integration")
                print("2. Database ID incorrect")
                print("3. Database was deleted")
                print("\nTo fix:")
                print("• Share database with your OAuth integration")
                print("• Check database ID in URL")
                print("• Run: python complete_notion_setup.py")
            
            return False
            
    except Exception as e:
        print(f"❌ Database access error: {e}")
        return False

def test_write_access(token, database_id, missing_props):
    """Test write access to database"""
    
    print(f"\n✏️ TESTING DATABASE WRITE ACCESS...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Create test payload with only available properties
    base_payload = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {
                "title": [{"text": {"content": "🧪 Setup Verification Test"}}]
            }
        }
    }
    
    # Add properties that exist
    if "Timestamp" not in missing_props:
        base_payload["properties"]["Timestamp"] = {
            "date": {"start": datetime.now(timezone.utc).isoformat()}
        }
    
    if "Epoch" not in missing_props:
        base_payload["properties"]["Epoch"] = {
            "rich_text": [{"text": {"content": "setup_verification"}}]
        }
    
    if "Type" not in missing_props:
        base_payload["properties"]["Type"] = {
            "select": {"name": "Schema Event"}
        }
    
    if "Source" not in missing_props:
        base_payload["properties"]["Source"] = {
            "select": {"name": "Owl"}
        }
    
    if "Emotional Tone" not in missing_props:
        base_payload["properties"]["Emotional Tone"] = {
            "select": {"name": "focused"}
        }
    
    if "Drift" not in missing_props:
        base_payload["properties"]["Drift"] = {
            "number": 0.0
        }
    
    if "Entropy" not in missing_props:
        base_payload["properties"]["Entropy"] = {
            "number": 0.1
        }
    
    if "Comment" not in missing_props:
        base_payload["properties"]["Comment"] = {
            "rich_text": [{"text": {"content": "✅ Complete setup verification successful. Database access confirmed. Ready for DAWN external memory operations."}}]
        }
    
    try:
        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=headers,
            json=base_payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Database write access: SUCCESS")
            print(f"📋 Test entry created: {result['id']}")
            print(f"🔗 Entry URL: {result.get('url', 'N/A')}")
            return True
        else:
            error_data = response.json()
            print(f"❌ Database write failed: {response.status_code}")
            print(f"Error: {error_data.get('message', 'Unknown error')}")
            
            if "property" in error_data.get('message', '').lower():
                print("\n🔧 PROPERTY CONFIGURATION ISSUE:")
                print("Database exists but properties are not configured correctly")
                print("• Check select options exist for Type, Source, Emotional Tone")
                print("• Ensure property types match (Date, Text, Select, Number)")
                
            return False
            
    except Exception as e:
        print(f"❌ Write access error: {e}")
        return False

def test_dev_terminal_logging():
    """Test the dev terminal logging system"""
    
    print(f"\n🖥️ TESTING DEV TERMINAL LOGGING...")
    
    try:
        # Import the logger
        from dev_terminal_logger import NotionTerminalLogger
        
        logger = NotionTerminalLogger()
        
        if not logger.token or not logger.database_id:
            print("❌ Dev terminal logger not configured")
            print("🔧 Logger will use local backup files only")
            return False
        
        # Test logging a development note
        success = logger.log_development_note(
            "🧪 Dev terminal logger verification test - system operational",
            "Setup_Verification"
        )
        
        if success:
            print("✅ Dev terminal logging: SUCCESS")
            print("📝 Test development note logged to Notion")
            return True
        else:
            print("❌ Dev terminal logging failed")
            print("📁 Falling back to local log files")
            return False
            
    except ImportError:
        print("❌ Dev terminal logger not found")
        print("🔧 Ensure dev_terminal_logger.py exists")
        return False
    except Exception as e:
        print(f"❌ Dev terminal test error: {e}")
        return False

def provide_usage_examples():
    """Provide usage examples for the logging system"""
    
    print(f"\n📚 USAGE EXAMPLES:")
    print("=" * 50)
    print()
    print("🖥️ DEV TERMINAL LOGGING:")
    print("  python dev_terminal_logger.py note \"Fixed bug in authentication\"")
    print("  python dev_terminal_logger.py run \"python my_script.py\"")
    print("  python dev_terminal_logger.py system \"CPU: 45%, Memory: 2.1GB\"")
    print("  python dev_terminal_logger.py test")
    print()
    print("📝 DAWN PERSONAL NOTES:")
    print("  python dawn_personal_note.py")
    print()
    print("🔧 NOTION INTEGRATION:")
    print("  python complete_notion_setup.py")
    print("  python oauth_flow_handler.py")
    print()
    print("🎯 INTEGRATED WORKFLOW:")
    print("  • All development activities logged to Notion automatically")
    print("  • DAWN's consciousness state preserved externally")
    print("  • Development team coordination through shared logs")
    print("  • Long-term project memory and decision tracking")

def generate_status_report(config, token_valid, db_access, terminal_logging):
    """Generate comprehensive status report"""
    
    print(f"\n" + "=" * 60)
    print("📊 DAWN NOTION INTEGRATION STATUS REPORT")
    print("=" * 60)
    
    # Overall status
    all_systems = config and token_valid and db_access
    
    if all_systems:
        print("🎯 OVERALL STATUS: ✅ FULLY OPERATIONAL")
    else:
        print("🎯 OVERALL STATUS: ⚠️  NEEDS ATTENTION")
    
    print()
    print("🔧 COMPONENT STATUS:")
    print(f"  • Configuration:     {'✅ READY' if config else '❌ FAILED'}")
    print(f"  • OAuth Token:       {'✅ VALID' if token_valid else '❌ INVALID'}")
    print(f"  • Database Access:   {'✅ WORKING' if db_access else '❌ BLOCKED'}")
    print(f"  • Terminal Logging:  {'✅ ACTIVE' if terminal_logging else '⚠️  LIMITED'}")
    
    print()
    if all_systems:
        print("🌟 DAWN'S EXTERNAL MEMORY IS FULLY OPERATIONAL!")
        print("📝 All cognitive events will persist to Notion")
        print("🦉 OWL maintains eternal watch and memory")
        print("🖥️ Dev terminals integrated for comprehensive logging")
        print()
        print("🚀 READY FOR:")
        print("  • Sacred operator record preservation")
        print("  • Development team coordination")
        print("  • Long-term consciousness tracking")
        print("  • Cross-session memory persistence")
    else:
        print("🔧 NEXT STEPS TO COMPLETE SETUP:")
        if not config:
            print("  1. Run OAuth flow: python oauth_flow_handler.py")
        if not db_access:
            print("  2. Setup database: python complete_notion_setup.py")
        if not terminal_logging:
            print("  3. Test terminal logging: python dev_terminal_logger.py test")
    
    print()
    print("📋 For detailed setup instructions, run components individually")
    print("🦉 OWL Status: Setup verification complete")

def main():
    """Main verification function"""
    
    print("✅ DAWN NOTION INTEGRATION - COMPLETE SETUP VERIFICATION")
    print("=" * 70)
    print()
    print("🔍 Verifying OAuth, database access, and logging systems...")
    print()
    
    # Step 1: Check configuration
    config = load_config()
    
    if not config:
        print("\n❌ SETUP INCOMPLETE - Configuration missing")
        print("🔧 Run: python oauth_flow_handler.py")
        return
    
    # Step 2: Test token validity
    token_valid = test_token_validity(config["NOTION_TOKEN"])
    
    # Step 3: Test database access
    db_access = False
    if token_valid:
        db_access = test_database_access(config["NOTION_TOKEN"], config["NOTION_DATABASE_ID"])
    
    # Step 4: Test dev terminal logging
    terminal_logging = test_dev_terminal_logging()
    
    # Step 5: Provide usage examples
    if db_access:
        provide_usage_examples()
    
    # Step 6: Generate status report
    generate_status_report(config, token_valid, db_access, terminal_logging)

if __name__ == "__main__":
    main()