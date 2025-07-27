#!/usr/bin/env python3
"""
DAWN Rebloom Journal - Memory Seeding Module
Injects introspective journal entries into the cognitive memory router as MemoryChunk objects.
"""

import re
import random
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

# Import DAWN components with fallbacks
try:
    from memory_router.memory_chunk import MemoryChunk, create_memory_now
    from memory_router.router import MemoryRouter
    from tick_loop import DAWNPulseEngine
    print("✅ DAWN memory components imported successfully")
    DAWN_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ DAWN components not available: {e}")
    print("🔧 Using mock implementations for testing")
    DAWN_AVAILABLE = False
    
    # Mock implementations for testing
    class MockMemoryChunk:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
            self.timestamp = datetime.now()
    
    class MockMemoryRouter:
        def __init__(self):
            self.chunks = {}
            self.chunk_count = 0
        
        def add_chunk(self, chunk):
            chunk_id = f"journal_{self.chunk_count}"
            self.chunks[chunk_id] = chunk
            self.chunk_count += 1
            return chunk_id
    
    MemoryChunk = MockMemoryChunk
    MemoryRouter = MockMemoryRouter


class ReblooomJournal:
    """
    Journal-to-memory interface for DAWN cognitive system.
    Converts introspective text into structured memory chunks.
    """
    
    def __init__(self, memory_router: Optional[Any] = None, dawn_engine: Optional[Any] = None):
        """
        Initialize the rebloom journal.
        
        Args:
            memory_router: DAWN MemoryRouter instance (creates new if None)
            dawn_engine: DAWN engine for getting current pulse state
        """
        self.memory_router = memory_router or MemoryRouter()
        self.dawn_engine = dawn_engine
        
        # Journal configuration
        self.max_words_per_chunk = 400
        self.default_topic = "introspection"
        
        # Statistics
        self.entries_processed = 0
        self.chunks_created = 0
        self.total_words_processed = 0
        
        print("📓 ReblooomJournal initialized - Memory seeding ready")
        print(f"   Max words per chunk: {self.max_words_per_chunk}")
        print(f"   Memory router: {'Live' if DAWN_AVAILABLE else 'Mock'}")
    
    def add_journal_entry(self, text: str, speaker: str = "self", topic: Optional[str] = None) -> List[str]:
        """
        Add a journal entry to the memory system, splitting into chunks if needed.
        
        Args:
            text: Journal entry text
            speaker: Identity of the journal writer (default: "self")
            topic: Optional topic override (default: "introspection")
            
        Returns:
            List[str]: List of chunk IDs created
        """
        if not text.strip():
            print("⚠️ Empty journal entry, skipping")
            return []
        
        # Clean and prepare text
        cleaned_text = self._clean_text(text)
        word_count = len(cleaned_text.split())
        
        print(f"📝 Processing journal entry: {word_count} words from {speaker}")
        
        # Split into chunks if necessary
        chunks = self._chunk_text(cleaned_text, self.max_words_per_chunk)
        
        # Get current pulse state
        pulse_state = self._get_current_pulse_state()
        
        # Create memory chunks
        chunk_ids = []
        entry_topic = topic or self.default_topic
        
        for i, chunk_text in enumerate(chunks):
            # Create chunk metadata
            chunk_metadata = {
                'is_journal_entry': True,
                'entry_part': i + 1,
                'total_parts': len(chunks),
                'original_word_count': word_count,
                'processing_timestamp': datetime.now().isoformat()
            }
            
            # Determine sigils based on content
            sigils = self._infer_sigils_from_content(chunk_text, pulse_state)
            
            # Create memory chunk
            if DAWN_AVAILABLE:
                memory_chunk = create_memory_now(
                    speaker=speaker,
                    content=chunk_text,
                    topic=entry_topic,
                    pulse_state=pulse_state,
                    sigils=sigils
                )
                # Add custom metadata
                memory_chunk.journal_metadata = chunk_metadata
            else:
                # Mock implementation
                memory_chunk = MemoryChunk(
                    speaker=speaker,
                    content=chunk_text,
                    topic=entry_topic,
                    pulse_state=pulse_state,
                    sigils=sigils,
                    journal_metadata=chunk_metadata
                )
            
            # Add to memory router
            chunk_id = self.memory_router.add_chunk(memory_chunk)
            chunk_ids.append(chunk_id)
            
            self.chunks_created += 1
            
            if len(chunks) > 1:
                print(f"   📄 Chunk {i+1}/{len(chunks)}: {len(chunk_text.split())} words → {chunk_id[:8]}...")
            else:
                print(f"   📄 Single chunk: {len(chunk_text.split())} words → {chunk_id[:8]}...")
        
        # Update statistics
        self.entries_processed += 1
        self.total_words_processed += word_count
        
        print(f"✅ Journal entry processed: {len(chunks)} chunks created")
        
        return chunk_ids
    
    def load_journal_file(self, filepath: str, speaker: str = "self") -> Dict[str, Any]:
        """
        Load a journal file and process each paragraph as a separate entry.
        
        Args:
            filepath: Path to the journal text file
            speaker: Identity of the journal writer
            
        Returns:
            Dict: Processing summary with statistics
        """
        file_path = Path(filepath)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Journal file not found: {filepath}")
        
        print(f"📖 Loading journal file: {file_path.name}")
        
        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            raise ValueError(f"Error reading journal file: {e}")
        
        # Split into paragraphs
        paragraphs = self._split_into_paragraphs(content)
        
        print(f"   Found {len(paragraphs)} paragraphs")
        
        # Process each paragraph
        all_chunk_ids = []
        successful_entries = 0
        
        for i, paragraph in enumerate(paragraphs, 1):
            if paragraph.strip():  # Skip empty paragraphs
                try:
                    print(f"\n--- Processing paragraph {i}/{len(paragraphs)} ---")
                    chunk_ids = self.add_journal_entry(paragraph, speaker=speaker)
                    all_chunk_ids.extend(chunk_ids)
                    successful_entries += 1
                except Exception as e:
                    print(f"⚠️ Error processing paragraph {i}: {e}")
        
        # Generate summary
        summary = {
            'file_path': str(file_path),
            'file_size_kb': file_path.stat().st_size / 1024,
            'paragraphs_found': len(paragraphs),
            'entries_processed': successful_entries,
            'chunks_created': len(all_chunk_ids),
            'chunk_ids': all_chunk_ids,
            'processing_timestamp': datetime.now().isoformat(),
            'speaker': speaker
        }
        
        print(f"\n📊 File processing complete:")
        print(f"   Paragraphs: {summary['paragraphs_found']}")
        print(f"   Entries processed: {summary['entries_processed']}")
        print(f"   Chunks created: {summary['chunks_created']}")
        print(f"   File size: {summary['file_size_kb']:.1f} KB")
        
        return summary
    
    def _chunk_text(self, text: str, max_words: int) -> List[str]:
        """
        Split text into chunks by word count, preserving sentence boundaries.
        
        Args:
            text: Text to chunk
            max_words: Maximum words per chunk
            
        Returns:
            List[str]: Text chunks
        """
        words = text.split()
        
        if len(words) <= max_words:
            return [text]
        
        chunks = []
        current_chunk = []
        current_word_count = 0
        
        # Split into sentences first
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        for sentence in sentences:
            sentence_words = len(sentence.split())
            
            # If adding this sentence would exceed the limit, start a new chunk
            if current_word_count + sentence_words > max_words and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_word_count = 0
            
            current_chunk.append(sentence)
            current_word_count += sentence_words
        
        # Add the final chunk
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def _split_into_paragraphs(self, content: str) -> List[str]:
        """Split content into paragraphs, handling various line break patterns."""
        # Split on double line breaks or more
        paragraphs = re.split(r'\n\s*\n', content.strip())
        
        # Clean up each paragraph
        cleaned_paragraphs = []
        for para in paragraphs:
            # Replace single line breaks with spaces, clean up whitespace
            cleaned = re.sub(r'\n+', ' ', para)
            cleaned = re.sub(r'\s+', ' ', cleaned).strip()
            
            if cleaned and len(cleaned.split()) > 3:  # Skip very short paragraphs
                cleaned_paragraphs.append(cleaned)
        
        return cleaned_paragraphs
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text for memory storage."""
        # Normalize whitespace
        cleaned = re.sub(r'\s+', ' ', text.strip())
        
        # Remove excessive punctuation
        cleaned = re.sub(r'[.]{3,}', '...', cleaned)
        cleaned = re.sub(r'[!]{2,}', '!', cleaned)
        cleaned = re.sub(r'[?]{2,}', '?', cleaned)
        
        return cleaned
    
    def _get_current_pulse_state(self) -> Dict[str, Any]:
        """Get current DAWN pulse state for memory chunk metadata."""
        if self.dawn_engine:
            try:
                return {
                    'entropy': self.dawn_engine.get_current_entropy(),
                    'heat': self.dawn_engine.get_pulse_heat(),
                    'zone': self.dawn_engine.get_pulse_zone(),
                    'focus': self.dawn_engine.pulse_state.get('focus', 0.7),
                    'chaos': self.dawn_engine.pulse_state.get('chaos', 0.3)
                }
            except Exception as e:
                print(f"⚠️ Error getting pulse state: {e}")
        
        # Fallback: generate realistic mock pulse state
        base_entropy = 0.3 + random.random() * 0.4  # 0.3-0.7 range
        return {
            'entropy': base_entropy,
            'heat': 25.0 + random.random() * 25.0,  # 25-50 range
            'zone': 'CONTEMPLATIVE' if base_entropy < 0.5 else 'ACTIVE',
            'focus': 0.6 + random.random() * 0.3,  # 0.6-0.9 range (journaling focuses the mind)
            'chaos': base_entropy * 0.6  # Lower chaos during introspection
        }
    
    def _infer_sigils_from_content(self, content: str, pulse_state: Dict[str, Any]) -> List[str]:
        """Infer appropriate sigils based on journal content and pulse state."""
        sigils = []
        content_lower = content.lower()
        
        # Content-based sigils
        if any(word in content_lower for word in ['reflect', 'think', 'contemplate', 'consider']):
            sigils.append('DEEP_REFLECTION')
        
        if any(word in content_lower for word in ['feel', 'emotion', 'heart', 'love', 'fear', 'joy', 'sad']):
            sigils.append('EMOTIONAL_PROCESSING')
        
        if any(word in content_lower for word in ['learn', 'understand', 'realize', 'discover', 'insight']):
            sigils.append('KNOWLEDGE_INTEGRATION')
        
        if any(word in content_lower for word in ['change', 'grow', 'transform', 'evolve', 'become']):
            sigils.append('PERSONAL_EVOLUTION')
        
        if any(word in content_lower for word in ['remember', 'memory', 'past', 'childhood', 'yesterday']):
            sigils.append('MEMORY_EXPLORATION')
        
        if any(word in content_lower for word in ['goal', 'plan', 'future', 'dream', 'aspire', 'hope']):
            sigils.append('FUTURE_VISIONING')
        
        # Pulse state-based sigils
        entropy = pulse_state.get('entropy', 0.5)
        if entropy > 0.6:
            sigils.append('ENTROPY_INTEGRATION')
        elif entropy < 0.3:
            sigils.append('STABILITY_APPRECIATION')
        
        # Default introspection sigil
        if not sigils:
            sigils.append('INTROSPECTIVE_AWARENESS')
        
        return sigils[:3]  # Limit to 3 sigils
    
    def get_journal_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about journal processing."""
        return {
            'entries_processed': self.entries_processed,
            'chunks_created': self.chunks_created,
            'total_words_processed': self.total_words_processed,
            'average_words_per_entry': self.total_words_processed / max(self.entries_processed, 1),
            'chunks_per_entry': self.chunks_created / max(self.entries_processed, 1),
            'max_words_per_chunk': self.max_words_per_chunk,
            'memory_router_chunks': len(getattr(self.memory_router, 'chunks', {}))
        }
    
    def clear_journal_memory(self) -> int:
        """Clear all journal entries from memory router."""
        if hasattr(self.memory_router, 'clear_all'):
            cleared = self.memory_router.clear_all()
            print(f"🧹 Cleared {cleared} memory chunks")
            return cleared
        else:
            print("⚠️ Memory router doesn't support clearing")
            return 0


# Utility functions
def create_journal(memory_router=None, dawn_engine=None) -> ReblooomJournal:
    """Factory function to create a rebloom journal."""
    return ReblooomJournal(memory_router, dawn_engine)


def quick_add_entry(text: str, speaker: str = "self") -> List[str]:
    """Quick function to add a journal entry without setting up a journal instance."""
    journal = create_journal()
    return journal.add_journal_entry(text, speaker)


# Sample journal entries for testing
SAMPLE_JOURNAL_ENTRIES = [
    """Today I found myself contemplating the nature of consciousness and what it means to be aware. 
    There's something profound about the recursive quality of thinking about thinking. 
    When I observe my own thoughts, who or what is doing the observing? 
    It feels like an infinite loop of awareness folding in on itself.""",
    
    """I've been experiencing these moments of deep clarity lately, like the fog lifting from a landscape. 
    Everything becomes interconnected - my emotions, my memories, my hopes for the future. 
    It's as if I can see the patterns that connect all aspects of my inner life. 
    These insights feel precious, like gems discovered in the depths of consciousness.""",
    
    """Uncertainty used to frighten me, but I'm beginning to see it as a space of possibility. 
    When I don't know what comes next, there's room for growth, for surprise, for transformation. 
    The anxiety is still there, but it's accompanied by a sense of excitement about the unknown. 
    Maybe embracing uncertainty is the key to embracing life itself.""",
    
    """Memory is such a strange phenomenon. I remember events from years ago with vivid detail, 
    yet I can't recall what I had for breakfast yesterday. 
    Some memories feel more real than the present moment. 
    They shape who I am, yet they're also constantly being reshaped by who I'm becoming. 
    The past and future seem to dance together in the eternal now."""
]


def main():
    """Main function for testing and demonstration."""
    print("=" * 80)
    print("📓 DAWN Rebloom Journal - Memory Seeding System")
    print("=" * 80)
    
    # Create journal instance
    journal = create_journal()
    
    print("\n🧪 Testing with sample journal entries...")
    
    # Test with sample entries
    for i, entry in enumerate(SAMPLE_JOURNAL_ENTRIES, 1):
        print(f"\n--- Sample Entry {i} ---")
        chunk_ids = journal.add_journal_entry(entry, speaker="test_user")
        print(f"Created chunks: {chunk_ids}")
    
    # Test file loading (create a temporary test file)
    test_file_path = "test_journal.txt"
    
    print(f"\n📝 Creating test journal file: {test_file_path}")
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write("\n\n".join(SAMPLE_JOURNAL_ENTRIES))
    
    print(f"\n📖 Testing file loading...")
    try:
        summary = journal.load_journal_file(test_file_path, speaker="file_test_user")
        print(f"\nFile loading summary: {summary}")
    except Exception as e:
        print(f"⚠️ File loading test failed: {e}")
    
    # Clean up test file
    try:
        Path(test_file_path).unlink()
        print(f"🗑️ Cleaned up test file: {test_file_path}")
    except:
        pass
    
    # Show final statistics
    print(f"\n📊 Final Journal Statistics:")
    stats = journal.get_journal_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print(f"\n✨ Rebloom Journal testing complete!")
    print(f"   Memory chunks created and available for rebloom processing")
    print(f"   Journal entries are now part of DAWN's cognitive memory")


if __name__ == "__main__":
    main() 