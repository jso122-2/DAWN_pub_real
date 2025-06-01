
// Claude Multi-Chat Artifact Extractor
// This script will extract artifacts from multiple chat conversations

const chatIds = ["8f1829f2-dfbe-46e7-be4c-4d4f0948d1fc", "8fa06d86-267e-42b5-8857-ac3cbe5e2212", "c925739f-a1b0-498f-8c17-2d2c01515f44", "5fe50a26-adbe-4dbd-8e5e-8ccb53664b56", "530e2d49-8ce7-4e1f-9d7b-f18d71e2d130", "f505373c-b8d2-42cf-9ede-421bc6440d6a"];
const allArtifacts = [];

async function extractFromCurrentChat() {
    const artifacts = [];
    const currentUrl = window.location.href;
    const chatId = currentUrl.match(/\/chat\/([a-f0-9-]+)/)?.[1] || 'unknown';
    
    // Scroll to load all messages
    const messagesContainer = document.querySelector('[class*="overflow-y-auto"]');
    if (messagesContainer) {
        messagesContainer.scrollTo(0, messagesContainer.scrollHeight);
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    // Find all artifact containers - updated selectors for Claude's current UI
    const artifactSelectors = [
        '[data-testid*="artifact"]',
        '[class*="artifact-content"]',
        '[class*="code-block"]',
        'div[class*="bg-gray-900"]:has(pre)',
        'div:has(> div > pre[class*="language-"])'
    ];
    
    for (const selector of artifactSelectors) {
        document.querySelectorAll(selector).forEach((container, index) => {
            try {
                // Extract title - look for nearby headings or filenames
                let title = `Artifact ${index + 1}`;
                const possibleTitles = [
                    container.querySelector('div[class*="filename"]'),
                    container.previousElementSibling?.querySelector('p, div'),
                    container.closest('div[class*="group"]')?.querySelector('div[class*="font-semibold"]')
                ];
                
                for (const titleEl of possibleTitles) {
                    if (titleEl && titleEl.textContent.trim()) {
                        title = titleEl.textContent.trim();
                        break;
                    }
                }
                
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
                if (content.includes('<!DOCTYPE html>') || content.includes('<html')) {
                    type = 'text/html';
                    language = language || 'html';
                } else if (content.includes('import React') || content.includes('export default')) {
                    type = 'application/vnd.ant.react';
                    language = language || 'javascript';
                } else if (content.includes('def ') || content.includes('import ')) {
                    language = language || 'python';
                }
                
                artifacts.push({
                    title,
                    type,
                    content,
                    language,
                    chat_id: chatId,
                    chat_url: currentUrl,
                    extracted_at: new Date().toISOString()
                });
            } catch (e) {
                console.error(`Error extracting artifact ${index}:`, e);
            }
        });
    }
    
    return artifacts;
}

// Instructions for manual extraction
console.log('%c📋 Multi-Chat Artifact Extraction Instructions:', 'font-size: 16px; font-weight: bold; color: #4A90E2;');
console.log('%c1. Keep this console open', 'font-size: 14px; color: #7ED321;');
console.log('%c2. Visit each chat URL listed below', 'font-size: 14px; color: #7ED321;');
console.log('%c3. For each chat, run: extractFromCurrentChat()', 'font-size: 14px; color: #7ED321;');
console.log('%c4. After all chats, run: copyAllArtifacts()', 'font-size: 14px; color: #7ED321;');
console.log('\nChat URLs to visit:');
[
  "https://claude.ai/chat/8f1829f2-dfbe-46e7-be4c-4d4f0948d1fc",
  "https://claude.ai/chat/8fa06d86-267e-42b5-8857-ac3cbe5e2212",
  "https://claude.ai/chat/c925739f-a1b0-498f-8c17-2d2c01515f44",
  "https://claude.ai/chat/5fe50a26-adbe-4dbd-8e5e-8ccb53664b56",
  "https://claude.ai/chat/530e2d49-8ce7-4e1f-9d7b-f18d71e2d130",
  "https://claude.ai/chat/f505373c-b8d2-42cf-9ede-421bc6440d6a"
].forEach(url => console.log('  - ' + url));

// Make functions available globally
window.extractFromCurrentChat = async function() {
    const artifacts = await extractFromCurrentChat();
    allArtifacts.push(...artifacts);
    console.log(`✅ Extracted ${artifacts.length} artifacts from this chat. Total: ${allArtifacts.length}`);
    return artifacts;
};

window.copyAllArtifacts = function() {
    const jsonData = JSON.stringify(allArtifacts, null, 2);
    navigator.clipboard.writeText(jsonData).then(() => {
        console.log(`✅ Copied ${allArtifacts.length} total artifacts to clipboard!`);
        console.log('📄 Save this data to "artifacts.json" and continue with the Python script.');
    });
};

// Auto-extract if on a chat page
if (window.location.pathname.includes('/chat/')) {
    console.log('\n🔄 Auto-extracting from current chat...');
    extractFromCurrentChat();
}
