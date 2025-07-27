"""
DAWN Memory Loader - JSON Lines Memory Import/Export
Handles loading and saving memory chunks from/to JSONL format.
Integrated with DAWN's existing memory infrastructure.
"""

import json
import os
import threading
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any, Generator
from pathlib import Path

from .memory_chunk import MemoryChunk
from .memory_trace_log import EnhancedMemoryTraceLog

logger = logging.getLogger(__name__)

# Thread-safe file operations
_file_lock = threading.Lock()


class DAWNMemoryLoader:
    """
    DAWN-integrated memory loader with JSON Lines support.
    Connects with existing memory trace and anchor systems.
    """
    
    def __init__(self, memories_dir: str = "memories", trace_log: Optional[EnhancedMemoryTraceLog] = None):
        """
        Initialize the memory loader.
        
        Args:
            memories_dir: Directory for memory storage
            trace_log: Optional existing trace log system
        """
        self.memories_dir = Path(memories_dir)
        self.memories_dir.mkdir(exist_ok=True, parents=True)
        
        # Integration with existing DAWN memory systems
        self.trace_log = trace_log
        self.loaded_chunks_count = 0
        self.failed_loads_count = 0
        
        logger.info(f"Initialized DAWNMemoryLoader at {self.memories_dir}")
    
    def load_memory_from_json(self, filepath: str) -> List[MemoryChunk]:
        """
        Load memory chunks from a JSON Lines (.jsonl) file.
        
        Args:
            filepath: Path to the .jsonl file
            
        Returns:
            List[MemoryChunk]: List of loaded memory chunks
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If JSON parsing fails
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"Memory file not found: {filepath}")
        
        chunks = []
        failed_lines = []
        
        logger.info(f"🧠 Loading memories from {filepath}...")
        
        with _file_lock:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue
                    
                    try:
                        # Parse JSON line
                        data = json.loads(line)
                        
                        # Create MemoryChunk from data
                        chunk = MemoryChunk.from_dict(data)
                        chunks.append(chunk)
                        
                        # Integrate with DAWN trace system
                        if self.trace_log:
                            self._integrate_with_trace_log(chunk)
                        
                    except json.JSONDecodeError as e:
                        failed_lines.append((line_num, f"JSON decode error: {e}"))
                        logger.warning(f"⚠️ Failed to parse line {line_num}: {e}")
                        self.failed_loads_count += 1
                        
                    except KeyError as e:
                        failed_lines.append((line_num, f"Missing required field: {e}"))
                        logger.warning(f"⚠️ Missing field on line {line_num}: {e}")
                        self.failed_loads_count += 1
                        
                    except Exception as e:
                        failed_lines.append((line_num, f"Unexpected error: {e}"))
                        logger.warning(f"⚠️ Error on line {line_num}: {e}")
                        self.failed_loads_count += 1
        
        self.loaded_chunks_count += len(chunks)
        logger.info(f"✅ Loaded {len(chunks)} memory chunks")
        if failed_lines:
            logger.warning(f"⚠️ Failed to load {len(failed_lines)} lines")
        
        return chunks
    
    def save_memory_to_json(self, chunks: List[MemoryChunk], filepath: str) -> None:
        """
        Save memory chunks to a JSON Lines (.jsonl) file.
        
        Args:
            chunks: List of memory chunks to save
            filepath: Path where to save the file
        """
        filepath = Path(filepath)
        # Ensure directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"💾 Saving {len(chunks)} memories to {filepath}...")
        
        with _file_lock:
            with open(filepath, 'w', encoding='utf-8') as file:
                for chunk in chunks:
                    json_data = chunk.to_dict()
                    json_line = json.dumps(json_data, separators=(',', ':'))
                    file.write(json_line + '\n')
        
        logger.info(f"✅ Saved memory chunks to {filepath}")
    
    def load_memory_stream(self, filepath: str) -> Generator[MemoryChunk, None, None]:
        """
        Stream memory chunks from a JSON Lines file without loading all into memory.
        Useful for large memory files.
        
        Args:
            filepath: Path to the .jsonl file
            
        Yields:
            MemoryChunk: Individual memory chunks
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"Memory file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    data = json.loads(line)
                    chunk = MemoryChunk.from_dict(data)
                    
                    # Integrate with DAWN trace system
                    if self.trace_log:
                        self._integrate_with_trace_log(chunk)
                    
                    yield chunk
                    
                except Exception as e:
                    logger.warning(f"⚠️ Skipping line {line_num}: {e}")
                    continue
    
    def append_memory_to_json(self, chunk: MemoryChunk, filepath: str) -> None:
        """
        Append a single memory chunk to an existing JSON Lines file.
        
        Args:
            chunk: Memory chunk to append
            filepath: Path to the .jsonl file
        """
        filepath = Path(filepath)
        # Ensure directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with _file_lock:
            with open(filepath, 'a', encoding='utf-8') as file:
                json_data = chunk.to_dict()
                json_line = json.dumps(json_data, separators=(',', ':'))
                file.write(json_line + '\n')
        
        logger.debug(f"Appended memory chunk {chunk.memory_id} to {filepath}")
    
    def filter_memories(
        self,
        chunks: List[MemoryChunk],
        speaker: Optional[str] = None,
        topic: Optional[str] = None,
        content_contains: Optional[str] = None,
        min_entropy: Optional[float] = None,
        max_entropy: Optional[float] = None,
        min_heat: Optional[float] = None,
        max_heat: Optional[float] = None,
        has_sigil: Optional[str] = None,
        mood: Optional[str] = None,
        after_date: Optional[datetime] = None,
        before_date: Optional[datetime] = None
    ) -> List[MemoryChunk]:
        """
        Filter memory chunks based on various criteria.
        Enhanced with DAWN-specific filters.
        
        Args:
            chunks: List of memory chunks to filter
            speaker: Filter by speaker identity
            topic: Filter by topic
            content_contains: Filter by content substring (case-insensitive)
            min_entropy: Minimum entropy threshold
            max_entropy: Maximum entropy threshold
            min_heat: Minimum heat threshold
            max_heat: Maximum heat threshold
            has_sigil: Filter by presence of specific sigil
            mood: Filter by mood state
            after_date: Only memories after this date
            before_date: Only memories before this date
            
        Returns:
            List[MemoryChunk]: Filtered memory chunks
        """
        filtered = []
        
        for chunk in chunks:
            # Apply all filters using the chunk's matches_filter method
            filter_criteria = {}
            
            if speaker:
                filter_criteria['speaker'] = speaker
            if topic:
                filter_criteria['topic'] = topic
            if content_contains:
                filter_criteria['content_contains'] = content_contains
            if min_entropy is not None:
                filter_criteria['min_entropy'] = min_entropy
            if max_entropy is not None:
                filter_criteria['max_entropy'] = max_entropy
            if min_heat is not None:
                filter_criteria['min_heat'] = min_heat
            if max_heat is not None:
                filter_criteria['max_heat'] = max_heat
            if has_sigil:
                filter_criteria['has_sigil'] = has_sigil
            if mood:
                filter_criteria['mood'] = mood
            
            # Check basic filters
            if not chunk.matches_filter(**filter_criteria):
                continue
            
            # Check date filters
            if after_date and chunk.timestamp < after_date:
                continue
            if before_date and chunk.timestamp > before_date:
                continue
            
            filtered.append(chunk)
        
        logger.debug(f"Filtered {len(chunks)} chunks to {len(filtered)} matching criteria")
        return filtered
    
    def merge_memory_files(self, input_files: List[str], output_file: str) -> None:
        """
        Merge multiple memory JSON Lines files into a single file.
        
        Args:
            input_files: List of input .jsonl file paths
            output_file: Output file path
        """
        all_chunks = []
        
        for filepath in input_files:
            try:
                chunks = self.load_memory_from_json(filepath)
                all_chunks.extend(chunks)
                logger.info(f"📁 Merged {len(chunks)} chunks from {filepath}")
            except Exception as e:
                logger.error(f"⚠️ Failed to load {filepath}: {e}")
        
        # Sort by timestamp
        all_chunks.sort(key=lambda x: x.timestamp)
        
        self.save_memory_to_json(all_chunks, output_file)
        logger.info(f"🔗 Merged {len(all_chunks)} total chunks into {output_file}")
    
    def validate_memory_file(self, filepath: str) -> Dict[str, Any]:
        """
        Validate a memory JSON Lines file and return statistics.
        
        Args:
            filepath: Path to the .jsonl file
            
        Returns:
            dict: Validation results and statistics
        """
        filepath = Path(filepath)
        results = {
            'file_exists': filepath.exists(),
            'total_lines': 0,
            'valid_chunks': 0,
            'invalid_lines': [],
            'speakers': set(),
            'topics': set(),
            'moods': set(),
            'sigils': set(),
            'date_range': None,
            'entropy_range': None,
            'heat_range': None,
            'errors': []
        }
        
        if not results['file_exists']:
            results['errors'].append(f"File not found: {filepath}")
            return results
        
        try:
            chunks = []
            entropies = []
            heats = []
            
            with open(filepath, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    results['total_lines'] += 1
                    line = line.strip()
                    
                    if not line:
                        continue
                    
                    try:
                        data = json.loads(line)
                        chunk = MemoryChunk.from_dict(data)
                        chunks.append(chunk)
                        results['valid_chunks'] += 1
                        
                        # Collect statistics
                        results['speakers'].add(chunk.speaker)
                        if chunk.topic:
                            results['topics'].add(chunk.topic)
                        results['moods'].add(chunk.get_mood())
                        results['sigils'].update(chunk.sigils)
                        
                        entropies.append(chunk.get_entropy())
                        heats.append(chunk.get_heat())
                        
                    except Exception as e:
                        results['invalid_lines'].append((line_num, str(e)))
            
            if chunks:
                results['date_range'] = (
                    min(chunk.timestamp for chunk in chunks),
                    max(chunk.timestamp for chunk in chunks)
                )
                
                if entropies:
                    results['entropy_range'] = (min(entropies), max(entropies))
                if heats:
                    results['heat_range'] = (min(heats), max(heats))
            
            # Convert sets to lists for JSON serialization
            results['speakers'] = list(results['speakers'])
            results['topics'] = list(results['topics'])
            results['moods'] = list(results['moods'])
            results['sigils'] = list(results['sigils'])
            
        except Exception as e:
            results['errors'].append(f"File reading error: {e}")
        
        return results
    
    def _integrate_with_trace_log(self, chunk: MemoryChunk) -> None:
        """
        Integrate memory chunk with DAWN's trace log system.
        
        Args:
            chunk: Memory chunk to integrate
        """
        try:
            if self.trace_log and hasattr(self.trace_log, 'log_memory_event'):
                trace_data = chunk.to_memory_trace()
                self.trace_log.log_memory_event(trace_data)
                chunk.traced = True
                logger.debug(f"Integrated chunk {chunk.memory_id} with trace log")
        except Exception as e:
            logger.warning(f"Failed to integrate chunk {chunk.memory_id} with trace log: {e}")
    
    def create_from_dawn_interaction(
        self,
        speaker: str,
        content: str,
        topic: Optional[str] = None,
        pulse_data: Optional[Dict[str, Any]] = None,
        sigils: Optional[List[str]] = None,
        save_to_file: Optional[str] = None
    ) -> MemoryChunk:
        """
        Create a memory chunk from a DAWN interaction and optionally save it.
        
        Args:
            speaker: Identity of the speaker
            content: Content of the interaction
            topic: Optional topic/category
            pulse_data: Current pulse system state
            sigils: Active sigils during interaction
            save_to_file: Optional file to append the memory to
            
        Returns:
            MemoryChunk: Created memory chunk
        """
        from .memory_chunk import create_memory_now
        
        chunk = create_memory_now(
            speaker=speaker,
            content=content,
            topic=topic,
            pulse_state=pulse_data or {},
            sigils=sigils or []
        )
        
        # Integrate with trace system
        if self.trace_log:
            self._integrate_with_trace_log(chunk)
        
        # Save to file if requested
        if save_to_file:
            self.append_memory_to_json(chunk, save_to_file)
        
        logger.info(f"Created memory chunk from DAWN interaction: {chunk.summary()}")
        return chunk
    
    def get_stats(self) -> Dict[str, Any]:
        """Get loader statistics."""
        return {
            'loaded_chunks_count': self.loaded_chunks_count,
            'failed_loads_count': self.failed_loads_count,
            'memories_directory': str(self.memories_dir),
            'trace_log_connected': self.trace_log is not None
        }


# Convenience functions for DAWN integration
def load_dawn_memories(filepath: str) -> List[MemoryChunk]:
    """Load memories from JSON Lines file."""
    loader = DAWNMemoryLoader()
    return loader.load_memory_from_json(filepath)


def save_dawn_memories(chunks: List[MemoryChunk], filepath: str) -> None:
    """Save memories to JSON Lines file."""
    loader = DAWNMemoryLoader()
    loader.save_memory_to_json(chunks, filepath)


def create_test_memory_file(filepath: str = "memories/test_memories.jsonl") -> List[MemoryChunk]:
    """Create a test memory file with sample DAWN data."""
    
    test_chunks = [
        MemoryChunk(
            timestamp=datetime(2025, 1, 24, 15, 30, 0),
            speaker="j.orloff",
            topic="introspection",
            content="The system achieved stable entropy after the recent fluctuations.",
            pulse_state={"entropy": 0.47, "heat": 25.1, "scup": 0.65, "mood": "contemplative"},
            sigils=["STABILIZE_PROTOCOL"]
        ),
        MemoryChunk(
            timestamp=datetime(2025, 1, 24, 15, 32, 15),
            speaker="dawn.core",
            topic="system_event",
            content="Owl bridge recommended stabilization due to entropy threshold breach.",
            pulse_state={"entropy": 0.83, "heat": 45.7, "scup": 0.42, "focus": 0.62, "mood": "analytical"},
            sigils=["STABILIZE_PROTOCOL", "OWL_SUGGESTION"]
        ),
        MemoryChunk(
            timestamp=datetime(2025, 1, 24, 15, 35, 42),
            speaker="j.orloff",
            topic="reflection",
            content="The recursive nature of consciousness becomes apparent in moments of stillness.",
            pulse_state={"entropy": 0.23, "heat": 22.8, "scup": 0.91, "focus": 0.91, "mood": "reflective"},
            sigils=[]
        )
    ]
    
    loader = DAWNMemoryLoader()
    loader.save_memory_to_json(test_chunks, filepath)
    return test_chunks


if __name__ == "__main__":
    print("🧠 DAWN Memory Loader Test:")
    print("=" * 50)
    
    # Create test file
    test_file = "memories/test_memories.jsonl"
    test_chunks = create_test_memory_file(test_file)
    
    # Test loading
    loader = DAWNMemoryLoader()
    loaded_chunks = loader.load_memory_from_json(test_file)
    
    print(f"\nLoaded {len(loaded_chunks)} chunks:")
    for chunk in loaded_chunks:
        print(f"  {chunk.summary()}")
    
    # Test filtering
    print(f"\nFiltering by speaker 'j.orloff':")
    filtered = loader.filter_memories(loaded_chunks, speaker="j.orloff")
    for chunk in filtered:
        print(f"  {chunk.summary()}")
    
    # Test validation
    print(f"\nValidation results:")
    validation = loader.validate_memory_file(test_file)
    for key, value in validation.items():
        if key not in ['speakers', 'topics', 'moods', 'sigils']:  # Skip verbose lists
            print(f"  {key}: {value}")
    
    # Show stats
    print(f"\nLoader statistics:")
    stats = loader.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Cleanup
    os.remove(test_file)
    print(f"\n🗑️ Cleaned up test file: {test_file}") 