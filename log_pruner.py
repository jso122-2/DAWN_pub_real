#!/usr/bin/env python3
"""
DAWN Log Pruner v1.0
═══════════════════════════════════════

DAWN does not hold on to everything. 
She keeps what sings. She lets go of what has served.

Manages log file lifecycle through intelligent pruning and compression,
preserving semantically important entries while maintaining system hygiene.
"""

import json
import os
import gzip
import shutil
from datetime import datetime, timezone
from typing import Dict, List, Set, Optional, Tuple
from pathlib import Path
import re
from collections import defaultdict


class LogPruner:
    """
    Manages log file pruning and compression based on age, access patterns,
    and semantic retention signals.
    
    Balances between preserving important historical data and preventing
    unbounded growth of log storage.
    """
    
    def __init__(self, report_path: str = "system/logs"):
        """
        Initialize the log pruner.
        
        Args:
            report_path: Directory for pruning reports
        """
        self.report_path = Path(report_path)
        self.report_path.mkdir(parents=True, exist_ok=True)
        
        # Pruning statistics
        self.prune_stats = {
            'total_files_scanned': 0,
            'files_deleted': 0,
            'files_compressed': 0,
            'files_preserved': 0,
            'space_freed_bytes': 0,
            'space_compressed_bytes': 0,
            'keyword_preservations': 0
        }
        
        # Compression settings
        self.compression_suffix = '.gz'
        self.min_size_for_compression = 1024 * 10  # 10KB minimum
    
    def _extract_tick_from_filename(self, filename: str) -> Optional[int]:
        """
        Extract tick number from filename if present.
        
        Args:
            filename: Log filename
            
        Returns:
            Tick number or None if not found
        """
        # Common patterns for tick in filenames
        patterns = [
            r'tick_(\d+)',
            r'epoch_(\d+)',
            r'_(\d{4,})\.(?:json|txt|log)',  # 4+ digit numbers before extension
        ]
        
        for pattern in patterns:
            match = re.search(pattern, filename)
            if match:
                return int(match.group(1))
        
        return None
    
    def _get_file_age_ticks(self, filepath: Path, current_tick: int) -> Optional[int]:
        """
        Calculate file age in ticks.
        
        Args:
            filepath: Path to file
            current_tick: Current system tick
            
        Returns:
            Age in ticks or None if cannot determine
        """
        # Try to extract tick from filename first
        file_tick = self._extract_tick_from_filename(filepath.name)
        
        if file_tick is not None:
            return current_tick - file_tick
        
        # Fall back to file modification time
        # Assume 1 tick = 1 second for conversion (adjust as needed)
        try:
            mtime = filepath.stat().st_mtime
            current_time = datetime.now(timezone.utc).timestamp()
            age_seconds = current_time - mtime
            return int(age_seconds)  # Convert seconds to ticks
        except:
            return None
    
    def _check_preservation_keywords(self, filepath: Path, preserve_keywords: List[str]) -> bool:
        """
        Check if file contains preservation keywords.
        
        Args:
            filepath: Path to file
            preserve_keywords: List of keywords to check
            
        Returns:
            True if file should be preserved
        """
        if not preserve_keywords:
            return False
        
        # Check filename first
        filename_lower = filepath.name.lower()
        for keyword in preserve_keywords:
            if keyword.lower() in filename_lower:
                self.prune_stats['keyword_preservations'] += 1
                return True
        
        # For small files, check content
        try:
            if filepath.stat().st_size < 1024 * 100:  # 100KB limit for content scanning
                if filepath.suffix == '.json':
                    with open(filepath, 'r') as f:
                        content = json.load(f)
                        content_str = json.dumps(content).lower()
                else:
                    with open(filepath, 'r') as f:
                        content_str = f.read().lower()
                
                for keyword in preserve_keywords:
                    if keyword.lower() in content_str:
                        self.prune_stats['keyword_preservations'] += 1
                        return True
        except:
            # If can't read file, err on side of caution
            return True
        
        return False
    
    def _compress_file(self, filepath: Path) -> Optional[Path]:
        """
        Compress a file using gzip.
        
        Args:
            filepath: Path to file to compress
            
        Returns:
            Path to compressed file or None if failed
        """
        compressed_path = filepath.with_suffix(filepath.suffix + self.compression_suffix)
        
        try:
            # Get original size
            original_size = filepath.stat().st_size
            
            # Compress file
            with open(filepath, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb', compresslevel=9) as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Get compressed size
            compressed_size = compressed_path.stat().st_size
            
            # Only keep compression if it saved space
            if compressed_size < original_size * 0.9:  # At least 10% reduction
                # Remove original
                filepath.unlink()
                
                # Update stats
                self.prune_stats['files_compressed'] += 1
                self.prune_stats['space_compressed_bytes'] += original_size - compressed_size
                
                return compressed_path
            else:
                # Remove compressed version, not worth it
                compressed_path.unlink()
                return None
                
        except Exception as e:
            # Clean up on error
            if compressed_path.exists():
                compressed_path.unlink()
            return None
    
    def _delete_file(self, filepath: Path):
        """
        Delete a file and update statistics.
        
        Args:
            filepath: Path to file to delete
        """
        try:
            size = filepath.stat().st_size
            filepath.unlink()
            
            self.prune_stats['files_deleted'] += 1
            self.prune_stats['space_freed_bytes'] += size
        except:
            pass  # File might have been deleted already
    
    def _get_log_files(self, log_path: Path) -> List[Path]:
        """
        Get all log files in directory and subdirectories.
        
        Args:
            log_path: Root log directory
            
        Returns:
            List of log file paths
        """
        log_extensions = {'.log', '.txt', '.json'}
        log_files = []
        
        for ext in log_extensions:
            log_files.extend(log_path.rglob(f'*{ext}'))
            # Also include compressed versions
            log_files.extend(log_path.rglob(f'*{ext}{self.compression_suffix}'))
        
        return log_files
    
    def _save_pruning_report(self, results: Dict):
        """
        Save pruning report to JSON file.
        
        Args:
            results: Pruning results dictionary
        """
        report_data = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'results': results,
            'statistics': self.prune_stats,
            'space_summary': {
                'freed_mb': round(self.prune_stats['space_freed_bytes'] / (1024 * 1024), 2),
                'compressed_saved_mb': round(self.prune_stats['space_compressed_bytes'] / (1024 * 1024), 2)
            }
        }
        
        report_path = self.report_path / "pruning_report.json"
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        # Also save timestamped report
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        archive_path = self.report_path / f"pruning_report_{timestamp}.json"
        with open(archive_path, 'w') as f:
            json.dump(report_data, f, indent=2)
    
    def prune_directory(self, 
                       log_path: str,
                       max_age_ticks: int,
                       max_file_count: int,
                       preserve_keywords: List[str],
                       current_tick: Optional[int] = None) -> Dict:
        """
        Prune logs in a directory based on specified criteria.
        
        Args:
            log_path: Path to log directory
            max_age_ticks: Maximum age in ticks before deletion
            max_file_count: Maximum number of files to keep
            preserve_keywords: Keywords that prevent deletion
            current_tick: Current system tick (auto-generated if None)
            
        Returns:
            Dictionary with pruning results
        """
        log_path = Path(log_path)
        if not log_path.exists():
            return {
                'files_deleted': [],
                'files_compressed': [],
                'skipped': []
            }
        
        # Auto-generate current tick if not provided
        if current_tick is None:
            current_tick = int(datetime.now(timezone.utc).timestamp())
        
        # Get all log files
        log_files = self._get_log_files(log_path)
        self.prune_stats['total_files_scanned'] = len(log_files)
        
        # Track actions
        files_deleted = []
        files_compressed = []
        skipped = []
        
        # Sort files by age (oldest first)
        file_ages = []
        for filepath in log_files:
            age = self._get_file_age_ticks(filepath, current_tick)
            if age is not None:
                file_ages.append((filepath, age))
            else:
                # Can't determine age, skip
                skipped.append(str(filepath))
        
        file_ages.sort(key=lambda x: x[1], reverse=True)  # Oldest first
        
        # Process files
        files_to_keep = []
        
        for filepath, age in file_ages:
            # Check preservation keywords
            if self._check_preservation_keywords(filepath, preserve_keywords):
                skipped.append(str(filepath))
                files_to_keep.append(filepath)
                continue
            
            # Check age threshold
            if age > max_age_ticks:
                self._delete_file(filepath)
                files_deleted.append(str(filepath))
                continue
            
            # File is young enough to potentially keep
            files_to_keep.append(filepath)
        
        # Check file count limit
        if len(files_to_keep) > max_file_count:
            # Sort by age again (keep newest)
            files_to_keep_with_age = []
            for filepath in files_to_keep:
                age = self._get_file_age_ticks(filepath, current_tick)
                if age is not None:
                    files_to_keep_with_age.append((filepath, age))
            
            files_to_keep_with_age.sort(key=lambda x: x[1])  # Newest first
            
            # Keep only max_file_count newest files
            for filepath, _ in files_to_keep_with_age[max_file_count:]:
                # Try to compress before deleting
                if (not filepath.name.endswith(self.compression_suffix) and 
                    filepath.stat().st_size > self.min_size_for_compression):
                    compressed = self._compress_file(filepath)
                    if compressed:
                        files_compressed.append(str(filepath))
                        continue
                
                # Delete if compression failed or not applicable
                self._delete_file(filepath)
                files_deleted.append(str(filepath))
        
        # Mark remaining files as skipped
        for filepath in files_to_keep:
            if (str(filepath) not in files_deleted and 
                str(filepath) not in files_compressed and
                str(filepath) not in skipped):
                skipped.append(str(filepath))
                self.prune_stats['files_preserved'] += 1
        
        return {
            'files_deleted': files_deleted,
            'files_compressed': files_compressed,
            'skipped': skipped
        }


def prune_logs(log_path: str,
              max_age_ticks: int,
              max_file_count: int,
              preserve_keywords: List[str]) -> Dict:
    """
    Prune and compress old log files based on retention criteria.
    
    This function manages log file lifecycle by deleting old files,
    compressing medium-aged files, and preserving semantically important
    entries based on keywords.
    
    Args:
        log_path: Path to log directory to prune
        max_age_ticks: Maximum age in ticks before deletion
        max_file_count: Maximum number of files to keep
        preserve_keywords: List of keywords that prevent deletion
        
    Returns:
        Dictionary containing:
            - files_deleted: List of deleted file paths
            - files_compressed: List of compressed file paths
            - skipped: List of preserved file paths
    """
    # Create pruner instance
    pruner = LogPruner()
    
    # Perform pruning
    results = pruner.prune_directory(
        log_path,
        max_age_ticks,
        max_file_count,
        preserve_keywords
    )
    
    # Save pruning report
    pruner._save_pruning_report(results)
    
    # Add metadata to results
    results['metadata'] = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'statistics': pruner.prune_stats,
        'criteria': {
            'max_age_ticks': max_age_ticks,
            'max_file_count': max_file_count,
            'preserve_keywords': preserve_keywords
        }
    }
    
    return results


# Example usage and testing
if __name__ == "__main__":
    import tempfile
    import time
    
    # Create temporary log directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        log_dir = Path(temp_dir) / "logs"
        log_dir.mkdir()
        
        # Create sample log files
        sample_files = [
            ("entropy_sweep_epoch_1000.txt", "Old entropy sweep log", 1000),
            ("rebloom_events_tick_1500.json", '{"events": ["rebloom1", "rebloom2"]}', 1500),
            ("sacred_memory_log.txt", "This contains sacred memories", 1800),
            ("drift_analysis_tick_2000.json", '{"drift": 0.5}', 2000),
            ("belief_evaluation_20240102_120000.json", '{"beliefs": []}', 2100),
            ("debug_log_tick_2200.txt", "Debug information", 2200),
            ("rebloom_stabilization_tick_2300.json", '{"stabilized": []}', 2300),
            ("token_linkage_map_tick_2400.json", '{"linked_tokens": []}', 2400)
        ]
        
        # Write sample files
        for filename, content, tick in sample_files:
            filepath = log_dir / filename
            with open(filepath, 'w') as f:
                f.write(content)
            # Simulate age by modifying file time
            os.utime(filepath, (time.time() - (2500 - tick), time.time() - (2500 - tick)))
        
        # Run pruning
        results = prune_logs(
            log_path=str(log_dir),
            max_age_ticks=800,  # Delete files older than 800 ticks
            max_file_count=5,   # Keep maximum 5 files
            preserve_keywords=['sacred', 'belief']  # Preserve these
        )
        
        # Display results
        print("LOG PRUNING RESULTS:")
        print("=" * 50)
        print(f"\nFiles Deleted ({len(results['files_deleted'])}):")
        for filepath in results['files_deleted']:
            print(f"  - {Path(filepath).name}")
        
        print(f"\nFiles Compressed ({len(results['files_compressed'])}):")
        for filepath in results['files_compressed']:
            print(f"  - {Path(filepath).name}")
        
        print(f"\nFiles Preserved ({len(results['skipped'])}):")
        for filepath in results['skipped']:
            print(f"  - {Path(filepath).name}")
        
        print(f"\nStatistics: {results['metadata']['statistics']}")