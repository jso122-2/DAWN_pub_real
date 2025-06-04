#!/usr/bin/env python3
"""
🦉 NOTION ARTIFACT SYNC
=======================
Captures Claude's generated artifacts and syncs them to Notion.
Monitors artifact creation, validates completion, and pushes to workspace.
"""

import os
import json
import asyncio
import aiohttp
from datetime import datetime, timezone
from typing import Dict, List, Optional
import hashlib
from pathlib import Path

class NotionArtifactSync:
    def __init__(self):
        self.notion_token = os.getenv("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")
        self.code_db_id = os.getenv("205a947e889781e8b384000c3021d0a0")
        self.artifacts_captured = set()
        
    async def create_notion_code_page(self, artifact: Dict) -> bool:
        """Push completed artifact to Notion code database"""
        
        headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        # Create Notion page for code artifact
        page_data = {
            "parent": {"database_id": self.code_db_id},
            "properties": {
                "Title": {
                    "title": [{
                        "text": {"content": artifact['filename']}
                    }]
                },
                "Type": {
                    "select": {"name": artifact['type']}
                },
                "Language": {
                    "select": {"name": artifact.get('language', 'python')}
                },
                "Created": {
                    "date": {"start": artifact['timestamp']}
                },
                "Chat_Source": {
                    "select": {"name": artifact['chat_id'][-8:]}
                },
                "Status": {
                    "select": {"name": "Complete"}
                }
            },
            "children": [
                {
                    "object": "block",
                    "type": "code",
                    "code": {
                        "language": artifact.get('language', 'python'),
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": artifact['content'][:2000]}  # Notion limit
                        }]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": f"Full content: {len(artifact['content'])} chars"}
                        }]
                    }
                }
            ]
        }
        
        # If content is too long, add as file block
        if len(artifact['content']) > 2000:
            # Save locally first
            local_path = Path(f"artifacts_cache/{artifact['filename']}")
            local_path.parent.mkdir(exist_ok=True)
            with open(local_path, 'w', encoding='utf-8') as f:
                f.write(artifact['content'])
            
            page_data['children'].append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": f"📄 Full file saved locally: {local_path}"
                        }
                    }]
                }
            })
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.notion.com/v1/pages",
                headers=headers,
                json=page_data
            ) as response:
                if response.status == 200:
                    print(f"✅ Synced to Notion: {artifact['filename']}")
                    return True
                else:
                    error = await response.text()
                    print(f"❌ Notion sync error: {response.status} - {error}")
                    return False

    def capture_artifact(self, artifact_data: Dict) -> Dict:
        """Process and prepare artifact for Notion"""
        
        # Generate unique ID
        content_hash = hashlib.sha256(
            artifact_data['content'].encode()
        ).hexdigest()[:12]
        
        if content_hash in self.artifacts_captured:
            return None  # Already captured
        
        self.artifacts_captured.add(content_hash)
        
        return {
            "filename": artifact_data['filename'],
            "type": artifact_data['type'],
            "language": artifact_data.get('language', 'text'),
            "content": artifact_data['content'],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "chat_id": artifact_data.get('chat_id', 'unknown'),
            "hash": content_hash
        }

    async def monitor_and_sync(self, artifact_queue: asyncio.Queue):
        """Main monitoring loop"""
        print("🦉 Artifact Sync Active - Monitoring for Claude artifacts...")
        
        while True:
            try:
                # Wait for artifact from queue
                artifact_data = await artifact_queue.get()
                
                # Capture and prepare
                artifact = self.capture_artifact(artifact_data)
                
                if artifact:
                    # Sync to Notion
                    success = await self.create_notion_code_page(artifact)
                    
                    if success:
                        # Log locally too
                        log_path = Path(f"logs/artifact_sync/{artifact['hash']}.json")
                        log_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(log_path, 'w') as f:
                            json.dump(artifact, f, indent=2)
                
            except Exception as e:
                print(f"❌ Sync error: {e}")
                await asyncio.sleep(5)

# Example artifact structure for testing
EXAMPLE_ARTIFACT = {
    "filename": "pressure_reflection_loop.py",
    "type": "code",
    "language": "python", 
    "content": "# Your actual code here...",
    "chat_id": "8f1829f2-dfbe-46e7-be4c-4d4f0948d1fc"
}

async def main():
    # Create sync instance
    syncer = NotionArtifactSync()
    
    # Create queue for artifacts
    artifact_queue = asyncio.Queue()
    
    # Start monitoring
    monitor_task = asyncio.create_task(
        syncer.monitor_and_sync(artifact_queue)
    )
    
    # Test with example
    await artifact_queue.put(EXAMPLE_ARTIFACT)
    
    # Keep running
    await monitor_task

if __name__ == "__main__":
    print("""
    🌀 NOTION ARTIFACT SYNC
    ======================
    
    Set these environment variables:
    - NOTION_ACCESS_TOKEN: Your integration token
    - NOTION_CODE_DATABASE_ID: Database for code artifacts
    
    This will capture Claude artifacts and sync to Notion.
    """)
    
    asyncio.run(main())