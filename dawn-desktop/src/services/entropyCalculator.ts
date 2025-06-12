export class EntropyCalculator {
  private history: number[] = [];
  private maxHistory = 100;
  
  calculateEntropy(metrics: {
    cpuUsage: number,
    memoryUsage: number,
    diskIO: number,
    networkLatency: number,
    processCount: number
  }) {
    // Shannon entropy calculation based on system variance
    const values = Object.values(metrics);
    const sum = values.reduce((a, b) => a + b, 0);
    
    let entropy = 0;
    values.forEach(value => {
      if (value > 0) {
        const p = value / sum;
        entropy -= p * Math.log2(p);
      }
    });
    
    // Normalize to 0-100 scale
    const normalized = (entropy / Math.log2(values.length)) * 100;
    
    this.history.push(normalized);
    if (this.history.length > this.maxHistory) {
      this.history.shift();
    }
    
    // Add variance component
    const variance = this.calculateVariance();
    return Math.min(100, normalized + variance * 10);
  }
  
  private calculateVariance() {
    if (this.history.length < 2) return 0;
    const mean = this.history.reduce((a, b) => a + b) / this.history.length;
    const variance = this.history.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / this.history.length;
    return Math.sqrt(variance);
  }
} 