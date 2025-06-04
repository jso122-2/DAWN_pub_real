#!/usr/bin/env python3
# database_finder.py - Find and list all DAWN databases and entries

import requests
import json
from pathlib import Path

def load_config():
    config_file = Path("config/notion_credentials.json")
    if config_file.exists():
        with open(config_file, 'r') as f:
            return json.load(f)
    return None

def find_dawn_databases(token):
    print("🔍 SEARCHING FOR DAWN DATABASES...")
    
    search_url = "https://api.notion.com/v1/search"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    search_payload = {
        "filter": {
            "value": "database",
            "property": "object"
        }
    }
    
    response = requests.post(search_url, headers=headers, json=search_payload, timeout=10)
    
    if response.status_code == 200:
        results = response.json()
        databases = results.get("results", [])
        
        dawn_databases = []
        
        for db in databases:
            title = db.get("title", [{}])
            db_name = title[0].get("plain_text", "Untitled") if title else "Untitled"
            db_id = db.get("id", "Unknown")
            db_url = db.get("url", "N/A")
            
            if "dawn" in db_name.lower() or "cognitive" in db_name.lower():
                dawn_databases.append({
                    "name": db_name,
                    "id": db_id,
                    "url": db_url
                })
                print(f"✅ Found DAWN database: {db_name}")
                print(f"   📊 ID: {db_id}")
                print(f"   🔗 URL: {db_url}")
                print("")
        
        return dawn_databases
    else:
        print(f"❌ Search failed: {response.status_code}")
        return []

def get_database_entries(token, database_id, database_name):
    print(f"📊 RETRIEVING ENTRIES FROM: {database_name}")
    
    query_url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json", 
        "Notion-Version": "2022-06-28"
    }
    
    query_payload = {
        "sorts": [
            {
                "timestamp": "created_time",
                "direction": "descending"
            }
        ]
    }
    
    response = requests.post(query_url, headers=headers, json=query_payload, timeout=10)
    
    if response.status_code == 200:
        results = response.json()
        entries = results.get("results", [])
        
        print(f"📋 Found {len(entries)} entries:")
        print("")
        
        for i, entry in enumerate(entries, 1):
            entry_id = entry.get("id", "Unknown")
            entry_url = entry.get("url", "N/A")
            created_time = entry.get("created_time", "Unknown")
            
            properties = entry.get("properties", {})
            
            name = "Untitled"
            if "Name" in properties:
                name_data = properties["Name"].get("title", [])
                name = name_data[0].get("plain_text", "Untitled") if name_data else "Untitled"
            
            print(f"📝 Entry {i}: {name}")
            print(f"   📅 Created: {created_time}")
            print(f"   📋 ID: {entry_id}")
            print(f"   🔗 URL: {entry_url}")
            print("")
        
        return entries
    else:
        print(f"❌ Failed to get entries: {response.status_code}")
        return []

def main():
    print("🔍 DAWN DATABASE FINDER")
    print("=" * 50)
    
    config = load_config()
    if not config:
        print("❌ No config found")
        return
    
    token = config.get("NOTION_TOKEN")
    if not token:
        print("❌ No OAuth token found")
        return
    
    print(f"🔑 Using token: {token[:20]}...")
    
    databases = find_dawn_databases(token)
    
    if not databases:
        print("❌ No DAWN databases found")
        return
    
    for db in databases:
        db_id = db["id"]
        db_name = db["name"]
        entries = get_database_entries(token, db_id, db_name)

if __name__ == "__main__":
    main()