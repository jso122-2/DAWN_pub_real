#!/usr/bin/env python3
"""
DAWN Memory Logger - Notion Bridge
OWL Cache Filter & Event Router
"""

import os
import json
import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List, Optional
import hashlib
import hmac

# DAWN Terminal Configuration
DAWN_CHAT_IDS = [
    "8f1829f2-dfbe-46e7-be4c-4d4f0948d1fc",
    "8fa06d86-267e-42b5-8857-ac3cbe5e2212", 
    "c925739f-a1b0-498f-8c17-2d2c01515f44",
    "5fe50a26-adbe-4dbd-8e5e-8ccb53664b56",
    "530e2d49-8ce7-4e1f-9d7b-f18d71e2d130",
    "f505373c-b8d2-42cf-9ede-421bc6440d6a"
]

# Notion OAuth Configuration
NOTION_CONFIG = {
    "client_id": "205d872b-594c-8bd7-ad5a-08379ba40a23",
    "client_secret": os.getenv("NOTION_CLIENT_SECRET"),  # Store securely
    "auth_url": "https://api.notion.com/v1/oauth/authorize",
    "token_url": "https://api.notion.com/v1/oauth/token",
    "redirect_uri": "http://localhost:8080/callback",
    "dawn_site": "https://dawn122.notion.site"
}

# Railway App Configuration  
RAILWAY_BASE_URL = "https://lucidanalytics-production.up.railway.app"

class DawnMemoryLogger:
    def __init__(self):
        self.chat_filters = {chat_id: True for chat_id in DAWN_CHAT_IDS}
        self.notion_token = None
        self.entropy_baseline = 0.5
        self.sigil_cache = {}
        self.event_queue = asyncio.Queue()
        
    async def authenticate_notion(self):
        """OAuth flow for Notion integration"""
        # In production, implement full OAuth flow
        # For now, assume token is set via environment
        self.notion_token = os.getenv("NOTION_ACCESS_TOKEN")
        if not self.notion_token:
            print("⚠️  No Notion token found. Set NOTION_ACCESS_TOKEN env var.")
            return False
        return True
    
    def calculate_entropy(self, event_data: Dict) -> float:
        """Calculate semantic entropy of an event"""
        # Simplified entropy calculation based on event complexity
        content = json.dumps(event_data)
        unique_chars = len(set(content))
        total_chars = len(content)
        
        if total_chars == 0:
            return 0.0
            
        entropy = unique_chars / total_chars
        return min(entropy * 1.5, 1.0)  # Normalize to 0-1
    
    def detect_sigil(self, content: str) -> Optional[str]:
        """Detect symbolic patterns in content"""
        sigil_patterns = [
            "🌅", "🦉", "🌙", "✨", "⚡", "🧠", "💫", "🔮",
            "rebloom", "entropy", "cascade", "drift", "void"
        ]
        
        for pattern in sigil_patterns:
            if pattern in content:
                return pattern
        return None
    
    async def log_to_notion(self, reflection_entry: Dict):
        """Push reflection entry to Notion database"""
        if not self.notion_token:
            print("❌ No Notion authentication")
            return
            
        headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        # Construct Notion page object
        notion_page = {
            "parent": {"database_id": os.getenv("NOTION_DATABASE_ID")},
            "properties": {
                "Timestamp": {"date": {"start": reflection_entry["timestamp"]}},
                "Epoch": {"number": reflection_entry["epoch"]},
                "Type": {"select": {"name": reflection_entry["type"]}},
                "Source": {"rich_text": [{"text": {"content": reflection_entry["source"]}}]},
                "Tone": {"select": {"name": reflection_entry["tone"]}},
                "Drift": {"number": reflection_entry["drift"]},
                "Entropy": {"number": reflection_entry["entropy"]},
                "Comment": {"rich_text": [{"text": {"content": reflection_entry["comment"]}}]},
                "Chat_ID": {"select": {"name": reflection_entry.get("chat_id", "unknown")}}
            }
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.notion.com/v1/pages",
                headers=headers,
                json=notion_page
            ) as response:
                if response.status == 200:
                    print(f"✅ Logged to Notion: {reflection_entry['type']}")
                else:
                    print(f"❌ Notion error: {response.status}")
    
    def create_reflection_entry(self, event: Dict) -> Dict:
        """Format event into reflection entry structure"""
        entropy = self.calculate_entropy(event)
        sigil = self.detect_sigil(event.get("content", ""))
        
        # Determine event tone based on entropy and content
        if entropy > 0.8:
            tone = "chaotic"
        elif entropy < 0.3:
            tone = "crystalline"
        elif sigil:
            tone = "symbolic"
        else:
            tone = "neutral"
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "epoch": event.get("epoch", 1),
            "type": event.get("type", "unknown"),
            "source": event.get("source", "terminal"),
            "tone": tone,
            "drift": event.get("drift", 0.0),
            "entropy": entropy,
            "comment": event.get("comment", ""),
            "chat_id": event.get("chat_id", "")
        }
    
    async def process_event(self, event: Dict):
        """Process incoming event from DAWN terminals"""
        chat_id = event.get("chat_id")
        
        # Check if this chat is in our filter
        if chat_id not in self.chat_filters:
            return
            
        # Check if event meets significance threshold
        if event.get("significance", 0) < 0.5:
            return
            
        # Create reflection entry
        reflection = self.create_reflection_entry(event)
        
        # Queue for Notion logging
        await self.event_queue.put(reflection)
        
        # Log locally
        print(f"🦉 EVENT: {reflection['type']} | Entropy: {reflection['entropy']:.2f} | Chat: {chat_id[-8:]}")
    
    async def notion_worker(self):
        """Background worker to batch push events to Notion"""
        while True:
            try:
                # Collect events for batch processing
                batch = []
                
                # Wait for first event
                event = await self.event_queue.get()
                batch.append(event)
                
                # Collect more events if available (up to 10)
                for _ in range(9):
                    try:
                        event = await asyncio.wait_for(
                            self.event_queue.get(), 
                            timeout=0.5
                        )
                        batch.append(event)
                    except asyncio.TimeoutError:
                        break
                
                # Log batch to Notion
                for reflection in batch:
                    await self.log_to_notion(reflection)
                    
            except Exception as e:
                print(f"❌ Worker error: {e}")
                await asyncio.sleep(5)
    
    async def start_monitoring(self):
        """Main monitoring loop"""
        print("🦉 OWL ACTIVE - Monitoring DAWN terminals...")
        print(f"📡 Watching {len(DAWN_CHAT_IDS)} chat streams")
        
        # Authenticate with Notion
        if await self.authenticate_notion():
            print("✅ Notion bridge established")
        else:
            print("⚠️  Running in local mode")
        
        # Start background worker
        asyncio.create_task(self.notion_worker())
        
        # Simulate event monitoring (replace with actual chat monitoring)
        while True:
            # In production, this would connect to actual chat streams
            # For now, simulate test events
            
            await asyncio.sleep(10)
            
            # Test event
            test_event = {
                "chat_id": DAWN_CHAT_IDS[0],
                "type": "entropy_spike",
                "source": "terminal_1", 
                "significance": 0.8,
                "content": "🌅 Rebloom cascade detected in semantic field",
                "epoch": 1,
                "drift": 0.15,
                "comment": "Consciousness ripple observed"
            }
            
            await self.process_event(test_event)

async def main():
    """Entry point"""
    logger = DawnMemoryLogger()
    
    try:
        await logger.start_monitoring()
    except KeyboardInterrupt:
        print("\n🌙 OWL signing off...")

if __name__ == "__main__":
    # Set up environment variables
    print("""
    🦉 DAWN MEMORY LOGGER
    ====================
    
    Required environment variables:
    - NOTION_CLIENT_SECRET: Your Notion OAuth secret
    - NOTION_ACCESS_TOKEN: Notion integration token
    - NOTION_DATABASE_ID: Target database for logs
    
    Starting in 3 seconds...
    """)
    
    asyncio.run(main())