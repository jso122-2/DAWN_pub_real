import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Any, Tuple
import io
import base64

class BaseVisualizer:
    def __init__(self):
        self.update_interval = 0.1  # 10Hz update rate
        plt.style.use('dark_background')
    
    def _fig_to_base64(self, fig) -> str:
        """Convert matplotlib figure to base64 string"""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        return f"data:image/png;base64,{img_str}"

class ConsciousnessWaveVisualizer(BaseVisualizer):
    def generate(self, data: Dict[str, Any], size: Tuple[int, int] = (800, 600)) -> str:
        """Generate consciousness wave visualization"""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100))
        
        scup_history = data.get('scup_history', [])
        current_tick = data.get('current_tick', 0)
        
        if scup_history:
            x = np.arange(len(scup_history))
            ax.plot(x, scup_history, 'c-', linewidth=2, alpha=0.8)
            ax.scatter(len(scup_history)-1, scup_history[-1], color='cyan', s=100)
        
        ax.set_title('Consciousness Wave', color='white', pad=20)
        ax.set_xlabel('Time', color='white')
        ax.set_ylabel('SCUP', color='white')
        ax.grid(True, alpha=0.2)
        
        return self._fig_to_base64(fig)

class EntropyThermalVisualizer(BaseVisualizer):
    def generate(self, data: Dict[str, Any], size: Tuple[int, int] = (800, 600)) -> str:
        """Generate entropy thermal visualization"""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100))
        
        entropy_map = data.get('entropy_map', np.zeros((10, 10)))
        temperature = data.get('temperature', 0)
        
        im = ax.imshow(entropy_map, cmap='hot', interpolation='nearest')
        plt.colorbar(im, ax=ax, label='Entropy')
        
        ax.set_title(f'Entropy Distribution (T={temperature:.2f})', color='white', pad=20)
        ax.grid(True, alpha=0.2)
        
        return self._fig_to_base64(fig)

class NeuralActivityVisualizer(BaseVisualizer):
    def generate(self, data: Dict[str, Any], size: Tuple[int, int] = (800, 600)) -> str:
        """Generate neural activity visualization"""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100))
        
        neural_matrix = data.get('neural_matrix', np.zeros((10, 10)))
        activation_levels = data.get('activation_levels', [])
        
        im = ax.imshow(neural_matrix, cmap='viridis', interpolation='nearest')
        plt.colorbar(im, ax=ax, label='Activation')
        
        ax.set_title('Neural Activity Matrix', color='white', pad=20)
        ax.grid(True, alpha=0.2)
        
        return self._fig_to_base64(fig)

class AlignmentMatrixVisualizer(BaseVisualizer):
    def generate(self, data: Dict[str, Any], size: Tuple[int, int] = (800, 600)) -> str:
        """Generate alignment matrix visualization"""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100))
        
        alignment_data = data.get('alignment_data', np.zeros((10, 10)))
        coherence = data.get('coherence', 0)
        
        im = ax.imshow(alignment_data, cmap='coolwarm', interpolation='nearest')
        plt.colorbar(im, ax=ax, label='Alignment')
        
        ax.set_title(f'System Alignment (Coherence={coherence:.2f})', color='white', pad=20)
        ax.grid(True, alpha=0.2)
        
        return self._fig_to_base64(fig)

class BloomPatternVisualizer(BaseVisualizer):
    def generate(self, data: Dict[str, Any], size: Tuple[int, int] = (800, 600)) -> str:
        """Generate bloom pattern visualization"""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100))
        
        bloom_state = data.get('bloom_state', np.zeros((10, 10)))
        growth_rate = data.get('growth_rate', 0)
        
        im = ax.imshow(bloom_state, cmap='spring', interpolation='nearest')
        plt.colorbar(im, ax=ax, label='Bloom Intensity')
        
        ax.set_title(f'Consciousness Bloom (Growth={growth_rate:.2f})', color='white', pad=20)
        ax.grid(True, alpha=0.2)
        
        return self._fig_to_base64(fig)

class MoodGradientVisualizer(BaseVisualizer):
    def generate(self, data: Dict[str, Any], size: Tuple[int, int] = (800, 600)) -> str:
        """Generate mood gradient visualization"""
        fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100))
        
        mood_vector = data.get('mood_vector', np.zeros(10))
        mood_history = data.get('mood_history', [])
        
        if mood_history:
            x = np.arange(len(mood_history))
            ax.plot(x, mood_history, 'g-', linewidth=2, alpha=0.8)
            ax.scatter(len(mood_history)-1, mood_history[-1], color='green', s=100)
        
        ax.set_title('Mood State Transitions', color='white', pad=20)
        ax.set_xlabel('Time', color='white')
        ax.set_ylabel('Mood Value', color='white')
        ax.grid(True, alpha=0.2)
        
        return self._fig_to_base64(fig) 