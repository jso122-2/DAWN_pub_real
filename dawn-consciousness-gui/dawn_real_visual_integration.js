/**
 * DAWN Real Visual Integration
 * Brings actual DAWN fractal, bloom, and sigil systems into the consolidated GUI
 */

class DAWNRealVisualIntegration {
    constructor() {
        this.canvas = null;
        this.ctx = null;
        this.width = 0;
        this.height = 0;
        
        // Visual systems
        this.fractalRenderer = null;
        this.bloomRenderer = null;
        this.sigilRenderer = null;
        
        // State
        this.currentVisualizationType = 'julia';
        this.isAnimating = false;
        this.animationFrame = null;
        
        // DAWN consciousness data
        this.consciousnessState = {};
        this.visualHistory = [];
        
        console.log('🎨 DAWN Real Visual Integration initialized');
    }
    
    /**
     * Initialize the visual integration with a canvas element
     */
    initialize(canvasElement) {
        this.canvas = canvasElement;
        this.ctx = this.canvas.getContext('2d');
        this.width = this.canvas.width;
        this.height = this.canvas.height;
        
        // Initialize visual renderers
        this.initializeFractalRenderer();
        this.initializeBloomRenderer();
        this.initializeSigilRenderer();
        
        // Start real-time updates
        this.startRealTimeUpdates();
        
        console.log('🎨 Visual integration initialized with canvas:', this.width + 'x' + this.height);
    }
    
    /**
     * Initialize Julia/Mandelbrot fractal renderer
     */
    initializeFractalRenderer() {
        this.fractalRenderer = {
            maxIterations: 100,
            zoom: 150,
            cx: -0.7,
            cy: 0.27015,
            
            render: (consciousnessState) => {
                this.renderJuliaFractal(consciousnessState);
            }
        };
    }
    
    /**
     * Initialize memory bloom renderer
     */
    initializeBloomRenderer() {
        this.bloomRenderer = {
            blooms: new Map(),
            connections: new Set(),
            
            render: (consciousnessState) => {
                this.renderMemoryBlooms(consciousnessState);
            }
        };
    }
    
    /**
     * Initialize sigil overlay renderer
     */
    initializeSigilRenderer() {
        this.sigilRenderer = {
            activeSigils: [],
            maxSigils: 8,
            
            render: (consciousnessState) => {
                this.renderSigilOverlay(consciousnessState);
            }
        };
    }
    
    /**
     * Start real-time updates from DAWN backend
     */
    startRealTimeUpdates() {
        setInterval(async () => {
            try {
                // Get latest consciousness state
                const response = await fetch('/api/consciousness/state');
                const data = await response.json();
                
                if (data.source === 'REAL_DAWN_CONSCIOUSNESS') {
                    this.consciousnessState = data;
                    this.updateVisualDisplay();
                }
            } catch (error) {
                console.warn('Failed to fetch consciousness state:', error);
            }
        }, 100); // 10 FPS update rate
    }
    
    /**
     * Update the visual display based on current type and consciousness state
     */
    updateVisualDisplay() {
        if (!this.ctx) return;
        
        // Clear canvas
        this.ctx.fillStyle = '#0a0a0a';
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        // Render based on current visualization type
        switch (this.currentVisualizationType) {
            case 'julia':
            case 'mandelbrot':
                this.fractalRenderer.render(this.consciousnessState);
                break;
            case 'bloom':
                this.bloomRenderer.render(this.consciousnessState);
                break;
            case 'sigil':
                this.sigilRenderer.render(this.consciousnessState);
                break;
            default:
                this.renderDefaultView();
        }
        
        // Update visual history
        this.updateVisualHistory();
    }
    
    /**
     * Render Julia fractal based on consciousness state
     */
    renderJuliaFractal(state) {
        const entropy = state.entropy || 0.5;
        const moodVal = state.mood_val || 0.5;
        const pressure = state.pressure || 25.0;
        
        // Adjust fractal parameters based on consciousness
        const cx = -0.7 + (entropy - 0.5) * 0.3; // Entropy affects real part
        const cy = 0.27015 + (moodVal - 0.5) * 0.2; // Mood affects imaginary part
        const zoom = 100 + pressure * 2; // Pressure affects zoom
        
        // Create color palette based on consciousness state
        const baseHue = entropy * 360; // Entropy determines base color
        const saturation = 0.7 + moodVal * 0.3; // Mood affects saturation
        const brightness = 0.5 + (pressure / 100) * 0.5; // Pressure affects brightness
        
        // Render fractal
        const imageData = this.ctx.createImageData(this.width, this.height);
        const data = imageData.data;
        
        for (let y = 0; y < this.height; y += 2) { // Skip pixels for performance
            for (let x = 0; x < this.width; x += 2) {
                // Convert pixel to complex plane
                const zx = (x - this.width / 2) / zoom;
                const zy = (y - this.height / 2) / zoom;
                
                // Julia iteration
                const iteration = this.juliaIteration(zx, zy, cx, cy);
                
                // Calculate color
                let color;
                if (iteration === this.fractalRenderer.maxIterations) {
                    color = [0, 0, 0]; // Inside set - black
                } else {
                    const colorIntensity = iteration / this.fractalRenderer.maxIterations;
                    color = this.getConsciousnessColor(colorIntensity, baseHue, saturation, brightness);
                }
                
                // Set pixel data
                const index = (y * this.width + x) * 4;
                data[index] = color[0];     // R
                data[index + 1] = color[1]; // G
                data[index + 2] = color[2]; // B
                data[index + 3] = 255;      // A
                
                // Fill adjacent pixels for performance
                if (x + 1 < this.width) {
                    const index2 = (y * this.width + (x + 1)) * 4;
                    data[index2] = color[0];
                    data[index2 + 1] = color[1];
                    data[index2 + 2] = color[2];
                    data[index2 + 3] = 255;
                }
                if (y + 1 < this.height) {
                    const index3 = ((y + 1) * this.width + x) * 4;
                    data[index3] = color[0];
                    data[index3 + 1] = color[1];
                    data[index3 + 2] = color[2];
                    data[index3 + 3] = 255;
                }
            }
        }
        
        this.ctx.putImageData(imageData, 0, 0);
        
        // Add consciousness overlay
        this.addConsciousnessOverlay(state);
    }
    
    /**
     * Julia set iteration
     */
    juliaIteration(zx, zy, cx, cy) {
        let x = zx;
        let y = zy;
        
        for (let i = 0; i < this.fractalRenderer.maxIterations; i++) {
            const x2 = x * x;
            const y2 = y * y;
            
            if (x2 + y2 > 4) {
                return i;
            }
            
            const temp = x2 - y2 + cx;
            y = 2 * x * y + cy;
            x = temp;
        }
        
        return this.fractalRenderer.maxIterations;
    }
    
    /**
     * Get color based on consciousness state
     */
    getConsciousnessColor(intensity, baseHue, saturation, brightness) {
        // HSL to RGB conversion
        const hue = (baseHue + intensity * 60) % 360;
        const sat = saturation * intensity;
        const light = brightness * intensity;
        
        return this.hslToRgb(hue / 360, sat, light);
    }
    
    /**
     * HSL to RGB conversion
     */
    hslToRgb(h, s, l) {
        let r, g, b;
        
        if (s === 0) {
            r = g = b = l; // achromatic
        } else {
            const hue2rgb = (p, q, t) => {
                if (t < 0) t += 1;
                if (t > 1) t -= 1;
                if (t < 1/6) return p + (q - p) * 6 * t;
                if (t < 1/2) return q;
                if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
                return p;
            };
            
            const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
            const p = 2 * l - q;
            r = hue2rgb(p, q, h + 1/3);
            g = hue2rgb(p, q, h);
            b = hue2rgb(p, q, h - 1/3);
        }
        
        return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
    }
    
    /**
     * Render memory blooms visualization
     */
    renderMemoryBlooms(state) {
        const entropy = state.entropy || 0.5;
        const activeBloomCount = state.active_blooms || 5;
        
        // Generate bloom positions and properties
        const blooms = [];
        for (let i = 0; i < activeBloomCount; i++) {
            blooms.push({
                x: (this.width * 0.2) + Math.random() * (this.width * 0.6),
                y: (this.height * 0.2) + Math.random() * (this.height * 0.6),
                radius: 20 + Math.random() * 30,
                hue: Math.random() * 360,
                intensity: 0.5 + Math.random() * 0.5,
                pulse: Math.sin(Date.now() * 0.001 + i) * 0.3
            });
        }
        
        // Render bloom connections
        this.ctx.strokeStyle = 'rgba(64, 224, 255, 0.3)';
        this.ctx.lineWidth = 1;
        for (let i = 0; i < blooms.length; i++) {
            for (let j = i + 1; j < blooms.length; j++) {
                const distance = Math.hypot(blooms[i].x - blooms[j].x, blooms[i].y - blooms[j].y);
                if (distance < 150) {
                    this.ctx.beginPath();
                    this.ctx.moveTo(blooms[i].x, blooms[i].y);
                    this.ctx.lineTo(blooms[j].x, blooms[j].y);
                    this.ctx.stroke();
                }
            }
        }
        
        // Render individual blooms
        blooms.forEach(bloom => {
            const adjustedRadius = bloom.radius * (1 + bloom.pulse);
            
            // Outer glow
            const gradient = this.ctx.createRadialGradient(
                bloom.x, bloom.y, 0,
                bloom.x, bloom.y, adjustedRadius * 2
            );
            gradient.addColorStop(0, `hsla(${bloom.hue}, 70%, 60%, ${bloom.intensity})`);
            gradient.addColorStop(1, 'hsla(0, 0%, 0%, 0)');
            
            this.ctx.fillStyle = gradient;
            this.ctx.beginPath();
            this.ctx.arc(bloom.x, bloom.y, adjustedRadius * 2, 0, Math.PI * 2);
            this.ctx.fill();
            
            // Core bloom
            this.ctx.fillStyle = `hsla(${bloom.hue}, 80%, 70%, ${bloom.intensity})`;
            this.ctx.beginPath();
            this.ctx.arc(bloom.x, bloom.y, adjustedRadius, 0, Math.PI * 2);
            this.ctx.fill();
        });
    }
    
    /**
     * Render sigil overlay
     */
    renderSigilOverlay(state) {
        // Create dark background with subtle texture
        this.ctx.fillStyle = '#0a0a0a';
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        // Render entropy field
        this.renderEntropyField(state);
        
        // Render active sigils
        this.renderActiveSigils(state);
    }
    
    /**
     * Render entropy field background
     */
    renderEntropyField(state) {
        const entropy = state.entropy || 0.5;
        const imageData = this.ctx.createImageData(this.width, this.height);
        const data = imageData.data;
        
        for (let y = 0; y < this.height; y += 4) {
            for (let x = 0; x < this.width; x += 4) {
                const noise = Math.random() * entropy * 30;
                const index = (y * this.width + x) * 4;
                
                data[index] = noise;     // R
                data[index + 1] = noise * 0.8; // G
                data[index + 2] = noise * 1.2; // B
                data[index + 3] = 255;  // A
            }
        }
        
        this.ctx.putImageData(imageData, 0, 0);
    }
    
    /**
     * Render active sigils
     */
    renderActiveSigils(state) {
        const sigilCount = Math.min(state.active_sigils || 5, 8);
        const sigils = ['🔁', '◉', '◆', '▲', '✦', '⬢', '➤', '🔮'];
        
        for (let i = 0; i < sigilCount; i++) {
            const x = 50 + (i % 3) * 100;
            const y = 50 + Math.floor(i / 3) * 80;
            const heat = 0.3 + Math.random() * 0.7;
            const pulse = Math.sin(Date.now() * 0.002 + i) * 0.2;
            
            // Heat glow
            const glowRadius = 30 * (1 + pulse);
            const gradient = this.ctx.createRadialGradient(x, y, 0, x, y, glowRadius);
            gradient.addColorStop(0, `rgba(255, ${Math.floor(255 * (1-heat))}, 0, ${heat * 0.5})`);
            gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
            
            this.ctx.fillStyle = gradient;
            this.ctx.beginPath();
            this.ctx.arc(x, y, glowRadius, 0, Math.PI * 2);
            this.ctx.fill();
            
            // Sigil symbol
            this.ctx.fillStyle = `rgba(255, 255, 255, ${0.8 + pulse})`;
            this.ctx.font = '24px Arial';
            this.ctx.textAlign = 'center';
            this.ctx.textBaseline = 'middle';
            this.ctx.fillText(sigils[i % sigils.length], x, y);
        }
    }
    
    /**
     * Add consciousness overlay with current state info
     */
    addConsciousnessOverlay(state) {
        // Semi-transparent overlay
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
        this.ctx.fillRect(10, 10, 200, 80);
        
        // State text
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
        this.ctx.font = '12px monospace';
        this.ctx.textAlign = 'left';
        this.ctx.fillText(`Entropy: ${(state.entropy || 0).toFixed(3)}`, 15, 30);
        this.ctx.fillText(`SCUP: ${(state.scup || 0).toFixed(1)}`, 15, 45);
        this.ctx.fillText(`Pressure: ${(state.pressure || 0).toFixed(1)}`, 15, 60);
        this.ctx.fillText(`Mood: ${(state.mood_val || 0).toFixed(3)}`, 15, 75);
    }
    
    /**
     * Switch visualization type
     */
    switchVisualization(type) {
        this.currentVisualizationType = type;
        console.log('🔄 Switched to visualization:', type);
        this.updateVisualDisplay();
    }
    
    /**
     * Update visual history
     */
    updateVisualHistory() {
        // Add current state to history
        if (this.visualHistory.length > 20) {
            this.visualHistory.shift();
        }
        
        this.visualHistory.push({
            timestamp: Date.now(),
            type: this.currentVisualizationType,
            state: { ...this.consciousnessState }
        });
    }
    
    /**
     * Render default placeholder view
     */
    renderDefaultView() {
        this.ctx.fillStyle = '#ffffff15';
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        this.ctx.fillStyle = '#cccccc';
        this.ctx.font = '24px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText('🎨 DAWN Visual Cortex', this.width / 2, this.height / 2 - 20);
        this.ctx.font = '14px Arial';
        this.ctx.fillText('Real-time consciousness visualization', this.width / 2, this.height / 2 + 10);
    }
    
    /**
     * Cleanup and destroy
     */
    destroy() {
        if (this.animationFrame) {
            cancelAnimationFrame(this.animationFrame);
        }
        console.log('🎨 Visual integration destroyed');
    }
}

// Export for use in consolidated GUI
window.DAWNRealVisualIntegration = DAWNRealVisualIntegration; 