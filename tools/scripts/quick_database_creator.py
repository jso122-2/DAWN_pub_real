#!/usr/bin/env python3
# 🚀 QUICK DATABASE CREATOR
# ========================
# Creates a new DAWN database with OAuth integration
# ========================

import requests
import json
from datetime import datetime, timezone
from pathlib import Path

def load_config():
    """Load OAuth configuration"""
    config_file = Path("config/notion_credentials.json")
    
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Config error: {e}")
    
    return None

def search_for_pages(token):
    """Search for pages where we can create a database"""
    
    print("🔍 Searching for accessible pages...")
    
    search_url = "https://api.notion.com/v1/search"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Search for pages
    search_payload = {
        "filter": {
            "value": "page",
            "property": "object"
        }
    }
    
    try:
        response = requests.post(search_url, headers=headers, json=search_payload, timeout=10)
        
        if response.status_code == 200:
            results = response.json()
            pages = results.get("results", [])
            
            print(f"📄 Found {len(pages)} accessible pages")
            
            # Look for a suitable parent page
            for page in pages:
                title = page.get("properties", {}).get("title", {}).get("title", [])
                page_title = title[0].get("plain_text", "Untitled") if title else "Untitled"
                page_id = page.get("id")
                
                print(f"  • {page_title} ({page_id})")
                
                # Return first accessible page as parent
                if page_id:
                    return page_id
            
            return None
        else:
            print(f"❌ Search failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Search error: {e}")
        return None

def create_dawn_database_in_page(token, parent_page_id):
    """Create DAWN database in an existing page"""
    
    print(f"🏗️ Creating DAWN database in page: {parent_page_id}")
    
    create_db_url = "https://api.notion.com/v1/databases"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Database structure
    database_payload = {
        "parent": {
            "type": "page_id",
            "page_id": parent_page_id
        },
        "title": [
            {
                "type": "text",
                "text": {
                    "content": "DAWN Cognitive Logs"
                }
            }
        ],
        "properties": {
            "Name": {
                "title": {}
            },
            "Timestamp": {
                "date": {}
            },
            "Epoch": {
                "rich_text": {}
            },
            "Type": {
                "select": {
                    "options": [
                        {"name": "Rebloom", "color": "green"},
                        {"name": "Schema Event", "color": "blue"},
                        {"name": "Operator Log", "color": "orange"},
                        {"name": "Thermal", "color": "red"},
                        {"name": "Drift", "color": "purple"}
                    ]
                }
            },
            "Source": {
                "select": {
                    "options": [
                        {"name": "Owl", "color": "brown"},
                        {"name": "Jackson", "color": "blue"},
                        {"name": "Pulse", "color": "green"},
                        {"name": "Sigil_Pipeline", "color": "purple"},
                        {"name": "Terminal", "color": "gray"}
                    ]
                }
            },
            "Emotional Tone": {
                "select": {
                    "options": [
                        {"name": "hopeful", "color": "green"},
                        {"name": "focused", "color": "blue"},
                        {"name": "wavering", "color": "yellow"},
                        {"name": "concerned", "color": "orange"},
                        {"name": "lucid", "color": "purple"},
                        {"name": "grateful", "color": "pink"},
                        {"name": "determined", "color": "red"},
                        {"name": "accomplished", "color": "default"}
                    ]
                }
            },
            "Drift": {
                "number": {
                    "format": "number"
                }
            },
            "Entropy": {
                "number": {
                    "format": "number"
                }
            },
            "Comment": {
                "rich_text": {}
            }
        }
    }
    
    try:
        response = requests.post(create_db_url, headers=headers, json=database_payload, timeout=15)
        
        if response.status_code == 200:
            db_result = response.json()
            db_id = db_result["id"]
            db_url = db_result["url"]
            
            print("✅ DAWN DATABASE CREATED SUCCESSFULLY!")
            print(f"📊 Database ID: {db_id}")
            print(f"🔗 Database URL: {db_url}")
            
            # Update config
            update_config_with_new_db(db_id)
            
            # Test the new database
            test_new_database(token, db_id)
            
            return db_id
            
        else:
            error_data = response.json()
            print(f"❌ Database creation failed: {response.status_code}")
            print(f"Error: {error_data.get('message', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"❌ Database creation error: {e}")
        return None

def update_config_with_new_db(database_id):
    """Update config file with new database ID"""
    
    config_file = Path("config/notion_credentials.json")
    
    try:
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
        else:
            config = {}
        
        config["NOTION_DATABASE_ID"] = database_id
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Config updated with new database ID")
        
    except Exception as e:
        print(f"❌ Config update error: {e}")

def test_new_database(token, database_id):
    """Test the newly created database"""
    
    print("🧪 Testing new database...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Create test entry
    test_payload = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {
                "title": [{"text": {"content": "🎯 DAWN External Memory Activated"}}]
            },
            "Timestamp": {
                "date": {"start": datetime.now(timezone.utc).isoformat()}
            },
            "Epoch": {
                "rich_text": [{"text": {"content": "database_creation_success"}}]
            },
            "Type": {
                "select": {"name": "Schema Event"}
            },
            "Source": {
                "select": {"name": "Owl"}
            },
            "Emotional Tone": {
                "select": {"name": "accomplished"}
            },
            "Drift": {
                "number": 0.0
            },
            "Entropy": {
                "number": 0.1
            },
            "Comment": {
                "rich_text": [{"text": {"content": "🦉 DAWN's external memory database successfully created and operational. OAuth integration confirmed. Ready for sacred operator record preservation and dev terminal logging."}}]
            }
        }
    }
    
    try:
        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=headers,
            json=test_payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ DATABASE TEST SUCCESSFUL!")
            print(f"📋 First entry created: {result['id']}")
            print(f"🔗 Entry URL: {result['url']}")
            print("")
            print("🌟 DAWN'S EXTERNAL MEMORY IS NOW FULLY OPERATIONAL!")
            print("📝 Sacred operator records ready for preservation")
            print("🦉 OWL eternal memory watch: ACTIVE")
            return True
        else:
            print(f"❌ Database test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Database test error: {e}")
        return False

def main():
    """Main function to create database"""
    
    print("🚀 QUICK DAWN DATABASE CREATOR")
    print("=" * 50)
    print()
    
    # Load config
    config = load_config()
    if not config:
        print("❌ No OAuth config found - run OAuth flow first")
        return
    
    token = config.get("NOTION_TOKEN")
    if not token:
        print("❌ No OAuth token found")
        return
    
    print(f"🔑 Using OAuth token: {token[:20]}...")
    print("👤 Integration: DAWN Memory Logger")
    print()
    
    # Search for accessible pages
    parent_page_id = search_for_pages(token)
    
    if not parent_page_id:
        print("❌ No accessible pages found")
        print("🔧 Try creating a page manually in Notion first")
        return
    
    # Create database
    new_db_id = create_dawn_database_in_page(token, parent_page_id)
    
    if new_db_id:
        print("")
        print("🎯 DATABASE CREATION COMPLETE!")
        print("🚀 Next steps:")
        print("  1. Database is automatically shared with OAuth integration")
        print("  2. Run your personal note script: python dawn_personal_note.py")
        print("  3. Set up dev terminal logging")
        print("")
        print("🦉 OWL Status: New database operational and ready")
    else:
        print("❌ Database creation failed")
        print("🔧 Manual database creation may be required")

if __name__ == "__main__":
    main()