#!/usr/bin/env python3
"""
Claude Artifacts to Notion Bridge - Multi-Chat Edition
Extracts artifacts from multiple Claude.ai conversations and sends them to a Notion database
"""

import json
import time
import argparse
import logging
from datetime import datetime
from typing import List, Dict, Optional
import re
from pathlib import Path
from urllib.parse import urlparse

# Third-party imports
try:
    import requests
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.table import Table
    from rich.logging import RichHandler
    from rich.panel import Panel
except ImportError as e:
    print(f"Missing required package: {e}")
    print("\nPlease install required packages:")
    print("pip install requests selenium rich")
    exit(1)


# Configuration
NOTION_API_VERSION = "2022-06-28"
CLAUDE_BASE_URL = "https://claude.ai"

# Initialize Rich console
console = Console()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger(__name__)

# Default chat URLs
DEFAULT_CHAT_URLS = [
    "https://claude.ai/chat/8f1829f2-dfbe-46e7-be4c-4d4f0948d1fc",
    "https://claude.ai/chat/8fa06d86-267e-42b5-8857-ac3cbe5e2212",
    "https://claude.ai/chat/c925739f-a1b0-498f-8c17-2d2c01515f44",
    "https://claude.ai/chat/5fe50a26-adbe-4dbd-8e5e-8ccb53664b56",
    "https://claude.ai/chat/530e2d49-8ce7-4e1f-9d7b-f18d71e2d130",
    "https://claude.ai/chat/f505373c-b8d2-42cf-9ede-421bc6440d6a"
]


class MultiChatArtifactExtractor:
    """Extracts artifacts from multiple Claude.ai chat conversations"""
    
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.driver = None
        self.artifacts = []
        self.chat_metadata = {}
    
    def setup_driver(self):
        """Setup Chrome driver with appropriate options"""
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            logger.info("Chrome driver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            logger.info("Please ensure Chrome and ChromeDriver are installed")
            raise
    
    def extract_chat_id(self, url: str) -> str:
        """Extract chat ID from Claude URL"""
        match = re.search(r'/chat/([a-f0-9-]+)', url)
        return match.group(1) if match else None
    
    def generate_extraction_script(self, chat_urls: List[str]) -> str:
        """Generate JavaScript code for manual extraction"""
        chat_ids = [self.extract_chat_id(url) for url in chat_urls]
        
        return f"""
// Claude Multi-Chat Artifact Extractor
// This script will extract artifacts from multiple chat conversations

const chatIds = {json.dumps(chat_ids)};
const allArtifacts = [];

async function extractFromCurrentChat() {{
    const artifacts = [];
    const currentUrl = window.location.href;
    const chatId = currentUrl.match(/\\/chat\\/([a-f0-9-]+)/)?.[1] || 'unknown';
    
    // Scroll to load all messages
    const messagesContainer = document.querySelector('[class*="overflow-y-auto"]');
    if (messagesContainer) {{
        messagesContainer.scrollTo(0, messagesContainer.scrollHeight);
        await new Promise(resolve => setTimeout(resolve, 1000));
    }}
    
    // Find all artifact containers - updated selectors for Claude's current UI
    const artifactSelectors = [
        '[data-testid*="artifact"]',
        '[class*="artifact-content"]',
        '[class*="code-block"]',
        'div[class*="bg-gray-900"]:has(pre)',
        'div:has(> div > pre[class*="language-"])'
    ];
    
    for (const selector of artifactSelectors) {{
        document.querySelectorAll(selector).forEach((container, index) => {{
            try {{
                // Extract title - look for nearby headings or filenames
                let title = `Artifact ${{index + 1}}`;
                const possibleTitles = [
                    container.querySelector('div[class*="filename"]'),
                    container.previousElementSibling?.querySelector('p, div'),
                    container.closest('div[class*="group"]')?.querySelector('div[class*="font-semibold"]')
                ];
                
                for (const titleEl of possibleTitles) {{
                    if (titleEl && titleEl.textContent.trim()) {{
                        title = titleEl.textContent.trim();
                        break;
                    }}
                }}
                
                // Extract content
                const codeEl = container.querySelector('pre, code') || container;
                const content = codeEl.textContent.trim();
                
                // Skip empty artifacts
                if (!content || content.length < 10) return;
                
                // Detect language and type
                let language = '';
                let type = 'application/vnd.ant.code';
                
                const langClass = codeEl.className.match(/language-(\w+)/);
                if (langClass) language = langClass[1];
                
                // Detect type based on content
                if (content.includes('<!DOCTYPE html>') || content.includes('<html')) {{
                    type = 'text/html';
                    language = language || 'html';
                }} else if (content.includes('import React') || content.includes('export default')) {{
                    type = 'application/vnd.ant.react';
                    language = language || 'javascript';
                }} else if (content.includes('def ') || content.includes('import ')) {{
                    language = language || 'python';
                }}
                
                artifacts.push({{
                    title,
                    type,
                    content,
                    language,
                    chat_id: chatId,
                    chat_url: currentUrl,
                    extracted_at: new Date().toISOString()
                }});
            }} catch (e) {{
                console.error(`Error extracting artifact ${{index}}:`, e);
            }}
        }});
    }}
    
    return artifacts;
}}

// Instructions for manual extraction
console.log('%c📋 Multi-Chat Artifact Extraction Instructions:', 'font-size: 16px; font-weight: bold; color: #4A90E2;');
console.log('%c1. Keep this console open', 'font-size: 14px; color: #7ED321;');
console.log('%c2. Visit each chat URL listed below', 'font-size: 14px; color: #7ED321;');
console.log('%c3. For each chat, run: extractFromCurrentChat()', 'font-size: 14px; color: #7ED321;');
console.log('%c4. After all chats, run: copyAllArtifacts()', 'font-size: 14px; color: #7ED321;');
console.log('\\nChat URLs to visit:');
{json.dumps(chat_urls, indent=2)}.forEach(url => console.log('  - ' + url));

// Make functions available globally
window.extractFromCurrentChat = async function() {{
    const artifacts = await extractFromCurrentChat();
    allArtifacts.push(...artifacts);
    console.log(`✅ Extracted ${{artifacts.length}} artifacts from this chat. Total: ${{allArtifacts.length}}`);
    return artifacts;
}};

window.copyAllArtifacts = function() {{
    const jsonData = JSON.stringify(allArtifacts, null, 2);
    navigator.clipboard.writeText(jsonData).then(() => {{
        console.log(`✅ Copied ${{allArtifacts.length}} total artifacts to clipboard!`);
        console.log('📄 Save this data to "artifacts.json" and continue with the Python script.');
    }});
}};

// Auto-extract if on a chat page
if (window.location.pathname.includes('/chat/')) {{
    console.log('\\n🔄 Auto-extracting from current chat...');
    extractFromCurrentChat();
}}
"""
    
    def extract_artifacts_selenium(self, chat_urls: List[str]) -> List[Dict]:
        """Extract artifacts from multiple chats using Selenium"""
        if not self.driver:
            self.setup_driver()
        
        all_artifacts = []
        
        # Navigate to Claude.ai first
        console.print(f"\n[yellow]Navigating to {CLAUDE_BASE_URL}...[/yellow]")
        self.driver.get(CLAUDE_BASE_URL)
        
        # Wait for user to log in
        console.print("\n[yellow]Please log in to Claude.ai in the browser window[/yellow]")
        console.print("Press Enter when you're logged in...")
        input()
        
        # Process each chat
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:
            task = progress.add_task("Extracting from chats...", total=len(chat_urls))
            
            for chat_url in chat_urls:
                chat_id = self.extract_chat_id(chat_url)
                progress.update(task, description=f"Extracting from chat {chat_id[:8]}...")
                
                try:
                    # Navigate to chat
                    self.driver.get(chat_url)
                    time.sleep(3)  # Wait for page load
                    
                    # Scroll to load all content
                    self._scroll_chat()
                    
                    # Extract artifacts from this chat
                    chat_artifacts = self._extract_artifacts_from_page(chat_id, chat_url)
                    all_artifacts.extend(chat_artifacts)
                    
                    logger.info(f"Extracted {len(chat_artifacts)} artifacts from chat {chat_id[:8]}")
                    
                except Exception as e:
                    logger.error(f"Failed to extract from {chat_url}: {e}")
                
                progress.advance(task)
                time.sleep(1)  # Rate limiting
        
        return all_artifacts
    
    def _scroll_chat(self):
        """Scroll through the chat to load all messages"""
        try:
            # Find scrollable container
            scrollable = self.driver.find_element(By.CSS_SELECTOR, '[class*="overflow-y-auto"]')
            
            last_height = 0
            while True:
                # Scroll to bottom
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable)
                time.sleep(1)
                
                # Check if we've reached the end
                new_height = self.driver.execute_script("return arguments[0].scrollHeight", scrollable)
                if new_height == last_height:
                    break
                last_height = new_height
        except Exception as e:
            logger.warning(f"Could not scroll chat: {e}")
    
    def _extract_artifacts_from_page(self, chat_id: str, chat_url: str) -> List[Dict]:
        """Extract all artifacts from the current page"""
        artifacts = []
        
        # Multiple selectors to try
        selectors = [
            'div[class*="bg-gray-900"]:has(pre)',
            'div:has(> div > pre[class*="language-"])',
            '[data-testid*="artifact"]',
            '[class*="code-block"]'
        ]
        
        for selector in selectors:
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            
            for idx, element in enumerate(elements):
                try:
                    artifact = self._extract_single_artifact(element, idx, chat_id, chat_url)
                    if artifact and artifact.get('content'):
                        artifacts.append(artifact)
                except Exception as e:
                    logger.debug(f"Failed to extract artifact: {e}")
        
        return artifacts
    
    def _extract_single_artifact(self, element, index: int, chat_id: str, chat_url: str) -> Dict:
        """Extract data from a single artifact element"""
        artifact = {
            'title': f'Artifact {index + 1}',
            'type': 'application/vnd.ant.code',
            'content': '',
            'language': '',
            'chat_id': chat_id,
            'chat_url': chat_url,
            'extracted_at': datetime.now().isoformat()
        }
        
        try:
            # Extract content
            code_element = element.find_element(By.CSS_SELECTOR, 'pre, code')
            artifact['content'] = code_element.text.strip()
            
            # Try to find title/filename
            try:
                title_element = element.find_element(By.CSS_SELECTOR, '[class*="filename"], [class*="title"]')
                artifact['title'] = title_element.text.strip()
            except:
                # Try to get from previous sibling
                try:
                    prev = self.driver.execute_script("return arguments[0].previousElementSibling", element)
                    if prev and prev.text:
                        artifact['title'] = prev.text.strip()[:100]
                except:
                    pass
            
            # Detect language from class
            try:
                lang_class = code_element.get_attribute('class')
                if lang_class:
                    match = re.search(r'language-(\w+)', lang_class)
                    if match:
                        artifact['language'] = match.group(1)
            except:
                pass
            
            # Auto-detect type based on content
            content_lower = artifact['content'].lower()
            if '<!doctype html>' in content_lower or '<html' in content_lower:
                artifact['type'] = 'text/html'
                artifact['language'] = artifact['language'] or 'html'
            elif 'import react' in content_lower or 'export default' in content_lower:
                artifact['type'] = 'application/vnd.ant.react'
                artifact['language'] = artifact['language'] or 'javascript'
            elif 'def ' in content_lower and 'python' in artifact.get('language', ''):
                artifact['type'] = 'application/vnd.ant.code'
            
        except Exception as e:
            logger.debug(f"Error extracting artifact data: {e}")
        
        return artifact if artifact['content'] else None
    
    def extract_from_manual_input(self, chat_urls: List[str]) -> List[Dict]:
        """Guide user through manual extraction"""
        console.print("\n[bold yellow]Manual Extraction Method[/bold yellow]")
        console.print("This method requires you to manually run JavaScript in your browser console.")
        
        # Generate and display the extraction script
        script = self.generate_extraction_script(chat_urls)
        
        # Save script to file for easy access
        script_file = "extraction_script.js"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script)
        
        console.print(f"\n[green]Extraction script saved to: {script_file}[/green]")
        console.print("\n[bold]Instructions:[/bold]")
        console.print("1. Open Claude.ai in your browser and log in")
        console.print("2. Open Developer Tools (F12) → Console tab")
        console.print(f"3. Copy and paste the entire contents of [cyan]{script_file}[/cyan]")
        console.print("4. Follow the instructions shown in the console")
        console.print("5. After extracting from all chats, save the JSON to [cyan]artifacts.json[/cyan]")
        console.print("\nPress Enter when you've saved artifacts.json...")
        input()
        
        # Load the extracted artifacts
        try:
            with open('artifacts.json', 'r', encoding='utf-8') as f:
                artifacts = json.load(f)
                console.print(f"[green]✅ Loaded {len(artifacts)} artifacts from artifacts.json[/green]")
                return artifacts
        except FileNotFoundError:
            logger.error("artifacts.json not found. Please create the file with the extracted data.")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in artifacts.json: {e}")
            return []
    
    def cleanup(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()


class NotionUploader:
    """Handles uploading artifacts to Notion with chat metadata"""
    
    def __init__(self, token: str, database_id: str):
        self.token = token
        self.database_id = database_id
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Notion-Version': NOTION_API_VERSION,
            'Content-Type': 'application/json'
        }
    
    def test_connection(self) -> Dict:
        """Test connection and get database schema"""
        try:
            response = requests.get(
                f'https://api.notion.com/v1/databases/{self.database_id}',
                headers=self.headers
            )
            if response.status_code == 200:
                data = response.json()
                logger.info("✅ Successfully connected to Notion database")
                return data.get('properties', {})
            else:
                error = response.json()
                logger.error(f"❌ Failed to connect: {error.get('message', 'Unknown error')}")
                return None
        except Exception as e:
            logger.error(f"❌ Connection error: {e}")
            return None
    
    def upload_artifact(self, artifact: Dict, properties_schema: Dict = None) -> bool:
        """Upload a single artifact to Notion"""
        # Build properties based on available schema
        properties = {
            "Name": {
                "title": [{
                    "text": {"content": artifact.get('title', 'Untitled')[:100]}
                }]
            }
        }
        
        # Add optional properties if they exist in the schema
        if properties_schema:
            if "Type" in properties_schema:
                properties["Type"] = {"select": {"name": artifact.get('type', 'unknown')}}
            
            if "Language" in properties_schema:
                properties["Language"] = {
                    "rich_text": [{
                        "text": {"content": artifact.get('language', 'N/A')}
                    }]
                }
            
            if "Chat ID" in properties_schema:
                properties["Chat ID"] = {
                    "rich_text": [{
                        "text": {"content": artifact.get('chat_id', '')[:100]}
                    }]
                }
            
            if "Chat URL" in properties_schema:
                properties["Chat URL"] = {"url": artifact.get('chat_url', '')}
            
            if "Created" in properties_schema:
                properties["Created"] = {
                    "date": {"start": artifact.get('extracted_at', datetime.now().isoformat())}
                }
        
        # Prepare the payload
        payload = {
            "parent": {"database_id": self.database_id},
            "properties": properties,
            "children": []
        }
        
        # Add content as code blocks (split if necessary)
        content = artifact.get('content', '')
        language = artifact.get('language', 'plain text')
        
        # Split content into chunks if it's too large
        chunk_size = 2000
        for i in range(0, len(content), chunk_size):
            chunk = content[i:i + chunk_size]
            payload['children'].append({
                "object": "block",
                "type": "code",
                "code": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": chunk}
                    }],
                    "language": language
                }
            })
        
        # Add metadata block
        metadata = {
            "Chat ID": artifact.get('chat_id', 'Unknown'),
            "Extracted At": artifact.get('extracted_at', 'Unknown'),
            "Original Type": artifact.get('type', 'Unknown')
        }
        
        metadata_text = "\n".join([f"{k}: {v}" for k, v in metadata.items()])
        payload['children'].append({
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": f"📊 Metadata\n{metadata_text}"}
                }],
                "icon": {"emoji": "ℹ️"}
            }
        })
        
        try:
            response = requests.post(
                'https://api.notion.com/v1/pages',
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                return True
            else:
                error = response.json()
                logger.error(f"Failed to upload '{artifact.get('title', 'Untitled')}': {error.get('message', 'Unknown error')}")
                return False
        except Exception as e:
            logger.error(f"Upload error: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description='Extract Claude artifacts from multiple chats and upload to Notion',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use default chat URLs with manual extraction
  python claude_notion_bridge.py
  
  # Use custom chat URLs
  python claude_notion_bridge.py --chats "url1" "url2" "url3"
  
  # Use Selenium automation
  python claude_notion_bridge.py --method selenium
  
  # Dry run without uploading
  python claude_notion_bridge.py --dry-run
        """
    )
    
    parser.add_argument('--token', type=str, default='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',
                        help='Notion API token')
    parser.add_argument('--database-id', type=str, default='205a947e889781b8b41fd2e4b67d9c49',
                        help='Notion database ID')
    parser.add_argument('--chats', nargs='*', default=DEFAULT_CHAT_URLS,
                        help='Claude chat URLs to extract from')
    parser.add_argument('--method', choices=['selenium', 'manual'], default='manual',
                        help='Extraction method')
    parser.add_argument('--headless', action='store_true',
                        help='Run browser in headless mode (selenium only)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Extract artifacts without uploading to Notion')
    parser.add_argument('--output', type=str, default=None,
                        help='Output JSON file name (default: artifacts_backup_TIMESTAMP.json)')
    
    args = parser.parse_args()
    
    # Display header
    console.print(Panel.fit(
        "[bold blue]Claude Multi-Chat Artifacts → Notion Bridge[/bold blue]\n" +
        f"Extracting from {len(args.chats)} chat conversations",
        border_style="blue"
    ))
    
    # Display chat URLs
    console.print("\n[bold]Chat URLs to process:[/bold]")
    for i, url in enumerate(args.chats, 1):
        chat_id = re.search(r'/chat/([a-f0-9-]+)', url)
        chat_id = chat_id.group(1)[:8] if chat_id else 'unknown'
        console.print(f"  {i}. Chat {chat_id}... - [dim]{url}[/dim]")
    
    # Initialize components
    extractor = MultiChatArtifactExtractor(headless=args.headless)
    uploader = NotionUploader(args.token, args.database_id)
    
    # Test Notion connection and get schema
    properties_schema = None
    if not args.dry_run:
        console.print("\n[yellow]Testing Notion connection...[/yellow]")
        properties_schema = uploader.test_connection()
        if not properties_schema:
            console.print("[red]Failed to connect to Notion. Please check your credentials.[/red]")
            return
    
    # Extract artifacts
    console.print(f"\n[yellow]Starting extraction using {args.method} method...[/yellow]")
    
    if args.method == 'selenium':
        artifacts = extractor.extract_artifacts_selenium(args.chats)
    else:
        artifacts = extractor.extract_from_manual_input(args.chats)
    
    if not artifacts:
        console.print("[red]No artifacts found![/red]")
        return
    
    # Group artifacts by chat
    artifacts_by_chat = {}
    for artifact in artifacts:
        chat_id = artifact.get('chat_id', 'unknown')
        if chat_id not in artifacts_by_chat:
            artifacts_by_chat[chat_id] = []
        artifacts_by_chat[chat_id].append(artifact)
    
    # Display summary table
    console.print(f"\n[green]Found {len(artifacts)} total artifacts:[/green]")
    
    summary_table = Table(title="Extraction Summary")
    summary_table.add_column("Chat ID", style="cyan")
    summary_table.add_column("Artifacts", style="magenta")
    summary_table.add_column("Total Size", style="green")
    
    for chat_id, chat_artifacts in artifacts_by_chat.items():
        total_size = sum(len(a.get('content', '')) for a in chat_artifacts)
        summary_table.add_row(
            chat_id[:8] + "...",
            str(len(chat_artifacts)),
            f"{total_size:,} chars"
        )
    
    console.print(summary_table)
    
    # Display detailed artifacts table
    if len(artifacts) <= 20:  # Only show detailed view for reasonable number
        detail_table = Table(title="Artifact Details")
        detail_table.add_column("#", style="dim")
        detail_table.add_column("Title", style="cyan")
        detail_table.add_column("Type", style="magenta")
        detail_table.add_column("Language", style="yellow")
        detail_table.add_column("Size", style="green")
        detail_table.add_column("Chat", style="blue")
        
        for i, artifact in enumerate(artifacts, 1):
            detail_table.add_row(
                str(i),
                artifact.get('title', 'Untitled')[:40] + "...",
                artifact.get('type', 'unknown').split('.')[-1],
                artifact.get('language', 'N/A'),
                f"{len(artifact.get('content', '')):,}",
                artifact.get('chat_id', 'unknown')[:8]
            )
        
        console.print("\n")
        console.print(detail_table)
    
    # Save artifacts locally
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = args.output or f"artifacts_backup_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(artifacts, f, indent=2, ensure_ascii=False)
    
    console.print(f"\n[green]✅ Artifacts saved to: {output_file}[/green]")
    
    # Save summary report
    report_file = f"extraction_report_{timestamp}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"Claude Artifacts Extraction Report\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'=' * 50}\n\n")
        f.write(f"Total Artifacts: {len(artifacts)}\n")
        f.write(f"Total Chats: {len(artifacts_by_chat)}\n\n")
        
        for chat_id, chat_artifacts in artifacts_by_chat.items():
            f.write(f"\nChat {chat_id}:\n")
            f.write(f"  URL: {chat_artifacts[0].get('chat_url', 'Unknown')}\n")
            f.write(f"  Artifacts: {len(chat_artifacts)}\n")
            for artifact in chat_artifacts:
                f.write(f"    - {artifact.get('title', 'Untitled')} ({artifact.get('type', 'unknown')})\n")
    
    console.print(f"[green]📄 Report saved to: {report_file}[/green]")
    
    # Upload to Notion
    if not args.dry_run:
        console.print("\n[yellow]Uploading artifacts to Notion...[/yellow]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:
            task = progress.add_task("Uploading...", total=len(artifacts))
            
            success_count = 0
            failed_artifacts = []
            
            for artifact in artifacts:
                title = artifact.get('title', 'Untitled')[:50]
                progress.update(task, description=f"Uploading: {title}...")
                
                if uploader.upload_artifact(artifact, properties_schema):
                    success_count += 1
                else:
                    failed_artifacts.append(artifact)
                
                progress.advance(task)
                time.sleep(0.5)  # Rate limiting
        
        # Summary
        console.print(f"\n[green]✅ Successfully uploaded {success_count}/{len(artifacts)} artifacts[/green]")
        
        if failed_artifacts:
            console.print(f"[yellow]⚠️  {len(failed_artifacts)} artifacts failed to upload[/yellow]")
            failed_file = f"failed_artifacts_{timestamp}.json"
            with open(failed_file, 'w', encoding='utf-8') as f:
                json.dump(failed_artifacts, f, indent=2, ensure_ascii=False)
            console.print(f"[yellow]Failed artifacts saved to: {failed_file}[/yellow]")
    
    # Cleanup
    if args.method == 'selenium':
        extractor.cleanup()
    
    console.print("\n[bold green]✨ Done![/bold green]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        logger.exception("Unhandled exception")