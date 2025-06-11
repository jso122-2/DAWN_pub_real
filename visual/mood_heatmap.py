#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from pathlib import Path

def generate_mood_heatmap():
    print("Generating mood heatmap for DAWN...")
    
    moods = ['joyful', 'focused', 'reflective', 'curious', 'calm']
    intensities = np.random.rand(5) * 0.8 + 0.2
    
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='black')
    ax.set_facecolor('black')
    
    colors = ['gold', 'royalblue', 'mediumpurple', 'tomato', 'limegreen']
    bars = ax.barh(moods, intensities, color=colors, alpha=0.8)
    
    ax.set_xlabel('Emotional Intensity', color='white')
    ax.set_title('DAWN Current Mood State', color='white', fontsize=16)
    ax.tick_params(colors='white')
    
    for i, (mood, intensity) in enumerate(zip(moods, intensities)):
        ax.text(intensity + 0.05, i, f'{intensity:.2f}', 
               color='white', va='center', fontweight='bold')
    
    plt.tight_layout()
    
    output_path = Path("visual_output") / "mood_heatmap_current.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, facecolor='black', dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Success! Mood heatmap saved to: {output_path}")
    return str(output_path)

if __name__ == "__main__":
    generate_mood_heatmap()
