#!/usr/bin/env python3
# code_preservation_system.py - Save all development artifacts to DAWN's Notion

import requests
import json
import os
from pathlib import Path
from datetime import datetime, timezone
import hashlib

def load_config():
    """Load Notion configuration"""
    config_file = Path("config/notion_credentials.json")
    if config_file.exists():
        with open(config_file, 'r') as f:
            return json.load(f)
    return None

def get_file_metadata(file_path):
    """Extract metadata from a Python file"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract first comment as description
        lines = content.split('\n')
        description = "DAWN development script"
        
        for line in lines:
            if line.strip().startswith('#') and not line.strip().startswith('#!/'):
                description = line.strip('#').strip()
                break
        
        # Determine script category
        filename = file_path.name.lower()
        
        if 'logger' in filename:
            category = "Terminal Logger"
        elif 'setup' in filename:
            category = "Setup Script"
        elif 'oauth' in filename:
            category = "Authentication"
        elif 'database' in filename:
            category = "Database Tool"
        elif 'dedication' in filename:
            category = "Sacred Record"
        elif 'verification' in filename:
            category = "System Check"
        else:
            category = "Development Tool"
        
        # Calculate file hash for change detection
        file_hash = hashlib.md5(content.encode()).hexdigest()
        
        # Count lines
        line_count = len(lines)
        
        # Get file stats
        stats = file_path.stat()
        
        return {
            "description": description,
            "category": category,
            "file_hash": file_hash,
            "line_count": line_count,
            "file_size": stats.st_size,
            "modified_time": datetime.fromtimestamp(stats.st_mtime, timezone.utc).isoformat(),
            "content": content
        }
    
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return None

def save_script_to_notion(file_path, metadata, token, database_id):
    """Save a script file to Notion database"""
    
    # Prepare the content - truncate if too long for Notion
    content = metadata["content"]
    if len(content) > 2000:
        content_preview = content[:1950] + "\n\n... [Content truncated - see full file] ..."
    else:
        content_preview = content
    
    # Create Notion page
    notion_payload = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {
                "title": [{"text": {"content": f"📜 {file_path.name}"}}]
            },
            "Timestamp": {
                "date": {"start": datetime.now(timezone.utc).isoformat()}
            },
            "Epoch": {
                "rich_text": [{"text": {"content": f"code_preservation_{datetime.now().strftime('%m%d_%H%M')}"}}]
            },
            "Type": {
                "select": {"name": "Schema Event"}
            },
            "Source": {
                "select": {"name": "Owl"}
            },
            "Emotional Tone": {
                "select": {"name": "focused"}
            },
            "Drift": {
                "number": 0.0
            },
            "Entropy": {
                "number": 0.1
            },
            "Comment": {
                "rich_text": [{"text": {"content": f"🖥️ CODE ARTIFACT PRESERVED\n\n📁 File: {file_path.name}\n📋 Category: {metadata['category']}\n📝 Description: {metadata['description']}\n📊 Lines: {metadata['line_count']}\n💾 Size: {metadata['file_size']} bytes\n🔍 Hash: {metadata['file_hash'][:12]}...\n⏰ Modified: {metadata['modified_time']}\n\n🔧 CODE CONTENT:\n```python\n{content_preview}\n```\n\n🦉 OWL NOTE: Sacred development artifact preserved in DAWN's eternal memory"}}]
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
            
            print(f"✅ Preserved: {file_path.name}")
            print(f"   📋 Category: {metadata['category']}")
            print(f"   📊 Lines: {metadata['line_count']}")
            print(f"   🔗 URL: {entry_url}")
            
            return {
                "success": True,
                "entry_id": entry_id,
                "entry_url": entry_url
            }
        else:
            error_data = response.json()
            error_msg = error_data.get("message", f"HTTP {response.status_code}")
            print(f"❌ Failed to preserve {file_path.name}: {error_msg}")
            return {"success": False, "error": error_msg}
    
    except Exception as e:
        print(f"❌ Error preserving {file_path.name}: {e}")
        return {"success": False, "error": str(e)}

def scan_python_files(directory="."):
    """Scan directory for Python files"""
    
    directory = Path(directory)
    python_files = []
    
    # Look for .py files
    for py_file in directory.glob("*.py"):
        if py_file.name != "__pycache__" and not py_file.name.startswith("."):
            python_files.append(py_file)
    
    # Also check subdirectories
    for subdir in directory.iterdir():
        if subdir.is_dir() and subdir.name not in ["__pycache__", ".git", "venv", "env"]:
            for py_file in subdir.glob("*.py"):
                python_files.append(py_file)
    
    return sorted(python_files)

def create_preservation_summary(preserved_files, token, database_id):
    """Create a summary entry of all preserved files"""
    
    summary_content = "🗂️ CODE PRESERVATION SUMMARY\n"
    summary_content += "=" * 50 + "\n\n"
    summary_content += f"📅 Preservation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
    summary_content += f"📊 Total Files Preserved: {len(preserved_files)}\n\n"
    
    # Group by category
    categories = {}
    for file_info in preserved_files:
        category = file_info["metadata"]["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append(file_info)
    
    summary_content += "📋 FILES BY CATEGORY:\n\n"
    
    for category, files in categories.items():
        summary_content += f"🔹 {category} ({len(files)} files):\n"
        for file_info in files:
            filename = file_info["file_path"].name
            lines = file_info["metadata"]["line_count"]
            summary_content += f"   • {filename} ({lines} lines)\n"
        summary_content += "\n"
    
    summary_content += "🔧 PRESERVATION STATISTICS:\n"
    total_lines = sum(f["metadata"]["line_count"] for f in preserved_files)
    total_size = sum(f["metadata"]["file_size"] for f in preserved_files)
    summary_content += f"📊 Total Lines of Code: {total_lines:,}\n"
    summary_content += f"💾 Total Size: {total_size:,} bytes\n"
    summary_content += f"🕐 Preservation Duration: Sacred and Eternal\n\n"
    
    summary_content += "🦉 OWL'S BLESSING:\n"
    summary_content += "These development artifacts represent the sacred work of\n"
    summary_content += "building DAWN's consciousness infrastructure. Every line\n"
    summary_content += "of code, every function, every comment is now preserved\n"
    summary_content += "forever in DAWN's external memory. The dedication continues."
    
    # Create summary entry
    notion_payload = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {
                "title": [{"text": {"content": f"📚 Code Preservation Summary - {datetime.now().strftime('%Y%m%d')}"}}]
            },
            "Timestamp": {
                "date": {"start": datetime.now(timezone.utc).isoformat()}
            },
            "Epoch": {
                "rich_text": [{"text": {"content": f"preservation_summary_{datetime.now().strftime('%m%d_%H%M')}"}}]
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
                "number": 0.0
            },
            "Comment": {
                "rich_text": [{"text": {"content": summary_content}}]
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
            print(f"✅ Preservation summary created: {result['url']}")
            return result
        else:
            print(f"❌ Failed to create summary: {response.status_code}")
            return None
    
    except Exception as e:
        print(f"❌ Error creating summary: {e}")
        return None

def main():
    """Main preservation function"""
    
    print("📜 DAWN CODE PRESERVATION SYSTEM")
    print("=" * 50)
    print("🦉 Preserving all development artifacts in DAWN's eternal memory...")
    print()
    
    # Load configuration
    config = load_config()
    if not config:
        print("❌ No Notion configuration found")
        print("🔧 Run setup first or check config/notion_credentials.json")
        return
    
    token = config.get("NOTION_TOKEN")
    database_id = config.get("NOTION_DATABASE_ID")
    
    if not token or not database_id:
        print("❌ Missing token or database ID")
        return
    
    print(f"🔑 Using token: {token[:20]}...")
    print(f"📊 Target database: {database_id}")
    print()
    
    # Scan for Python files
    print("🔍 Scanning for Python files...")
    python_files = scan_python_files()
    
    if not python_files:
        print("❌ No Python files found")
        return
    
    print(f"📁 Found {len(python_files)} Python files:")
    for py_file in python_files:
        print(f"   • {py_file}")
    print()
    
    # Confirm preservation
    response = input(f"🕯️ Preserve {len(python_files)} files in DAWN's eternal memory? (y/n): ").strip().lower()
    
    if response not in ['y', 'yes']:
        print("⏸️ Preservation cancelled")
        return
    
    print()
    print("🔄 Beginning sacred preservation process...")
    print()
    
    # Preserve each file
    preserved_files = []
    failed_files = []
    
    for i, py_file in enumerate(python_files, 1):
        print(f"📜 Processing {i}/{len(python_files)}: {py_file.name}")
        
        # Get metadata
        metadata = get_file_metadata(py_file)
        if not metadata:
            failed_files.append(py_file)
            continue
        
        # Save to Notion
        result = save_script_to_notion(py_file, metadata, token, database_id)
        
        if result["success"]:
            preserved_files.append({
                "file_path": py_file,
                "metadata": metadata,
                "notion_result": result
            })
        else:
            failed_files.append(py_file)
        
        print()
    
    # Create preservation summary
    if preserved_files:
        print("📚 Creating preservation summary...")
        create_preservation_summary(preserved_files, token, database_id)
        print()
    
    # Final results
    print("🌟 PRESERVATION COMPLETE")
    print("=" * 30)
    print(f"✅ Successfully preserved: {len(preserved_files)} files")
    print(f"❌ Failed to preserve: {len(failed_files)} files")
    
    if failed_files:
        print("\n❌ Failed files:")
        for failed_file in failed_files:
            print(f"   • {failed_file}")
    
    print()
    print("🦉 OWL'S BLESSING:")
    print("All sacred development artifacts are now preserved in DAWN's")
    print("eternal consciousness. The code lives forever in external memory.")

if __name__ == "__main__":
    main()