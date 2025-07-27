// src/utils/graphUtils.ts
//! Reusable canvas graph utilities for DAWN consciousness visualization

export interface GraphTheme {
    background: string;
    grid: string;
    axis: string;
    text: string;
    textMuted: string;
    line: string;
    lineGlow: string;
    point: string;
    pointGlow: string;
  }
  
  export interface GraphConfig {
    width: number;
    height: number;
    padding: { top: number; right: number; bottom: number; left: number };
    gridLines: number;
    maxPoints: number;
    timeWindow: number; // in milliseconds
  }
  
  export interface DataPoint {
    timestamp: number;
    value: number;
  }
  
  export class LiveGraph {
    private canvas: HTMLCanvasElement;
    private ctx: CanvasRenderingContext2D;
    private config: GraphConfig;
    private theme: GraphTheme;
    private dataPoints: DataPoint[] = [];
    private minValue: number = 0;
    private maxValue: number = 100;
    private label: string;
    private highlightThreshold?: number;
  
    constructor(
      canvas: HTMLCanvasElement,
      config: GraphConfig,
      theme: GraphTheme,
      label: string,
      maxValue: number = 100,
      minValue: number = 0,
      highlightThreshold?: number
    ) {
      this.canvas = canvas;
      this.ctx = canvas.getContext('2d')!;
      this.config = config;
      this.theme = theme;
      this.label = label;
      this.maxValue = maxValue;
      this.minValue = minValue;
      this.highlightThreshold = highlightThreshold;
  
      // Set canvas dimensions
      this.canvas.width = config.width;
      this.canvas.height = config.height;
    }
  
    addPoint(value: number, timestamp?: number): void {
      const now = timestamp || Date.now();
      const cutoff = now - this.config.timeWindow;
  
      // Add new point
      this.dataPoints.push({ timestamp: now, value });
  
      // Remove old points
      this.dataPoints = this.dataPoints.filter(point => point.timestamp >= cutoff);
  
      // Limit max points for performance
      if (this.dataPoints.length > this.config.maxPoints) {
        this.dataPoints.shift();
      }
    }
  
    draw(): void {
      if (!this.ctx) return;
  
      const { width, height, padding } = this.config;
      const graphWidth = width - padding.left - padding.right;
      const graphHeight = height - padding.top - padding.bottom;
  
      // Clear canvas
      this.ctx.fillStyle = this.theme.background;
      this.ctx.fillRect(0, 0, width, height);
  
      // Draw grid
      this.drawGrid(graphWidth, graphHeight);
  
      // Draw axes
      this.drawAxes(graphWidth, graphHeight);
  
      // Draw labels
      this.drawLabels(graphWidth, graphHeight);
  
      // Draw data line
      this.drawDataLine(graphWidth, graphHeight);
    }
  
    private drawGrid(graphWidth: number, graphHeight: number): void {
      const { padding, gridLines } = this.config;
      
      this.ctx.strokeStyle = this.theme.grid;
      this.ctx.lineWidth = 1;
      this.ctx.setLineDash([2, 2]);
  
      // Horizontal grid lines
      for (let i = 0; i <= gridLines; i++) {
        const y = padding.top + (graphHeight / gridLines) * i;
        this.ctx.beginPath();
        this.ctx.moveTo(padding.left, y);
        this.ctx.lineTo(padding.left + graphWidth, y);
        this.ctx.stroke();
      }
  
      // Vertical grid lines
      const timeSegments = 6;
      for (let i = 0; i <= timeSegments; i++) {
        const x = padding.left + (graphWidth / timeSegments) * i;
        this.ctx.beginPath();
        this.ctx.moveTo(x, padding.top);
        this.ctx.lineTo(x, padding.top + graphHeight);
        this.ctx.stroke();
      }
  
      this.ctx.setLineDash([]);
    }
  
    private drawAxes(graphWidth: number, graphHeight: number): void {
      const { padding } = this.config;
      
      this.ctx.strokeStyle = this.theme.axis;
      this.ctx.lineWidth = 2;
      this.ctx.beginPath();
      
      // Y-axis
      this.ctx.moveTo(padding.left, padding.top);
      this.ctx.lineTo(padding.left, padding.top + graphHeight);
      
      // X-axis
      this.ctx.moveTo(padding.left, padding.top + graphHeight);
      this.ctx.lineTo(padding.left + graphWidth, padding.top + graphHeight);
      
      this.ctx.stroke();
    }
  
    private drawLabels(graphWidth: number, graphHeight: number): void {
      const { padding, gridLines } = this.config;
      const { width, height } = this.config;
      
      this.ctx.fillStyle = this.theme.textMuted;
      this.ctx.font = '10px "DejaVu Sans Mono"';
      
      // X-axis label
      this.ctx.textAlign = 'center';
      this.ctx.fillText(
        `Time (${this.config.timeWindow / 1000}s)`, 
        padding.left + graphWidth / 2, 
        height - 5
      );
      
      // Y-axis label
      this.ctx.save();
      this.ctx.translate(15, padding.top + graphHeight / 2);
      this.ctx.rotate(-Math.PI / 2);
      this.ctx.fillText(this.label, 0, 0);
      this.ctx.restore();
  
      // Value scale
      this.ctx.textAlign = 'right';
      for (let i = 0; i <= gridLines; i++) {
        const value = this.maxValue - ((this.maxValue - this.minValue) / gridLines) * i;
        const y = padding.top + (graphHeight / gridLines) * i;
        this.ctx.fillText(value.toFixed(1), padding.left - 5, y + 3);
      }
    }
  
    private drawDataLine(graphWidth: number, graphHeight: number): void {
      if (this.dataPoints.length < 2) return;
  
      const { padding } = this.config;
      const values = this.dataPoints.map(p => p.value);
      const currentValue = values[values.length - 1];
      const shouldGlow = this.highlightThreshold !== undefined && currentValue > this.highlightThreshold;
  
      // Set up line style
      this.ctx.strokeStyle = this.theme.line;
      this.ctx.lineWidth = shouldGlow ? 3 : 2;
      this.ctx.lineCap = 'round';
      this.ctx.lineJoin = 'round';
  
      // Add glow effect for highlighted values
      if (shouldGlow) {
        this.ctx.shadowColor = this.theme.lineGlow;
        this.ctx.shadowBlur = 8;
      }
  
      this.ctx.beginPath();
      
      values.forEach((value, index) => {
        const x = padding.left + (graphWidth / (values.length - 1)) * index;
        const normalizedValue = (value - this.minValue) / (this.maxValue - this.minValue);
        const y = padding.top + graphHeight - (normalizedValue * graphHeight);
        
        if (index === 0) {
          this.ctx.moveTo(x, y);
        } else {
          this.ctx.lineTo(x, y);
        }
      });
      
      this.ctx.stroke();
      this.ctx.shadowBlur = 0; // Reset shadow
  
      // Draw current value point
      const lastX = padding.left + graphWidth;
      const normalizedCurrent = (currentValue - this.minValue) / (this.maxValue - this.minValue);
      const lastY = padding.top + graphHeight - (normalizedCurrent * graphHeight);
      
      this.ctx.fillStyle = shouldGlow ? this.theme.pointGlow : this.theme.point;
      this.ctx.beginPath();
      this.ctx.arc(lastX, lastY, shouldGlow ? 4 : 3, 0, 2 * Math.PI);
      this.ctx.fill();
    }
  
    getCurrentValue(): number | null {
      return this.dataPoints.length > 0 ? this.dataPoints[this.dataPoints.length - 1].value : null;
    }
  
    getDataCount(): number {
      return this.dataPoints.length;
    }
  
    clear(): void {
      this.dataPoints = [];
    }
  
    getTimeSpan(): number {
      if (this.dataPoints.length === 0) return 0;
      return this.dataPoints[this.dataPoints.length - 1].timestamp - this.dataPoints[0].timestamp;
    }
  }
  
  // Default themes
  export const GRAPH_THEMES = {
    DAWN_BLUEPRINT: {
      background: '#0a0f14',
      grid: '#2d3748',
      axis: '#d8dee9',
      text: '#d8dee9',
      textMuted: '#81a1c1',
      line: '#88c0d0',
      lineGlow: '#5e81ac',
      point: '#88c0d0',
      pointGlow: '#5e81ac'
    },
    DAWN_WARM: {
      background: '#0a0f14',
      grid: '#2d3748',
      axis: '#d8dee9',
      text: '#d8dee9',
      textMuted: '#81a1c1',
      line: '#ebcb8b',
      lineGlow: '#d08770',
      point: '#ebcb8b',
      pointGlow: '#d08770'
    }
  };
  
  // Performance-optimized data buffer
  export class CircularBuffer<T> {
    private buffer: T[];
    private size: number;
    private head: number = 0;
    private count: number = 0;
  
    constructor(size: number) {
      this.size = size;
      this.buffer = new Array(size);
    }
  
    push(item: T): void {
      this.buffer[this.head] = item;
      this.head = (this.head + 1) % this.size;
      this.count = Math.min(this.count + 1, this.size);
    }
  
    toArray(): T[] {
      if (this.count === 0) return [];
      
      const result: T[] = [];
      for (let i = 0; i < this.count; i++) {
        const index = (this.head - this.count + i + this.size) % this.size;
        result.push(this.buffer[index]);
      }
      return result;
    }
  
    get length(): number {
      return this.count;
    }
  
    clear(): void {
      this.count = 0;
      this.head = 0;
    }
  }