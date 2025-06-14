export type AnimationCallback = (deltaTime: number, totalTime: number) => void;

class AnimationManager {
  private callbacks = new Map<string, AnimationCallback>();
  private lastTime = 0;
  private animationId: number | null = null;
  private isRunning = false;

  register(id: string, callback: AnimationCallback): () => void {
    this.callbacks.set(id, callback);
    
    if (!this.isRunning && this.callbacks.size > 0) {
      this.start();
    }

    // Return unregister function
    return () => {
      this.callbacks.delete(id);
      if (this.callbacks.size === 0) {
        this.stop();
      }
    };
  }

  private start(): void {
    if (this.isRunning) return;
    
    this.isRunning = true;
    this.lastTime = performance.now();
    this.animate();
  }

  private stop(): void {
    if (!this.isRunning) return;
    
    this.isRunning = false;
    if (this.animationId !== null) {
      cancelAnimationFrame(this.animationId);
      this.animationId = null;
    }
  }

  private animate = (): void => {
    if (!this.isRunning) return;

    const currentTime = performance.now();
    const deltaTime = currentTime - this.lastTime;
    this.lastTime = currentTime;

    // Call all registered callbacks
    this.callbacks.forEach(callback => {
      try {
        callback(deltaTime, currentTime);
      } catch (error) {
        console.error('Animation callback error:', error);
      }
    });

    this.animationId = requestAnimationFrame(this.animate);
  };

  getActiveAnimations(): string[] {
    return Array.from(this.callbacks.keys());
  }

  isAnimating(): boolean {
    return this.isRunning;
  }
}

// Export singleton instance
export const animationManager = new AnimationManager(); 