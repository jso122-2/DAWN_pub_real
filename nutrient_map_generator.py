#!/usr/bin/env python3
"""
DAWN Nutrient Map Generator v1.0
═══════════════════════════════════════

Memory that is accessed grows roots. 
Memory that is left alone grows quiet. 
This map is not a performance report — it is a health scan.

Generates semantic "nutrient density" maps showing pressure, memory access,
rebloom activity, and lineage flow around each semantic node in DAWN's field.
"""

import json
import csv
import os
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Optional
import math
from pathlib import Path

# Optional matplotlib for heatmap generation
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class NutrientMapGenerator:
    """Generates nutrient density maps for DAWN's bloom nodes."""
    
    def __init__(self, base_path: str = "memory/mycelium/nutrient_map"):
        """
        Initialize the nutrient map generator.
        
        Args:
            base_path: Base directory for output files
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Decay parameters
        self.time_decay_factor = 0.01  # How fast nutrients fade without access
        self.overgrowth_threshold = 50  # Access count above which becomes overgrown
        self.dormancy_threshold = 5     # Ticks without access before dormant
        
    def calculate_nutrient_score(self, 
                               access_count: int,
                               rebloom_count: int,
                               entropy: float,
                               last_access_tick: int,
                               current_tick: int) -> float:
        """
        Calculate the nutrient density score for a bloom node.
        
        Formula: weighted average of access + rebloom - entropy - time decay
        
        Args:
            access_count: How many times bloom was activated
            rebloom_count: Number of rebloom events
            entropy: Entropy value (0.0 to 1.0)
            last_access_tick: Last access timestamp
            current_tick: Current timestamp
            
        Returns:
            Nutrient score (normalized 0.0 to 1.0)
        """
        # Time decay calculation
        ticks_since_access = current_tick - last_access_tick
        time_decay = 1.0 / (1.0 + self.time_decay_factor * ticks_since_access)
        
        # Weighted components
        access_weight = 0.4
        rebloom_weight = 0.3
        entropy_weight = 0.2
        time_weight = 0.1
        
        # Normalize access count (sigmoid to handle large values)
        normalized_access = 2.0 / (1.0 + math.exp(-access_count / 10)) - 1.0
        
        # Normalize rebloom count
        normalized_rebloom = min(rebloom_count / 5.0, 1.0)
        
        # Calculate score
        score = (
            access_weight * normalized_access +
            rebloom_weight * normalized_rebloom +
            entropy_weight * (1.0 - entropy) +  # Lower entropy = higher nutrients
            time_weight * time_decay
        )
        
        return max(0.0, min(1.0, score))  # Clamp to [0, 1]
    
    def determine_status(self, 
                        nutrient_score: float,
                        access_count: int,
                        last_access_tick: int,
                        current_tick: int) -> str:
        """
        Determine the health status of a bloom node.
        
        Args:
            nutrient_score: Calculated nutrient score
            access_count: Total access count
            last_access_tick: Last access timestamp
            current_tick: Current timestamp
            
        Returns:
            Status string: "active", "dormant", "overgrown", or "fading"
        """
        ticks_since_access = current_tick - last_access_tick
        
        if access_count > self.overgrowth_threshold:
            return "overgrown"
        elif ticks_since_access > self.dormancy_threshold:
            if nutrient_score < 0.2:
                return "fading"
            else:
                return "dormant"
        elif nutrient_score > 0.6:
            return "active"
        else:
            return "dormant"
    
    def process_blooms(self, blooms: List[Dict], current_tick: Optional[int] = None) -> List[Dict]:
        """
        Process a list of bloom nodes and calculate their nutrient metrics.
        
        Args:
            blooms: List of bloom dictionaries with required fields
            current_tick: Current timestamp (defaults to current time)
            
        Returns:
            List of processed bloom data with nutrient metrics
        """
        if current_tick is None:
            current_tick = int(datetime.now(timezone.utc).timestamp())
        
        processed_blooms = []
        
        for bloom in blooms:
            # Calculate nutrient score
            nutrient_score = self.calculate_nutrient_score(
                bloom['access_count'],
                bloom['rebloom_count'],
                bloom['entropy'],
                bloom['last_access_tick'],
                current_tick
            )
            
            # Determine status
            status = self.determine_status(
                nutrient_score,
                bloom['access_count'],
                bloom['last_access_tick'],
                current_tick
            )
            
            # Create enriched bloom data
            enriched_bloom = {
                **bloom,
                'nutrient_score': round(nutrient_score, 4),
                'status': status,
                'processed_at': current_tick
            }
            
            processed_blooms.append(enriched_bloom)
        
        return processed_blooms
    
    def write_hourly_csv(self, processed_blooms: List[Dict]):
        """Write processed bloom data to hourly CSV file."""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H")
        csv_path = self.base_path / f"hourly_{timestamp}.csv"
        
        fieldnames = [
            'bloom_id', 'semantic_region', 'access_count', 'rebloom_count',
            'entropy', 'nutrient_score', 'status', 'last_access_tick', 'processed_at'
        ]
        
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for bloom in processed_blooms:
                row = {field: bloom.get(field, '') for field in fieldnames}
                writer.writerow(row)
        
        return csv_path
    
    def write_daily_summary(self, processed_blooms: List[Dict]):
        """Generate and write daily summary JSON."""
        # Group by semantic region
        regions = {}
        for bloom in processed_blooms:
            region = bloom['semantic_region']
            if region not in regions:
                regions[region] = {
                    'blooms': [],
                    'total_access': 0,
                    'total_rebloom': 0,
                    'avg_entropy': 0,
                    'avg_nutrient_score': 0,
                    'status_counts': {'active': 0, 'dormant': 0, 'overgrown': 0, 'fading': 0}
                }
            
            regions[region]['blooms'].append(bloom['bloom_id'])
            regions[region]['total_access'] += bloom['access_count']
            regions[region]['total_rebloom'] += bloom['rebloom_count']
            regions[region]['avg_entropy'] += bloom['entropy']
            regions[region]['avg_nutrient_score'] += bloom['nutrient_score']
            regions[region]['status_counts'][bloom['status']] += 1
        
        # Calculate averages
        for region, data in regions.items():
            bloom_count = len(data['blooms'])
            data['avg_entropy'] = round(data['avg_entropy'] / bloom_count, 4)
            data['avg_nutrient_score'] = round(data['avg_nutrient_score'] / bloom_count, 4)
            data['bloom_count'] = bloom_count
        
        # Create summary
        summary = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'total_blooms': len(processed_blooms),
            'regions': regions,
            'overall_stats': {
                'avg_nutrient_score': round(
                    sum(b['nutrient_score'] for b in processed_blooms) / len(processed_blooms), 4
                ),
                'status_distribution': {
                    status: sum(1 for b in processed_blooms if b['status'] == status)
                    for status in ['active', 'dormant', 'overgrown', 'fading']
                }
            }
        }
        
        json_path = self.base_path / "daily_summary.json"
        with open(json_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        return json_path
    
    def generate_heatmap(self, processed_blooms: List[Dict], output_path: Optional[str] = None):
        """
        Generate a visual heatmap of bloom activity (requires matplotlib).
        
        Args:
            processed_blooms: List of processed bloom data
            output_path: Path for output image (defaults to base_path/activity_heatmap.png)
        """
        if not MATPLOTLIB_AVAILABLE:
            print("[WARNING] matplotlib not available, skipping heatmap generation")
            return None
        
        if output_path is None:
            output_path = self.base_path / "activity_heatmap.png"
        
        # Group blooms by semantic region
        regions = {}
        for bloom in processed_blooms:
            region = bloom['semantic_region']
            if region not in regions:
                regions[region] = []
            regions[region].append(bloom)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Calculate grid dimensions
        num_regions = len(regions)
        cols = math.ceil(math.sqrt(num_regions))
        rows = math.ceil(num_regions / cols)
        
        # Color map for statuses
        status_colors = {
            'active': '#2ecc71',      # Green
            'dormant': '#95a5a6',     # Gray
            'overgrown': '#e74c3c',  # Red
            'fading': '#f39c12'       # Orange
        }
        
        # Plot each region
        for idx, (region, blooms) in enumerate(regions.items()):
            row = idx // cols
            col = idx % cols
            
            # Calculate region metrics
            avg_nutrient = sum(b['nutrient_score'] for b in blooms) / len(blooms)
            dominant_status = max(
                status_colors.keys(),
                key=lambda s: sum(1 for b in blooms if b['status'] == s)
            )
            
            # Create rectangle for region
            rect = patches.Rectangle(
                (col, rows - row - 1), 1, 1,
                linewidth=2,
                edgecolor='black',
                facecolor=status_colors[dominant_status],
                alpha=avg_nutrient  # Opacity based on nutrient score
            )
            ax.add_patch(rect)
            
            # Add region label
            ax.text(
                col + 0.5, rows - row - 0.5, 
                f"{region[:8]}...\n{len(blooms)} blooms",
                ha='center', va='center',
                fontsize=8, weight='bold'
            )
        
        # Configure plot
        ax.set_xlim(0, cols)
        ax.set_ylim(0, rows)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Add title and legend
        plt.title('DAWN Bloom Activity Heatmap', fontsize=16, weight='bold', pad=20)
        
        # Create legend
        legend_elements = [
            patches.Patch(color=color, label=status.capitalize())
            for status, color in status_colors.items()
        ]
        plt.legend(
            handles=legend_elements,
            loc='center left',
            bbox_to_anchor=(1, 0.5),
            title='Status'
        )
        
        # Add timestamp
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        plt.text(
            0.02, 0.02, f"Generated: {timestamp}",
            transform=fig.transFigure,
            fontsize=8, alpha=0.7
        )
        
        # Save figure
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def generate_full_report(self, blooms: List[Dict], 
                           current_tick: Optional[int] = None,
                           generate_visual: bool = True) -> Dict[str, str]:
        """
        Generate complete nutrient map report with all outputs.
        
        Args:
            blooms: List of bloom data dictionaries
            current_tick: Current timestamp
            generate_visual: Whether to generate heatmap visualization
            
        Returns:
            Dictionary with paths to generated files
        """
        # Process blooms
        processed_blooms = self.process_blooms(blooms, current_tick)
        
        # Generate outputs
        outputs = {
            'csv': str(self.write_hourly_csv(processed_blooms)),
            'json': str(self.write_daily_summary(processed_blooms))
        }
        
        # Generate heatmap if requested
        if generate_visual:
            heatmap_path = self.generate_heatmap(processed_blooms)
            if heatmap_path:
                outputs['heatmap'] = str(heatmap_path)
        
        return outputs


# Example usage and testing
if __name__ == "__main__":
    # Create sample bloom data
    sample_blooms = [
        {
            "bloom_id": "bloom_001",
            "access_count": 25,
            "rebloom_count": 3,
            "semantic_region": "trust_seed_42",
            "entropy": 0.3,
            "last_access_tick": 1000
        },
        {
            "bloom_id": "bloom_002",
            "access_count": 75,  # Overgrown
            "rebloom_count": 8,
            "semantic_region": "trust_seed_42",
            "entropy": 0.8,
            "last_access_tick": 900
        },
        {
            "bloom_id": "bloom_003",
            "access_count": 5,
            "rebloom_count": 0,
            "semantic_region": "emergence_17",
            "entropy": 0.1,
            "last_access_tick": 500  # Fading
        },
        {
            "bloom_id": "bloom_004",
            "access_count": 15,
            "rebloom_count": 2,
            "semantic_region": "emergence_17",
            "entropy": 0.4,
            "last_access_tick": 1005  # Active
        }
    ]
    
    # Generate nutrient map
    generator = NutrientMapGenerator()
    outputs = generator.generate_full_report(sample_blooms, current_tick=1010)
    
    print("DAWN Nutrient Map Generated:")
    for output_type, path in outputs.items():
        print(f"  {output_type}: {path}")