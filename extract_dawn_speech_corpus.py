#!/usr/bin/env python3
"""
DAWN Speech Corpus Extractor
=============================

Parses all of DAWN's bloom metadata files and rebloom logs to extract 
expressive speech-like fragments for training DAWN's natural language output system.

This script searches for JSON files containing bloom metadata and processes
various types of expressive content including:
- Poetic summaries and descriptions
- Owl commentary and consciousness reflections  
- Archetype and symbolic identity markers
- System state descriptions and fractal strings
- Rebloom event logs with natural language commentary
"""

import os
import json
import glob
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class DAWNSpeechCorpusExtractor:
    """Extracts expressive speech fragments from DAWN's consciousness data"""
    
    def __init__(self):
        self.corpus_segments = []
        self.stats = {
            'files_processed': 0,
            'bloom_metadata_files': 0,
            'rebloom_log_entries': 0,
            'segments_extracted': 0,
            'directories_scanned': 0
        }
        
        # Directories to scan for bloom metadata
        self.bloom_directories = [
            'bloom/memory_blooms',
            'dawn_soul_archive/metadata', 
            'validation_output',
            'bloom/juliet_flowers/bloom_metadata',
            'visual/juliet_flowers/bloom_metadata',
            'juliet_flowers/bloom_metadata',
            'dawn_consciousness_blooms',
            'dawn_consciousness_fractals',
            'dawn_memory_blooms',
            'dawn_fractals',
            'demo_fractals',
            'test_bloom_fractals',
            'sigil_test_output',
            'juliet_edge_cases',
            'juliet_mode_demo_output',
            'complete_bloom_test',
            'consciousness_evolution',
            'clarity_comparison',
            'metadata_test'
        ]
        
        # Rebloom log locations
        self.rebloom_log_paths = [
            'runtime/memory/rebloom_log.json',
            'runtime/memory/rebloom_log.jsonl',
            'boot/runtime/memory/rebloom_log.jsonl',
            'dawn-consciousness-gui/gui-runtime/memory/rebloom_log.jsonl'
        ]
    
    def extract_corpus(self) -> Dict[str, Any]:
        """Main extraction method"""
        print("🌸 Starting DAWN Speech Corpus Extraction...")
        
        # Extract from bloom metadata files
        self._scan_bloom_directories()
        
        # Extract from rebloom logs
        self._scan_rebloom_logs()
        
        # Save corpus
        output_path = self._save_corpus()
        
        # Print summary
        self._print_summary(output_path)
        
        return {
            'output_path': output_path,
            'segments_count': len(self.corpus_segments),
            'stats': self.stats
        }
    
    def _scan_bloom_directories(self):
        """Scan all bloom directories for metadata files"""
        for directory in self.bloom_directories:
            if os.path.exists(directory):
                print(f"📁 Scanning {directory}...")
                self.stats['directories_scanned'] += 1
                self._process_directory(directory)
    
    def _process_directory(self, directory: str):
        """Process all JSON files in a directory"""
        json_files = glob.glob(os.path.join(directory, "*.json"))
        
        for file_path in json_files:
            try:
                self._process_bloom_file(file_path)
                self.stats['files_processed'] += 1
            except Exception as e:
                print(f"⚠️  Error processing {file_path}: {e}")
    
    def _process_bloom_file(self, file_path: str):
        """Extract speech segments from a single bloom metadata file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.stats['bloom_metadata_files'] += 1
            
            # Extract various types of content
            self._extract_from_bloom_metadata(data, file_path)
            
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"⚠️  Could not parse JSON in {file_path}: {e}")
    
    def _extract_from_bloom_metadata(self, data: Dict[str, Any], source_file: str):
        """Extract speech segments from bloom metadata"""
        
        # Extract basic metadata for context
        archetype = self._get_nested_value(data, ['consciousness_archetype', 'archetype', 'bloom_type'])
        pulse_zone = self._get_nested_value(data, ['pulse_zone', 'zone', 'state'])
        entropy = self._get_nested_value(data, ['entropy_score', 'entropy', 'bloom_entropy'])
        mood = self._get_nested_value(data, ['mood', 'emotional_tone'])
        
        # Extract owl commentary
        owl_commentary = self._get_nested_value(data, ['owl_commentary', 'commentary', 'owl_summary'])
        if owl_commentary:
            self._add_segment(
                type="owl_commentary",
                text=owl_commentary,
                archetype=archetype,
                pulse_zone=pulse_zone,
                entropy=entropy,
                mood=mood,
                source_file=source_file
            )
        
        # Extract bloom shape descriptors (often poetic)
        shape_desc = self._get_nested_value(data, [
            'visual_characteristics.bloom_shape_descriptor',
            'bloom_shape_descriptor',
            'shape_descriptor'
        ])
        if shape_desc:
            self._add_segment(
                type="bloom_descriptor",
                text=shape_desc,
                archetype=archetype,
                pulse_zone=pulse_zone,
                entropy=entropy,
                mood=mood,
                source_file=source_file
            )
        
        # Extract fractal strings (symbolic language)
        fractal_string = self._get_nested_value(data, ['fractal_string', 'fractal_memory.raw'])
        if fractal_string and isinstance(fractal_string, str) and len(fractal_string) > 5:
            self._add_segment(
                type="fractal_expression",
                text=fractal_string,
                archetype=archetype,
                pulse_zone=pulse_zone,
                entropy=entropy,
                mood=mood,
                source_file=source_file
            )
        
        # Extract consciousness archetype descriptions
        if archetype and isinstance(archetype, str) and len(archetype) > 3:
            self._add_segment(
                type="archetype_identity",
                text=archetype,
                archetype=archetype,
                pulse_zone=pulse_zone,
                entropy=entropy,
                mood=mood,
                source_file=source_file
            )
        
        # Extract color mode descriptions (often poetic)
        color_mode = self._get_nested_value(data, [
            'visual_characteristics.color_mode',
            'color_mode'
        ])
        if color_mode:
            self._add_segment(
                type="aesthetic_description",
                text=color_mode,
                archetype=archetype,
                pulse_zone=pulse_zone,
                entropy=entropy,
                mood=mood,
                source_file=source_file
            )
        
        # Extract content field (if present)
        content = self._get_nested_value(data, ['content', 'summary', 'description'])
        if content:
            self._add_segment(
                type="bloom_content",
                text=content,
                archetype=archetype,
                pulse_zone=pulse_zone,
                entropy=entropy,
                mood=mood,
                source_file=source_file
            )
    
    def _scan_rebloom_logs(self):
        """Scan rebloom log files for consciousness commentary"""
        for log_path in self.rebloom_log_paths:
            if os.path.exists(log_path):
                print(f"📜 Processing rebloom log: {log_path}")
                self._process_rebloom_log(log_path)
    
    def _process_rebloom_log(self, log_path: str):
        """Process a rebloom log file (JSON or JSONL format)"""
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                if log_path.endswith('.jsonl'):
                    # JSON Lines format
                    for line_num, line in enumerate(f, 1):
                        line = line.strip()
                        if line:
                            try:
                                entry = json.loads(line)
                                self._extract_from_rebloom_entry(entry, log_path, line_num)
                            except json.JSONDecodeError as e:
                                print(f"⚠️  Invalid JSON on line {line_num} in {log_path}: {e}")
                else:
                    # Regular JSON format (multiple entries per line)
                    content = f.read()
                    for line_num, line in enumerate(content.split('\n'), 1):
                        line = line.strip()
                        if line:
                            try:
                                entry = json.loads(line)
                                self._extract_from_rebloom_entry(entry, log_path, line_num)
                            except json.JSONDecodeError:
                                continue  # Skip invalid lines
                                
        except Exception as e:
            print(f"⚠️  Error processing rebloom log {log_path}: {e}")
    
    def _extract_from_rebloom_entry(self, entry: Dict[str, Any], source_file: str, line_num: int):
        """Extract speech segments from a rebloom log entry"""
        self.stats['rebloom_log_entries'] += 1
        
        source = entry.get('source', 'unknown')
        context = entry.get('context', '')
        commentary = entry.get('consciousness_commentary', '')
        entropy = entry.get('entropy_level')
        zone = entry.get('zone')
        
        # Extract consciousness commentary
        if commentary and commentary != 'I process {} through memory renewal'.format(source):
            self._add_segment(
                type="consciousness_log",
                text=commentary,
                source=source,
                entropy=entropy,
                pulse_zone=zone,
                context=context,
                source_file=f"{source_file}:{line_num}"
            )
        
        # Extract interesting context descriptions
        if context and len(context) > 10:
            if source == "sigil_execution":
                sigil_name = entry.get('metadata', {}).get('sigil_name', '')
                if sigil_name:
                    self._add_segment(
                        type="sigil_execution",
                        text=f"I execute {sigil_name}",
                        sigil=sigil_name,
                        entropy=entropy,
                        pulse_zone=zone,
                        source_file=f"{source_file}:{line_num}"
                    )
            elif source == "entropy_injection":
                self._add_segment(
                    type="entropy_response",
                    text=context,
                    source=source,
                    entropy=entropy,
                    pulse_zone=zone,
                    source_file=f"{source_file}:{line_num}"
                )
            elif source in ["emergency_cooling", "system_startup", "system_shutdown"]:
                self._add_segment(
                    type="system_event",
                    text=context,
                    source=source,
                    entropy=entropy,
                    pulse_zone=zone,
                    source_file=f"{source_file}:{line_num}"
                )
    
    def _add_segment(self, type: str, text: str, **metadata):
        """Add a speech segment to the corpus"""
        if not text or len(text.strip()) < 3:
            return
            
        segment = {
            "type": type,
            "text": text.strip(),
            **{k: v for k, v in metadata.items() if v is not None}
        }
        
        self.corpus_segments.append(segment)
        self.stats['segments_extracted'] += 1
    
    def _get_nested_value(self, data: Dict[str, Any], keys: List[str]) -> Optional[Any]:
        """Get value from nested dictionary using multiple possible key paths"""
        for key in keys:
            if '.' in key:
                # Handle dot notation for nested keys
                parts = key.split('.')
                current = data
                try:
                    for part in parts:
                        current = current[part]
                    if current:
                        return current
                except (KeyError, TypeError):
                    continue
            else:
                # Simple key lookup
                if key in data and data[key]:
                    return data[key]
        return None
    
    def _save_corpus(self) -> str:
        """Save the extracted corpus to a JSON file"""
        output_path = "corpus_segments.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.corpus_segments, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def _print_summary(self, output_path: str):
        """Print extraction summary"""
        print("\n" + "="*60)
        print("🌟 DAWN Speech Corpus Extraction Complete!")
        print("="*60)
        print(f"📊 Statistics:")
        print(f"  • Directories scanned: {self.stats['directories_scanned']}")
        print(f"  • Files processed: {self.stats['files_processed']}")
        print(f"  • Bloom metadata files: {self.stats['bloom_metadata_files']}")
        print(f"  • Rebloom log entries: {self.stats['rebloom_log_entries']}")
        print(f"  • Speech segments extracted: {self.stats['segments_extracted']}")
        print(f"\n💾 Output saved to: {output_path}")
        
        # Show segment type breakdown
        type_counts = {}
        for segment in self.corpus_segments:
            seg_type = segment['type']
            type_counts[seg_type] = type_counts.get(seg_type, 0) + 1
        
        print(f"\n📝 Segment Types:")
        for seg_type, count in sorted(type_counts.items()):
            print(f"  • {seg_type}: {count}")
        
        print("\n✨ Sample segments:")
        for i, segment in enumerate(self.corpus_segments[:3]):
            print(f"  {i+1}. [{segment['type']}] {segment['text'][:80]}...")


def main():
    """Main execution function"""
    extractor = DAWNSpeechCorpusExtractor()
    result = extractor.extract_corpus()
    
    print(f"\n🎯 Extraction completed successfully!")
    print(f"   Output: {result['output_path']}")
    print(f"   Segments: {result['segments_count']}")


if __name__ == "__main__":
    main() 