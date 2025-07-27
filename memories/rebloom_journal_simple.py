#!/usr/bin/env python3
"""
DAWN Rebloom Journal - Human Memory Injection Module
Converts human journal entries into MemoryChunk objects for cognitive processing.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
import textwrap

# Import DAWN components with fallbacks
try:
    from memory_router.memory_chunk import MemoryChunk, create_memory_now
    from memory_router.router import MemoryRouter
    from entropy_analyzer import EntropyAnalyzer
    print("✅ DAWN memory components loaded")
    DAWN_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ DAWN components not available: {e}")
    print("🔧 Using mock implementations")
    DAWN_AVAILABLE = False
    
    # Mock implementations for standalone testing
    class MockMemoryChunk:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
            self.timestamp = datetime.now()
    
    class MockMemoryRouter:
        def __init__(self):
            self.chunks = {}
            self.count = 0
        
        def add_chunk(self, chunk):
            chunk_id = f"chunk_{self.count}"
            self.chunks[chunk_id] = chunk
            self.count += 1
            print(f"📝 Mock memory chunk added: {chunk_id}")
            return chunk_id
    
    MemoryChunk = MockMemoryChunk
    MemoryRouter = MockMemoryRouter


class ReblooomJournal:
    """
    Converts human journal entries into DAWN memory chunks.
    Handles text chunking, pulse state capture, and memory injection.
    """
    
    def __init__(self, memory_router: Optional[MemoryRouter] = None):
        """
        Initialize the rebloom journal.
        
        Args:
            memory_router: DAWN MemoryRouter instance (creates new if None)
        """
        self.memory_router = memory_router or MemoryRouter()
        self.chunk_size = 400  # characters
        self.entries_processed = 0
        self.chunks_created = 0
        
        print("📓 ReblooomJournal initialized")
        print(f"   Chunk size: {self.chunk_size} characters")
    
    def add_journal_entry(self, text: str, speaker: str = "self") -> List[str]:
        """
        Add a journal entry to memory, splitting into 400-character chunks.
        
        Args:
            text: Journal entry text
            speaker: Identity of the journal writer
            
        Returns:
            List[str]: List of chunk IDs created
        """
        if not text.strip():
            return []
        
        # Split into chunks
        chunks = self._split_into_chunks(text.strip())
        
        # Get current pulse state
        pulse_state = self._get_pulse_state()
        
        # Create memory chunks
        chunk_ids = []
        for i, chunk_text in enumerate(chunks):
            # Create memory chunk
            if DAWN_AVAILABLE:
                memory_chunk = create_memory_now(
                    speaker=speaker,
                    content=chunk_text,
                    topic="introspection",
                    pulse_state=pulse_state
                )
            else:
                memory_chunk = MemoryChunk(
                    timestamp=datetime.now(),
                    speaker=speaker,
                    content=chunk_text,
                    topic="introspection",
                    pulse_state=pulse_state
                )
            
            # Add to memory router
            chunk_id = self.memory_router.add_chunk(memory_chunk)
            chunk_ids.append(chunk_id)
            self.chunks_created += 1
        
        self.entries_processed += 1
        
        print(f"📝 Journal entry processed: {len(chunks)} chunks from '{speaker}'")
        return chunk_ids
    
    def load_journal_file(self, filepath: str, speaker: str = "self") -> int:
        """
        Load a journal file and process each line as a separate entry.
        
        Args:
            filepath: Path to the journal text file
            speaker: Identity of the journal writer
            
        Returns:
            int: Number of lines processed
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"❌ File not found: {filepath}")
            return 0
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return 0
        
        print(f"📖 Loading journal file: {filepath}")
        print(f"   Found {len(lines)} lines")
        
        lines_processed = 0
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if line:  # Skip empty lines
                try:
                    self.add_journal_entry(line, speaker=speaker)
                    lines_processed += 1
                except Exception as e:
                    print(f"⚠️ Error processing line {line_num}: {e}")
        
        print(f"✅ File processed: {lines_processed} lines → {self.chunks_created} total chunks")
        return lines_processed
    
    def _split_into_chunks(self, text: str) -> List[str]:
        """
        Split text into 400-character chunks, attempting to preserve word boundaries.
        
        Args:
            text: Text to split
            
        Returns:
            List[str]: Text chunks
        """
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        remaining = text
        
        while remaining:
            if len(remaining) <= self.chunk_size:
                chunks.append(remaining)
                break
            
            # Find a good break point near the chunk size
            chunk_end = self.chunk_size
            
            # Try to break at word boundary
            if chunk_end < len(remaining):
                # Look backwards for a space
                while chunk_end > self.chunk_size * 0.8 and remaining[chunk_end] != ' ':
                    chunk_end -= 1
                
                # If no space found, just cut at character limit
                if chunk_end <= self.chunk_size * 0.8:
                    chunk_end = self.chunk_size
            
            chunk = remaining[:chunk_end].strip()
            chunks.append(chunk)
            remaining = remaining[chunk_end:].strip()
        
        return chunks
    
    def _get_pulse_state(self) -> Dict[str, Any]:
        """
        Get current DAWN pulse state for memory chunk metadata.
        
        Returns:
            Dict: Pulse state information
        """
        # Try to get live pulse state from DAWN
        try:
            # Attempt to get real pulse data
            if DAWN_AVAILABLE:
                # This would be the real implementation
                # pulse_zone = pulse.get_zone()
                # entropy = entropy.get_current_entropy()
                # heat = pulse.get_heat()
                pass
        except:
            pass
        
        # Mock pulse state for testing
        import random
        entropy = 0.3 + random.random() * 0.4  # 0.3-0.7 range
        
        return {
            'entropy': entropy,
            'zone': 'CONTEMPLATIVE' if entropy < 0.5 else 'ACTIVE',
            'heat': 25.0 + random.random() * 15.0,  # 25-40 range (calm journaling)
            'focus': 0.7 + random.random() * 0.2,   # High focus during writing
            'timestamp': datetime.now().isoformat()
        }
    
    def get_stats(self) -> Dict[str, int]:
        """Get journal processing statistics."""
        return {
            'entries_processed': self.entries_processed,
            'chunks_created': self.chunks_created,
            'memory_chunks_stored': len(getattr(self.memory_router, 'chunks', {}))
        }


# Global journal instance for convenience
_default_journal = None

def get_default_journal() -> ReblooomJournal:
    """Get or create the default journal instance."""
    global _default_journal
    if _default_journal is None:
        _default_journal = ReblooomJournal()
    return _default_journal


def add_journal_entry(text: str, speaker: str = "self") -> List[str]:
    """
    Convenience function to add a journal entry using the default journal.
    
    Args:
        text: Journal entry text
        speaker: Identity of the journal writer
        
    Returns:
        List[str]: List of chunk IDs created
    """
    journal = get_default_journal()
    return journal.add_journal_entry(text, speaker)


def load_journal_file(filepath: str, speaker: str = "self") -> int:
    """
    Convenience function to load a journal file using the default journal.
    
    Args:
        filepath: Path to the journal text file
        speaker: Identity of the journal writer
        
    Returns:
        int: Number of lines processed
    """
    journal = get_default_journal()
    return journal.load_journal_file(filepath, speaker)


def main():
    """
    Interactive journal input mode.
    Accepts user input and injects into DAWN memory.
    """
    print("=" * 60)
    print("📓 DAWN Rebloom Journal - Interactive Mode")
    print("=" * 60)
    print("Enter journal entries to inject into DAWN memory.")
    print("Commands: 'quit' to exit, 'stats' for statistics")
    print("File loading: 'load <filepath>' to process a file")
    print("-" * 60)
    
    journal = get_default_journal()
    
    try:
        while True:
            try:
                user_input = input("Journal > ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                elif user_input.lower() == 'stats':
                    stats = journal.get_stats()
                    print(f"📊 Statistics:")
                    for key, value in stats.items():
                        print(f"   {key}: {value}")
                    continue
                
                elif user_input.lower().startswith('load '):
                    filepath = user_input[5:].strip()
                    if filepath:
                        journal.load_journal_file(filepath)
                    else:
                        print("❌ Please specify a file path: load <filepath>")
                    continue
                
                # Process as journal entry
                chunk_ids = journal.add_journal_entry(user_input)
                
                if chunk_ids:
                    print(f"✅ Memory injected: {len(chunk_ids)} chunks created")
                else:
                    print("⚠️ No chunks created (empty entry?)")
                
            except KeyboardInterrupt:
                print("\n👋 Exiting journal mode...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    finally:
        # Show final stats
        stats = journal.get_stats()
        print(f"\n📊 Final Statistics:")
        print(f"   Entries processed: {stats['entries_processed']}")
        print(f"   Memory chunks created: {stats['chunks_created']}")
        print(f"   Total chunks in memory: {stats['memory_chunks_stored']}")
        print("\n✨ Journal session complete - memories ready for rebloom!")


if __name__ == "__main__":
    main() 