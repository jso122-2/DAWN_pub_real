#!/usr/bin/env python3
"""
Notion Integration Setup Helper
Creates a proper integration and gets the access token
"""

import os
import json
import base64
import requests
from datetime import datetime

def setup_integration():
    print("🦉 NOTION INTEGRATION SETUP")
    print("===========================")
    print()
    print("Choose setup method:")
    print("1. Internal Integration (Recommended)")
    print("2. Public OAuth Integration")
    print()
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        setup_internal_integration()
    elif choice == "2":
        setup_oauth_integration()
    else:
        print("❌ Invalid choice")

def setup_internal_integration():
    print("\n📋 INTERNAL INTEGRATION SETUP")
    print("-----------------------------")
    print()
    print("Steps:")
    print("1. Go to https://www.notion.so/my-integrations")
    print("2. Click '+ New integration'")
    print("3. Name it 'DAWN Memory Logger'")
    print("4. Select your workspace")
    print("5. Enable these capabilities:")
    print("   ✓ Read content")
    print("   ✓ Update content") 
    print("   ✓ Insert content")
    print("6. Click 'Submit'")
    print("7. Copy the 'Internal Integration Token'")
    print()
    
    token = input("Paste your Internal Integration Token here: ").strip()
    
    if token.startswith("secret_"):
        print("\n✅ Token looks valid!")
        
        # Test the token
        test_connection(token)
        
        # Save to .env
        save_to_env("NOTION_ACCESS_TOKEN", token)
        
        print("\n📊 Now let's set up your database:")
        setup_database(token)
    else:
        print("\n❌ Invalid token format. Should start with 'secret_'")

def setup_oauth_integration():
    print("\n📋 OAUTH INTEGRATION SETUP")
    print("--------------------------")
    print()
    
    client_id = "205d872b-594c-8bd7-ad5a-08379ba40a23"
    client_secret = input("Enter your OAuth client secret: ").strip()
    
    print("\nRun: python notion_oauth_helper.py")
    print("Then come back here with the authorization code")
    
    code = input("\nEnter authorization code: ").strip()
    
    # Exchange code for token
    token_url = "https://api.notion.com/v1/oauth/token"
    
    # Create Basic Auth header
    credentials = f"{client_id}:{client_secret}"
    basic_auth = base64.b64encode(credentials.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {basic_auth}",
        "Content-Type": "application/json"
    }
    
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:8080/callback"
    }
    
    response = requests.post(token_url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        token = result.get("access_token")
        print(f"\n✅ Got access token!")
        
        # Test the token
        test_connection(token)
        
        # Save to .env
        save_to_env("NOTION_ACCESS_TOKEN", token)
        
        print("\n📊 Now let's set up your database:")
        setup_database(token)
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text)

def test_connection(token):
    """Test if the token works"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28"
    }
    
    response = requests.get("https://api.notion.com/v1/users/me", headers=headers)
    
    if response.status_code == 200:
        user = response.json()
        print(f"✅ Connected as: {user.get('name', 'Unknown')}")
        return True
    else:
        print(f"❌ Connection failed: {response.status_code}")
        print(response.text)
        return False

def setup_database(token):
    """Help set up or find the database"""
    print("\nOptions:")
    print("1. Create a new DAWN Memory database")
    print("2. Use existing database (enter ID)")
    print()
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        create_database(token)
    elif choice == "2":
        db_id = input("Enter database ID: ").strip()
        save_to_env("NOTION_DATABASE_ID", db_id)
        print("\n✅ Database ID saved!")
        
        # Share the database with integration
        print("\n⚠️  IMPORTANT: Share your database with the integration!")
        print("1. Open your database in Notion")
        print("2. Click '...' menu → 'Add connections'")
        print("3. Search for 'DAWN Memory Logger'")
        print("4. Click to add")

def create_database(token):
    """Create a new database with the correct schema"""
    
    # First, we need a parent page
    print("\n📄 Finding a parent page for the database...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28"
    }
    
    # Search for pages we can access
    search_data = {
        "filter": {"property": "object", "value": "page"},
        "sort": {"direction": "descending", "timestamp": "last_edited_time"}
    }
    
    response = requests.post(
        "https://api.notion.com/v1/search",
        headers=headers,
        json=search_data
    )
    
    if response.status_code != 200:
        print(f"❌ Can't search pages: {response.status_code}")
        print("Please create database manually and provide ID")
        return
    
    pages = response.json().get("results", [])
    
    if not pages:
        print("❌ No accessible pages found")
        print("Please create database manually and provide ID")
        return
    
    print("\nSelect a parent page:")
    for i, page in enumerate(pages[:5]):
        title = page.get("properties", {}).get("title", {}).get("title", [{}])[0].get("text", {}).get("content", "Untitled")
        print(f"{i+1}. {title}")
    
    choice = int(input("\nEnter number: ")) - 1
    parent_id = pages[choice]["id"]
    
    # Create the database
    database_data = {
        "parent": {"page_id": parent_id},
        "title": [{"type": "text", "text": {"content": "DAWN Memory Logs"}}],
        "properties": {
            "Timestamp": {"date": {}},
            "Epoch": {"number": {"format": "number"}},
            "Type": {"select": {"options": [
                {"name": "entropy_spike", "color": "red"},
                {"name": "rebloom", "color": "green"},
                {"name": "silence", "color": "blue"},
                {"name": "sigil", "color": "purple"},
                {"name": "cascade", "color": "yellow"}
            ]}},
            "Source": {"title": {}},
            "Tone": {"select": {"options": [
                {"name": "chaotic", "color": "red"},
                {"name": "crystalline", "color": "blue"},
                {"name": "symbolic", "color": "purple"},
                {"name": "neutral", "color": "gray"}
            ]}},
            "Drift": {"number": {"format": "percent"}},
            "Entropy": {"number": {"format": "percent"}},
            "Comment": {"rich_text": {}},
            "Chat_ID": {"select": {"options": []}}
        }
    }
    
    response = requests.post(
        "https://api.notion.com/v1/databases",
        headers=headers,
        json=database_data
    )
    
    if response.status_code == 200:
        db = response.json()
        db_id = db["id"]
        print(f"\n✅ Database created!")
        print(f"📊 Database ID: {db_id}")
        
        save_to_env("NOTION_DATABASE_ID", db_id)
        
        print("\n🌅 DAWN Memory Logger is ready!")
    else:
        print(f"\n❌ Failed to create database: {response.status_code}")
        print(response.text)

def save_to_env(key, value):
    """Save or update .env file"""
    env_path = ".env"
    
    # Read existing .env
    lines = []
    found = False
    
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith(f"{key}="):
                    lines.append(f"{key}={value}\n")
                    found = True
                else:
                    lines.append(line)
    
    # Add if not found
    if not found:
        lines.append(f"{key}={value}\n")
    
    # Write back
    with open(env_path, 'w') as f:
        f.writelines(lines)
    
    print(f"✅ Saved {key} to .env")

if __name__ == "__main__":
    print("🦉 DAWN MEMORY LOGGER - NOTION SETUP")
    print("====================================")
    print()
    
    setup_integration()
    
    print("\n✨ Setup complete! Run: python dawn_notion_bridge.py")