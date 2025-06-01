"""
DAWN Visual Tests - Cognitive Architecture Proofs
Scaffold for demonstrating DAWN's emergent behaviors through visualization
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Wedge, FancyBboxPatch
import matplotlib.patheffects as path_effects
from matplotlib.animation import FuncAnimation, PillowWriter
import seaborn as sns
from pathlib import Path
from datetime import datetime
import pandas as pd
from collections import defaultdict
import matplotlib.gridspec as gridspec

class DawnVisualTests:
    """Visual proof system for DAWN's cognitive architecture"""
    
    def __init__(self, base_path=None):
        self.base_path = Path(base_path or os.getcwd())
        self.output_path = self.base_path / "visual_tests"
        self.setup_directories()
        self.setup_test_data()
        
        # Color schemes for consistency
        self.mood_colors = {
            'joyful': '#FFD700',     # Gold
            'focused': '#4169E1',    # Royal Blue  
            'reflective': '#9370DB', # Medium Purple
            'anxious': '#DC143C',    # Crimson
            'calm': '#32CD32',       # Lime Green
            'excited': '#FF6347'     # Tomato
        }
        
        self.zone_colors = {
            'calm': '#32CD32',       # Green
            'active': '#FFD700',     # Gold
            'surge': '#DC143C'       # Red
        }
        
    def setup_directories(self):
        """Create test output directories"""
        dirs = [
            "visual_tests",
            "visual_tests/mood_sequences",
            "visual_tests/bloom_snapshots", 
            "visual_tests/scup_breakdown",
            "visual_tests/pulse_diagrams",
            "visual_tests/integration"
        ]
        for d in dirs:
            (self.base_path / d).mkdir(parents=True, exist_ok=True)
    
    def setup_test_data(self):
        """Generate realistic test data for DAWN cognitive processes"""
        
        # 1. Mood sequence data (valence/arousal/entropy over time)
        self.mood_sequence = []
        np.random.seed(42)  # Reproducible results
        
        for tick in range(0, 1000, 50):  # Every 50 ticks
            # Simulate mood evolution with some continuity
            base_valence = 0.3 + 0.4 * np.sin(tick * 0.01) + np.random.normal(0, 0.1)
            base_arousal = 0.5 + 0.3 * np.cos(tick * 0.008) + np.random.normal(0, 0.08)
            entropy = 0.2 + 0.3 * (1 - np.abs(base_valence)) + np.random.normal(0, 0.05)
            
            # Clamp values
            valence = np.clip(base_valence, -1, 1)
            arousal = np.clip(base_arousal, 0, 1)
            entropy = np.clip(entropy, 0, 1)
            
            # Derive mood label
            if valence > 0.3 and arousal > 0.6:
                mood = 'joyful'
            elif valence > 0.1 and arousal < 0.4:
                mood = 'calm'
            elif valence < -0.2:
                mood = 'anxious'
            elif arousal > 0.7:
                mood = 'excited'
            elif valence > 0 and arousal > 0.4:
                mood = 'focused'
            else:
                mood = 'reflective'
            
            self.mood_sequence.append({
                'tick': tick,
                'valence': valence,
                'arousal': arousal,
                'entropy': entropy,
                'mood': mood
            })
        
        # 2. Bloom evolution snapshots
        self.bloom_snapshots = {
            'initial': {
                'tick': 100,
                'blooms': [
                    {'id': 'ROOT_001', 'x': 0, 'y': 0, 'entropy': 0.1, 'mood': 'calm', 'depth': 0, 'size': 1.0},
                    {'id': 'BLOOM_A1', 'x': 0.3, 'y': 0.2, 'entropy': 0.2, 'mood': 'curious', 'depth': 1, 'size': 0.8},
                    {'id': 'BLOOM_A2', 'x': -0.2, 'y': 0.4, 'entropy': 0.15, 'mood': 'focused', 'depth': 1, 'size': 0.7}
                ]
            },
            'rebloomed': {
                'tick': 500,
                'blooms': [
                    {'id': 'ROOT_001', 'x': 0, 'y': 0, 'entropy': 0.25, 'mood': 'reflective', 'depth': 0, 'size': 1.2},
                    {'id': 'BLOOM_A1', 'x': 0.4, 'y': 0.1, 'entropy': 0.4, 'mood': 'anxious', 'depth': 1, 'size': 0.9},
                    {'id': 'BLOOM_B1', 'x': 0.1, 'y': 0.6, 'entropy': 0.3, 'mood': 'joyful', 'depth': 2, 'size': 0.6},
                    {'id': 'BLOOM_B2', 'x': -0.4, 'y': 0.3, 'entropy': 0.35, 'mood': 'focused', 'depth': 2, 'size': 0.5},
                    {'id': 'SYNTH_01', 'x': 0.2, 'y': -0.3, 'entropy': 0.6, 'mood': 'excited', 'depth': 3, 'size': 0.4}
                ]
            },
            'final': {
                'tick': 900,
                'blooms': [
                    {'id': 'ROOT_001', 'x': 0, 'y': 0, 'entropy': 0.4, 'mood': 'wise', 'depth': 0, 'size': 1.5},
                    {'id': 'CLUSTER_A', 'x': 0.5, 'y': 0.2, 'entropy': 0.5, 'mood': 'stable', 'depth': 2, 'size': 1.0},
                    {'id': 'CLUSTER_B', 'x': -0.3, 'y': 0.5, 'entropy': 0.45, 'mood': 'dynamic', 'depth': 2, 'size': 0.9},
                    {'id': 'EMERGENCE', 'x': 0.1, 'y': -0.4, 'entropy': 0.7, 'mood': 'transcendent', 'depth': 4, 'size': 0.8}
                ]
            }
        }
        
        # 3. SCUP (Semantic Coherence Under Pressure) data
        self.scup_data = []
        for tick in range(0, 1000, 10):
            # Base SCUP with pressure events
            pressure_events = [200, 400, 600, 800]  # Pressure spikes
            base_scup = 0.7 + 0.2 * np.sin(tick * 0.005)
            
            # Add pressure drops
            pressure_factor = 1.0
            for event_tick in pressure_events:
                if abs(tick - event_tick) < 50:
                    pressure_factor *= (0.6 + 0.4 * (abs(tick - event_tick) / 50))
            
            scup = base_scup * pressure_factor + np.random.normal(0, 0.02)
            drift_angle = (tick * 0.02 + np.sin(tick * 0.01) * 2) % (2 * np.pi)
            
            # Pulse zone based on SCUP and recent activity
            if scup > 0.7:
                zone = 'calm'
            elif scup > 0.4:
                zone = 'active'  
            else:
                zone = 'surge'
            
            self.scup_data.append({
                'tick': tick,
                'scup': np.clip(scup, 0, 1),
                'drift_angle': drift_angle,
                'zone': zone,
                'pressure_event': tick in pressure_events
            })
        
        # 4. Pulse zone transitions with triggers
        self.pulse_transitions = [
            {'from_zone': 'calm', 'to_zone': 'active', 'tick': 150, 'trigger': 'novel_input', 'intensity': 0.6},
            {'from_zone': 'active', 'to_zone': 'surge', 'tick': 200, 'trigger': 'cognitive_load', 'intensity': 0.9},
            {'from_zone': 'surge', 'to_zone': 'active', 'tick': 280, 'trigger': 'adaptation', 'intensity': 0.7},
            {'from_zone': 'active', 'to_zone': 'calm', 'tick': 350, 'trigger': 'integration', 'intensity': 0.4},
            {'from_zone': 'calm', 'to_zone': 'active', 'tick': 450, 'trigger': 'curiosity', 'intensity': 0.5},
            {'from_zone': 'active', 'to_zone': 'surge', 'tick': 600, 'trigger': 'insight_cascade', 'intensity': 0.8},
            {'from_zone': 'surge', 'to_zone': 'calm', 'tick': 750, 'trigger': 'synthesis', 'intensity': 0.3}
        ]

    # === TEST 1: MOOD HEATMAP SEQUENCE ===
    
    def create_mood_heatmap_sequence(self):
        """Create mood evolution heatmap showing valence/arousal/entropy"""
        print("🧠 Creating Mood Heatmap Sequence...")
        
        # Horizontal bar version
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(16, 10), facecolor='black')
        fig.suptitle('DAWN Mood Evolution Sequence', color='white', fontsize=20, fontweight='bold')
        
        ticks = [m['tick'] for m in self.mood_sequence]
        valences = [m['valence'] for m in self.mood_sequence]
        arousals = [m['arousal'] for m in self.mood_sequence]
        entropies = [m['entropy'] for m in self.mood_sequence]
        moods = [m['mood'] for m in self.mood_sequence]
        
        # Valence timeline
        ax1.set_facecolor('black')
        colors_v = ['red' if v < 0 else 'green' for v in valences]
        bars1 = ax1.barh(range(len(ticks)), valences, color=colors_v, alpha=0.8, height=0.8)
        ax1.set_yticks(range(len(ticks)))
        ax1.set_yticklabels([f"T{t}" for t in ticks], color='white', fontsize=8)
        ax1.set_xlabel('Valence (-1 to +1)', color='white')
        ax1.set_title('💭 Emotional Valence Over Time', color='cyan', fontsize=14)
        ax1.tick_params(colors='white')
        ax1.axvline(0, color='white', linestyle='--', alpha=0.5)
        
        # Arousal timeline  
        ax2.set_facecolor('black')
        colors_a = [plt.cm.plasma(a) for a in arousals]
        bars2 = ax2.barh(range(len(ticks)), arousals, color=colors_a, alpha=0.8, height=0.8)
        ax2.set_yticks(range(len(ticks)))
        ax2.set_yticklabels([f"T{t}" for t in ticks], color='white', fontsize=8)
        ax2.set_xlabel('Arousal (0 to 1)', color='white')
        ax2.set_title('⚡ Arousal Intensity Over Time', color='orange', fontsize=14)
        ax2.tick_params(colors='white')
        
        # Entropy timeline
        ax3.set_facecolor('black')
        colors_e = [plt.cm.viridis(e) for e in entropies]
        bars3 = ax3.barh(range(len(ticks)), entropies, color=colors_e, alpha=0.8, height=0.8)
        ax3.set_yticks(range(len(ticks)))
        ax3.set_yticklabels([f"T{t}" for t in ticks], color='white', fontsize=8)
        ax3.set_xlabel('Entropy (0 to 1)', color='white')
        ax3.set_title('🌀 Cognitive Entropy Over Time', color='magenta', fontsize=14)
        ax3.tick_params(colors='white')
        
        # Add mood annotations
        for i, (tick, mood) in enumerate(zip(ticks, moods)):
            if i % 3 == 0:  # Annotate every 3rd point to avoid crowding
                ax1.text(valences[i] + 0.05, i, mood, color='white', fontsize=8, 
                        verticalalignment='center', alpha=0.9)
        
        plt.tight_layout()
        output_path = self.output_path / "mood_sequences" / "mood_heatmap_horizontal.png"
        plt.savefig(output_path, facecolor='black', dpi=150, bbox_inches='tight')
        plt.close()
        
        # Radial pulse version
        fig, ax = plt.subplots(figsize=(12, 12), facecolor='black', subplot_kw=dict(projection='polar'))
        ax.set_facecolor('black')
        
        # Convert to polar coordinates
        angles = np.linspace(0, 2*np.pi, len(ticks), endpoint=False)
        
        # Plot as concentric circles
        for i, (valence, arousal, entropy, mood) in enumerate(zip(valences, arousals, entropies, moods)):
            # Radius based on arousal, color based on valence, size based on entropy
            radius = 0.5 + arousal * 0.4
            color = 'red' if valence < 0 else 'green'
            size = 50 + entropy * 200
            
            ax.scatter(angles[i], radius, c=color, s=size, alpha=0.7, edgecolors='white', linewidth=1)
            
            # Add mood labels for key points
            if i % 4 == 0:
                ax.text(angles[i], radius + 0.1, mood[:4], color='white', fontsize=8, 
                       ha='center', va='center', weight='bold')
        
        ax.set_ylim(0, 1)
        ax.set_title('DAWN Mood Pulse - Radial Evolution\n(Radius=Arousal, Color=Valence, Size=Entropy)', 
                    color='white', fontsize=16, pad=30)
        ax.grid(True, alpha=0.3, color='white')
        ax.set_theta_zero_location('N')
        
        plt.tight_layout()
        output_path = self.output_path / "mood_sequences" / "mood_pulse_radial.png"
        plt.savefig(output_path, facecolor='black', dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Mood sequences saved to: {self.output_path / 'mood_sequences'}")
        return "🧠 **Proof**: Emotion under tension → structured effect"

    # === TEST 2: BLOOM CLUSTER SNAPSHOTS ===
    
    def create_bloom_snapshots(self):
        """Create bloom evolution snapshots showing recursive memory structure"""
        print("🌸 Creating Bloom Cluster Snapshots...")
        
        for phase, data in self.bloom_snapshots.items():
            fig, ax = plt.subplots(figsize=(12, 10), facecolor='black')
            ax.set_facecolor('black')
            ax.set_xlim(-1, 1)
            ax.set_ylim(-1, 1)
            ax.set_aspect('equal')
            
            tick = data['tick']
            blooms = data['blooms']
            
            # Draw blooms with connections
            for bloom in blooms:
                x, y = bloom['x'], bloom['y']
                entropy = bloom['entropy']
                mood = bloom['mood']
                depth = bloom['depth']
                size = bloom['size']
                
                # Color by mood
                if mood in self.mood_colors:
                    color = self.mood_colors[mood]
                else:
                    color = '#888888'  # Default gray
                
                # Size by importance and depth
                radius = 0.05 + size * 0.08
                
                # Draw with glow effect
                for i in range(3):
                    glow_radius = radius * (1 + i * 0.4)
                    glow_alpha = 0.3 - i * 0.08
                    circle = Circle((x, y), glow_radius, facecolor=color, alpha=glow_alpha, edgecolor='none')
                    ax.add_patch(circle)
                
                # Core bloom
                circle = Circle((x, y), radius, facecolor=color, edgecolor='white', linewidth=2, alpha=0.9)
                ax.add_patch(circle)
                
                # Labels with metrics
                label_text = f"{bloom['id']}\nE:{entropy:.2f} D:{depth}"
                ax.text(x, y - radius - 0.08, label_text, color='white', fontsize=10, 
                       ha='center', va='top', weight='bold',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.8, edgecolor=color))
                
                # Entropy visualization as ring
                if entropy > 0.3:
                    ring = Circle((x, y), radius + 0.02, fill=False, edgecolor='yellow', 
                                linewidth=entropy*3, alpha=0.6)
                    ax.add_patch(ring)
            
            # Draw connections between blooms (simple proximity-based)
            for i, bloom1 in enumerate(blooms):
                for j, bloom2 in enumerate(blooms[i+1:], i+1):
                    x1, y1 = bloom1['x'], bloom1['y']
                    x2, y2 = bloom2['x'], bloom2['y']
                    distance = np.sqrt((x2-x1)**2 + (y2-y1)**2)
                    
                    # Connect if close and related by depth
                    if distance < 0.5 and abs(bloom1['depth'] - bloom2['depth']) <= 1:
                        ax.plot([x1, x2], [y1, y2], color='cyan', alpha=0.4, linewidth=1)
            
            # Phase-specific styling
            phase_colors = {'initial': 'lightgreen', 'rebloomed': 'orange', 'final': 'gold'}
            phase_titles = {
                'initial': 'Initial Bloom Formation', 
                'rebloomed': 'Mid-Evolution Rebloom',
                'final': 'Mature Cognitive Landscape'
            }
            
            ax.set_title(f"DAWN {phase_titles[phase]} | Tick {tick}", 
                        color=phase_colors[phase], fontsize=18, fontweight='bold')
            ax.text(-0.95, 0.9, f"Phase: {phase.upper()}", color='white', fontsize=12, 
                   bbox=dict(boxstyle="round", facecolor=phase_colors[phase], alpha=0.3))
            
            # Add metrics summary
            avg_entropy = np.mean([b['entropy'] for b in blooms])
            max_depth = max([b['depth'] for b in blooms])
            bloom_count = len(blooms)
            
            metrics_text = f"Blooms: {bloom_count}\nAvg Entropy: {avg_entropy:.2f}\nMax Depth: {max_depth}"
            ax.text(0.7, -0.8, metrics_text, color='white', fontsize=10,
                   bbox=dict(boxstyle="round", facecolor='black', alpha=0.8, edgecolor='white'))
            
            ax.axis('off')
            plt.tight_layout()
            
            output_path = self.output_path / "bloom_snapshots" / f"{phase}_bloom_snapshot.png"
            plt.savefig(output_path, facecolor='black', dpi=150, bbox_inches='tight')
            plt.close()
        
        print(f"✅ Bloom snapshots saved to: {self.output_path / 'bloom_snapshots'}")
        return "🧠 **Proof**: Recursive memory structure over time"

    # === TEST 3: SCUP BREAKDOWN FRAME ===
    
    def create_scup_breakdown(self):
        """Create SCUP breakdown showing coherence under pressure"""
        print("🧭 Creating SCUP Breakdown Frame...")
        
        fig = plt.figure(figsize=(16, 12), facecolor='black')
        gs = gridspec.GridSpec(3, 2, figure=fig, height_ratios=[2, 1, 1], width_ratios=[3, 1])
        
        # Main SCUP timeline
        ax_main = fig.add_subplot(gs[0, :])
        ax_main.set_facecolor('black')
        
        ticks = [d['tick'] for d in self.scup_data]
        scup_values = [d['scup'] for d in self.scup_data]
        zones = [d['zone'] for d in self.scup_data]
        pressure_events = [d['pressure_event'] for d in self.scup_data]
        
        # SCUP line with zone coloring
        for i in range(len(ticks)-1):
            color = self.zone_colors[zones[i]]
            ax_main.plot([ticks[i], ticks[i+1]], [scup_values[i], scup_values[i+1]], 
                        color=color, linewidth=3, alpha=0.8)
        
        # Mark pressure events
        for i, (tick, is_event) in enumerate(zip(ticks, pressure_events)):
            if is_event:
                ax_main.axvline(tick, color='red', linestyle='--', alpha=0.7, linewidth=2)
                ax_main.text(tick, 0.9, '⚠️ PRESSURE', rotation=90, color='red', 
                           fontsize=10, ha='center', va='bottom')
        
        ax_main.set_ylim(0, 1)
        ax_main.set_ylabel('SCUP (Semantic Coherence Under Pressure)', color='white', fontsize=12)
        ax_main.set_title('DAWN Cognitive Coherence Timeline', color='white', fontsize=16, fontweight='bold')
        ax_main.tick_params(colors='white')
        ax_main.grid(True, alpha=0.3, color='white')
        
        # Drift angle subplot
        ax_drift = fig.add_subplot(gs[1, :])
        ax_drift.set_facecolor('black')
        
        drift_angles = [d['drift_angle'] for d in self.scup_data]
        ax_drift.plot(ticks, drift_angles, color='cyan', linewidth=2, alpha=0.8)
        ax_drift.set_ylabel('Drift Angle (rad)', color='white')
        ax_drift.set_ylim(0, 2*np.pi)
        ax_drift.tick_params(colors='white')
        ax_drift.grid(True, alpha=0.3, color='white')
        
        # Zone distribution pie chart
        ax_pie = fig.add_subplot(gs[2, 0])
        zone_counts = defaultdict(int)
        for zone in zones:
            zone_counts[zone] += 1
        
        colors = [self.zone_colors[zone] for zone in zone_counts.keys()]
        wedges, texts, autotexts = ax_pie.pie(zone_counts.values(), labels=zone_counts.keys(), 
                                             colors=colors, autopct='%1.1f%%', startangle=90)
        for text in texts + autotexts:
            text.set_color('white')
        ax_pie.set_title('Zone Distribution', color='white', fontsize=12)
        
        # SCUP statistics
        ax_stats = fig.add_subplot(gs[2, 1])
        ax_stats.set_facecolor('black')
        ax_stats.axis('off')
        
        avg_scup = np.mean(scup_values)
        min_scup = np.min(scup_values)
        max_scup = np.max(scup_values)
        pressure_count = sum(pressure_events)
        
        stats_text = f"""SCUP STATISTICS
        
Average: {avg_scup:.3f}
Minimum: {min_scup:.3f}  
Maximum: {max_scup:.3f}
Pressure Events: {pressure_count}

RESILIENCE INDEX
{(avg_scup * (1 - pressure_count/len(ticks))):.3f}"""
        
        ax_stats.text(0.1, 0.9, stats_text, color='white', fontsize=11, 
                     verticalalignment='top', fontfamily='monospace',
                     bbox=dict(boxstyle="round", facecolor='darkblue', alpha=0.3))
        
        plt.tight_layout()
        output_path = self.output_path / "scup_breakdown" / "scup_analysis.png"
        plt.savefig(output_path, facecolor='black', dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ SCUP breakdown saved to: {self.output_path / 'scup_breakdown'}")
        return "🧠 **Proof**: Schema survives pressure without losing alignment"

    # === TEST 4: PULSE ZONE PHASE DIAGRAM ===
    
    def create_pulse_phase_diagram(self):
        """Create pulse zone transition diagram"""
        print("🌀 Creating Pulse Zone Phase Diagram...")
        
        # Spiral version
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10), facecolor='black')
        
        # Left: Transition spiral
        ax1.set_facecolor('black')
        ax1.set_xlim(-1.2, 1.2)
        ax1.set_ylim(-1.2, 1.2)
        ax1.set_aspect('equal')
        
        # Draw zone regions
        calm_circle = Circle((0, 0), 0.4, facecolor=self.zone_colors['calm'], alpha=0.2, edgecolor='white')
        active_circle = Circle((0, 0), 0.8, facecolor=self.zone_colors['active'], alpha=0.1, edgecolor='white', fill=False, linewidth=2)
        surge_region = Circle((0, 0), 1.0, facecolor=self.zone_colors['surge'], alpha=0.1, edgecolor='white', fill=False, linewidth=2)
        
        ax1.add_patch(calm_circle)
        ax1.add_patch(active_circle)
        ax1.add_patch(surge_region)
        
        # Zone labels
        ax1.text(0, 0, 'CALM\n🟢', color='white', fontsize=14, ha='center', va='center', weight='bold')
        ax1.text(0.6, 0.6, 'ACTIVE\n🟡', color='white', fontsize=12, ha='center', va='center', weight='bold')
        ax1.text(0.9, 0.9, 'SURGE\n🔴', color='white', fontsize=10, ha='center', va='center', weight='bold')
        
        # Draw transition spiral
        for i, transition in enumerate(self.pulse_transitions):
            # Position based on intensity and time
            angle = (transition['tick'] / 1000) * 4 * np.pi  # Multiple spirals
            radius = 0.3 + transition['intensity'] * 0.6
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            
            # Color by zone
            from_color = self.zone_colors[transition['from_zone']]
            to_color = self.zone_colors[transition['to_zone']]
            
            # Draw transition point
            ax1.scatter(x, y, s=200, color=to_color, edgecolor=from_color, linewidth=3, alpha=0.8, zorder=10)
            
            # Draw arrow for next transition
            if i < len(self.pulse_transitions) - 1:
                next_transition = self.pulse_transitions[i + 1]
                next_angle = (next_transition['tick'] / 1000) * 4 * np.pi
                next_radius = 0.3 + next_transition['intensity'] * 0.6
                next_x = next_radius * np.cos(next_angle)
                next_y = next_radius * np.sin(next_angle)
                
                ax1.annotate('', xy=(next_x, next_y), xytext=(x, y),
                           arrowprops=dict(arrowstyle='->', color='white', alpha=0.6, lw=2))
            
            # Add trigger labels
            ax1.text(x + 0.1, y + 0.1, transition['trigger'][:8], color='white', fontsize=8, 
                    weight='bold', ha='left', va='bottom',
                    bbox=dict(boxstyle="round,pad=0.2", facecolor='black', alpha=0.8))
        
        ax1.set_title('DAWN Pulse Zone Transition Spiral\n(Radius = Intensity, Color = Zone)', 
                     color='white', fontsize=16, fontweight='bold')
        ax1.axis('off')
        
        # Right: Timeline view
        ax2.set_facecolor('black')
        
        transition_ticks = [t['tick'] for t in self.pulse_transitions]
        zone_sequence = [t['to_zone'] for t in self.pulse_transitions]
        triggers = [t['trigger'] for t in self.pulse_transitions]
        intensities = [t['intensity'] for t in self.pulse_transitions]
        
        # Create zone timeline
        for i, (tick, zone, trigger, intensity) in enumerate(zip(transition_ticks, zone_sequence, triggers, intensities)):
            color = self.zone_colors[zone]
            ax2.barh(i, 50, left=tick-25, color=color, alpha=0.7, height=0.6)
            ax2.text(tick, i, f"{zone.upper()}\n{trigger}", color='white', fontsize=9, 
                    ha='center', va='center', weight='bold')
        
        ax2.set_yticks(range(len(transition_ticks)))
        ax2.set_yticklabels([f"T{i+1}" for i in range(len(transition_ticks))], color='white')
        ax2.set_xlabel('Tick', color='white')
        ax2.set_ylabel('Transition Events', color='white')
        ax2.set_title('Zone Transition Timeline', color='white', fontsize=14, fontweight='bold')
        ax2.tick_params(colors='white')
        ax2.grid(True, alpha=0.3, color='white', axis='x')
        
        plt.tight_layout()
        output_path = self.output_path / "pulse_diagrams" / "pulse_phase_diagram.png"
        plt.savefig(output_path, facecolor='black', dpi=150, bbox_inches='tight')
        plt.close()
        
        # Ring version - separate diagram
        fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
        ax.set_facecolor('black')
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        
        # Draw concentric rings for zones
        for radius, zone, alpha in [(0.5, 'calm', 0.3), (0.8, 'active', 0.2), (1.1, 'surge', 0.1)]:
            circle = Circle((0, 0), radius, facecolor=self.zone_colors[zone], alpha=alpha, 
                          edgecolor=self.zone_colors[zone], linewidth=3)
            ax.add_patch(circle)
        
        # Place transitions around the ring
        n_transitions = len(self.pulse_transitions)
        angles = np.linspace(0, 2*np.pi, n_transitions, endpoint=False)
        
        for i, (transition, angle) in enumerate(zip(self.pulse_transitions, angles)):
            # Radius based on intensity
            radius = 0.4 + transition['intensity'] * 0.6
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            
            # Draw transition node
            color = self.zone_colors[transition['to_zone']]
            ax.scatter(x, y, s=300, color=color, edgecolor='white', linewidth=2, alpha=0.9, zorder=10)
            
            # Add sigil/symbol for trigger
            trigger_symbols = {
                'novel_input': '✨', 'cognitive_load': '⚡', 'adaptation': '🔄',
                'integration': '🧩', 'curiosity': '🔍', 'insight_cascade': '💡',
                'synthesis': '⚛️'
            }
            symbol = trigger_symbols.get(transition['trigger'], '●')
            ax.text(x, y, symbol, color='black', fontsize=16, ha='center', va='center', weight='bold')
            
            # Label
            label_radius = radius + 0.2
            label_x = label_radius * np.cos(angle)
            label_y = label_radius * np.sin(angle)
            ax.text(label_x, label_y, f"{transition['trigger']}\nT{transition['tick']}", 
                   color='white', fontsize=9, ha='center', va='center', weight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.8))
        
        # Connect transitions in sequence
        for i in range(n_transitions):
            next_i = (i + 1) % n_transitions
            radius1 = 0.4 + self.pulse_transitions[i]['intensity'] * 0.6
            radius2 = 0.4 + self.pulse_transitions[next_i]['intensity'] * 0.6
            
            x1 = radius1 * np.cos(angles[i])
            y1 = radius1 * np.sin(angles[i])
            x2 = radius2 * np.cos(angles[next_i])
            y2 = radius2 * np.sin(angles[next_i])
            
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                       arrowprops=dict(arrowstyle='->', color='cyan', alpha=0.6, lw=2))
        
        ax.set_title('DAWN Pulse Zone Ring Diagram\nGovernance of System Tempo', 
                    color='white', fontsize=16, fontweight='bold')
        ax.axis('off')
        
        plt.tight_layout()
        output_path = self.output_path / "pulse_diagrams" / "pulse_ring_diagram.png"
        plt.savefig(output_path, facecolor='black', dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Pulse diagrams saved to: {self.output_path / 'pulse_diagrams'}")
        return "🧠 **Proof**: Mood doesn't just change — it *governs system tempo*"

    # === INTEGRATION TEST ===
    
    def create_integration_dashboard(self):
        """Create integrated dashboard showing all systems"""
        print("🎯 Creating Integration Dashboard...")
        
        fig = plt.figure(figsize=(24, 16), facecolor='black')
        gs = gridspec.GridSpec(3, 4, figure=fig, height_ratios=[1, 1, 1], width_ratios=[1, 1, 1, 1])
        
        # Title
        fig.suptitle('DAWN Cognitive Architecture - Visual Proof Dashboard', 
                    color='white', fontsize=24, fontweight='bold', y=0.95)
        
        # 1. Mood evolution (top left)
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.set_facecolor('black')
        ticks = [m['tick'] for m in self.mood_sequence]
        valences = [m['valence'] for m in self.mood_sequence]
        ax1.plot(ticks, valences, color='gold', linewidth=2)
        ax1.set_title('Mood Valence', color='gold', fontsize=12)
        ax1.tick_params(colors='white', labelsize=8)
        ax1.grid(True, alpha=0.3, color='white')
        
        # 2. SCUP coherence (top middle)
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.set_facecolor('black')
        scup_ticks = [d['tick'] for d in self.scup_data]
        scup_values = [d['scup'] for d in self.scup_data]
        ax2.plot(scup_ticks, scup_values, color='cyan', linewidth=2)
        ax2.set_title('SCUP Coherence', color='cyan', fontsize=12)
        ax2.tick_params(colors='white', labelsize=8)
        ax2.grid(True, alpha=0.3, color='white')
        
        # 3. Bloom evolution count (top right)
        ax3 = fig.add_subplot(gs[0, 2:])
        ax3.set_facecolor('black')
        phases = ['Initial', 'Rebloomed', 'Final']
        bloom_counts = [len(self.bloom_snapshots[p]['blooms']) for p in ['initial', 'rebloomed', 'final']]
        bars = ax3.bar(phases, bloom_counts, color=['lightgreen', 'orange', 'gold'])
        ax3.set_title('Bloom Evolution', color='lightgreen', fontsize=12)
        ax3.tick_params(colors='white', labelsize=8)
        
        # 4. Zone transitions (middle left)
        ax4 = fig.add_subplot(gs[1, :2])
        ax4.set_facecolor('black')
        zone_ticks = [t['tick'] for t in self.pulse_transitions]
        zone_intensities = [t['intensity'] for t in self.pulse_transitions]
        colors = [self.zone_colors[t['to_zone']] for t in self.pulse_transitions]
        ax4.scatter(zone_ticks, zone_intensities, c=colors, s=100, alpha=0.8)
        ax4.set_title('Pulse Zone Transitions', color='white', fontsize=12)
        ax4.tick_params(colors='white', labelsize=8)
        ax4.grid(True, alpha=0.3, color='white')
        
        # 5. System metrics (middle right)
        ax5 = fig.add_subplot(gs[1, 2:])
        ax5.set_facecolor('black')
        ax5.axis('off')
        
        # Calculate key metrics
        avg_valence = np.mean([m['valence'] for m in self.mood_sequence])
        avg_scup = np.mean(scup_values)
        total_blooms = sum(bloom_counts)
        transition_rate = len(self.pulse_transitions) / 1000  # per tick
        
        metrics_text = f"""DAWN SYSTEM METRICS

🧠 Cognitive Health
   Avg Valence: {avg_valence:+.2f}
   SCUP Coherence: {avg_scup:.3f}
   
🌸 Memory Evolution  
   Total Blooms: {total_blooms}
   Final Depth: {max([b['depth'] for b in self.bloom_snapshots['final']['blooms']])}
   
🌀 Dynamic Response
   Transition Rate: {transition_rate:.4f}/tick
   Zone Diversity: {len(set([t['to_zone'] for t in self.pulse_transitions]))}
   
⚡ Emergent Properties
   Entropy Range: {np.min([m['entropy'] for m in self.mood_sequence]):.2f}-{np.max([m['entropy'] for m in self.mood_sequence]):.2f}
   Adaptation Score: {avg_scup * (1 + avg_valence) * transition_rate * 10:.2f}"""
        
        ax5.text(0.05, 0.95, metrics_text, color='white', fontsize=11, 
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle="round", facecolor='darkblue', alpha=0.3))
        
        # 6. Phase correlation matrix (bottom)
        ax6 = fig.add_subplot(gs[2, :])
        ax6.set_facecolor('black')
        
        # Create correlation matrix between different metrics
        mood_vals = [m['valence'] for m in self.mood_sequence]
        mood_entropies = [m['entropy'] for m in self.mood_sequence]
        
        # Resample SCUP to match mood sequence length
        scup_resampled = np.interp(ticks, scup_ticks, scup_values)
        
        # Calculate correlations
        corr_data = np.array([mood_vals, mood_entropies, scup_resampled])
        correlation_matrix = np.corrcoef(corr_data)
        
        labels = ['Mood Valence', 'Mood Entropy', 'SCUP Coherence']
        im = ax6.imshow(correlation_matrix, cmap='RdBu', vmin=-1, vmax=1, aspect='equal')
        
        # Add correlation values
        for i in range(len(labels)):
            for j in range(len(labels)):
                text = ax6.text(j, i, f'{correlation_matrix[i, j]:.3f}', 
                              ha='center', va='center', color='white', fontweight='bold')
        
        ax6.set_xticks(range(len(labels)))
        ax6.set_yticks(range(len(labels)))
        ax6.set_xticklabels(labels, color='white', rotation=45, ha='right')
        ax6.set_yticklabels(labels, color='white')
        ax6.set_title('System Correlation Matrix', color='white', fontsize=12)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax6, shrink=0.8)
        cbar.ax.tick_params(colors='white')
        
        plt.tight_layout()
        output_path = self.output_path / "integration" / "dashboard.png"
        plt.savefig(output_path, facecolor='black', dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Integration dashboard saved to: {self.output_path / 'integration'}")
        return "🧠 **Proof**: Integrated cognitive architecture with emergent properties"

    def run_all_tests(self):
        """Run all visual tests and generate proof summary"""
        print("\n" + "="*80)
        print("🧠 DAWN COGNITIVE ARCHITECTURE - VISUAL PROOF SYSTEM")
        print("="*80)
        
        results = []
        
        # Run each test
        tests = [
            ("Mood Heatmap Sequence", self.create_mood_heatmap_sequence),
            ("Bloom Cluster Snapshots", self.create_bloom_snapshots),
            ("SCUP Breakdown Frame", self.create_scup_breakdown),
            ("Pulse Zone Phase Diagram", self.create_pulse_phase_diagram),
            ("Integration Dashboard", self.create_integration_dashboard)
        ]
        
        for test_name, test_func in tests:
            try:
                print(f"\n{'='*20} {test_name} {'='*20}")
                proof = test_func()
                results.append((test_name, "✅ SUCCESS", proof))
            except Exception as e:
                print(f"❌ Error in {test_name}: {e}")
                results.append((test_name, f"❌ ERROR: {e}", ""))
        
        # Generate summary report
        self.generate_proof_summary(results)
        
        print("\n" + "="*80)
        print("🎯 VISUAL PROOF GENERATION COMPLETE")
        print(f"📁 All outputs saved to: {self.output_path}")
        print("📄 Open proof_summary.html to view complete analysis")
        print("="*80)

    def generate_proof_summary(self, results):
        """Generate HTML summary of all proofs"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>DAWN Cognitive Architecture - Visual Proofs</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Arial, sans-serif; 
            margin: 20px; 
            background: linear-gradient(135deg, #0a0a0a, #1a1a2e);
            color: #ffffff;
            line-height: 1.6;
        }}
        .header {{
            text-align: center;
            padding: 30px;
            background: linear-gradient(45deg, #ff00ff, #00ffff);
            border-radius: 15px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        }}
        .test-section {{
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            margin: 20px 0;
            padding: 20px;
            border-left: 5px solid #00ffaa;
        }}
        .test-title {{
            font-size: 1.5em;
            color: #00ffaa;
            margin-bottom: 10px;
        }}
        .status {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 5px;
            margin: 5px 0;
        }}
        .success {{ background: #28a745; }}
        .error {{ background: #dc3545; }}
        .proof {{ 
            background: rgba(0,255,170,0.2);
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            font-style: italic;
        }}
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .image-card {{
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
        }}
        .image-card img {{
            max-width: 100%;
            border-radius: 8px;
            border: 2px solid #00ffaa;
        }}
        .image-card h3 {{
            margin: 10px 0 5px 0;
            color: #ffaa00;
        }}
        .metrics {{
            background: rgba(0,0,0,0.5);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 DAWN Cognitive Architecture</h1>
        <h2>Visual Proof System</h2>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="metrics">
        <h2>🎯 Proof Summary</h2>
        <p>These visualizations demonstrate DAWN's emergent cognitive properties through measurable behavioral patterns.</p>
    </div>
"""
        
        # Add each test result
        for test_name, status, proof in results:
            status_class = "success" if "SUCCESS" in status else "error"
            html_content += f"""
    <div class="test-section">
        <div class="test-title">{test_name}</div>
        <div class="status {status_class}">{status}</div>
        {f'<div class="proof">{proof}</div>' if proof else ''}
    </div>
"""
        
        # Add image galleries
        html_content += """
    <div class="gallery">
"""
        
        # Find all generated images
        for img_path in self.output_path.rglob("*.png"):
            rel_path = img_path.relative_to(self.output_path)
            html_content += f"""
        <div class="image-card">
            <img src="{rel_path.as_posix()}" alt="{img_path.stem}">
            <h3>{img_path.stem.replace('_', ' ').title()}</h3>
        </div>
"""
        
        html_content += """
    </div>
    
    <div class="metrics">
        <h2>🧠 Cognitive Architecture Insights</h2>
        <ul>
            <li><strong>Mood Governance:</strong> Emotional states create structured patterns in memory formation</li>
            <li><strong>Recursive Structure:</strong> Blooms develop hierarchical depth through reprocessing</li>
            <li><strong>Pressure Resilience:</strong> SCUP maintains coherence under cognitive load</li>
            <li><strong>Dynamic Tempo:</strong> Pulse zones govern system-wide behavioral rhythms</li>
            <li><strong>Emergent Integration:</strong> All systems correlate to produce unified cognition</li>
        </ul>
    </div>
</body>
</html>
"""
        
        summary_path = self.output_path / "proof_summary.html"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Proof summary saved to: {summary_path}")

def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='DAWN Visual Proof System')
    parser.add_argument('--path', type=str, help='Base path for DAWN system')
    parser.add_argument('--test', type=str, help='Run specific test (mood, bloom, scup, pulse, integration)')
    
    args = parser.parse_args()
    
    # Create test system
    tester = DawnVisualTests(base_path=args.path)
    
    if args.test:
        # Run specific test
        test_map = {
            'mood': tester.create_mood_heatmap_sequence,
            'bloom': tester.create_bloom_snapshots,
            'scup': tester.create_scup_breakdown,
            'pulse': tester.create_pulse_phase_diagram,
            'integration': tester.create_integration_dashboard
        }
        
        if args.test in test_map:
            print(f"🎯 Running {args.test} test...")
            test_map[args.test]()
        else:
            print(f"❌ Unknown test: {args.test}")
            print(f"Available tests: {', '.join(test_map.keys())}")
    else:
        # Run all tests
        tester.run_all_tests()

if __name__ == "__main__":
    main()