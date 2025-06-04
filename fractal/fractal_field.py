// DAWN Fractal Brain Visualization System
// Real-time recursive cognitive architecture renderer

class DAWNVisualCortex {
    constructor(canvas, config = {}) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.width = canvas.width;
        this.height = canvas.height;
        
        // Configuration
        this.config = {
            baseNodeSize: 8,
            maxRecursionDepth: 5,
            bloomDecayRate: 0.98,
            entropyColorShift: true,
            pulseRate: 0.1,
            ...config
        };
        
        // Core data structures
        this.memoryBlooms = new Map(); // bloom_id -> BloomNode
        this.activeConnections = new Set();
        this.entropyField = new Float32Array(this.width * this.height);
        this.vectorField = [];
        
        // Animation state
        this.tick = 0;
        this.animationId = null;
    }
    
    // Core bloom node structure
    class BloomNode {
        constructor(id, position, depth = 0, parent = null) {
            this.id = id;
            this.position = position;
            this.depth = depth;
            this.parent = parent;
            this.children = [];
            
            // Cognitive metrics
            this.heat = 0.5;
            this.entropy = 0.3;
            this.urgency = 0.0;
            this.mood = 0.0; // -1 to 1
            this.resonance = 0.0;
            
            // Visual properties
            this.radius = 8;
            this.opacity = 1.0;
            this.rotation = 0;
            this.fractalSeed = Math.random();
            
            // Bloom lifecycle
            this.age = 0;
            this.blooming = true;
            this.decay = 0;
        }
        
        // Fractal shape generator
        generateFractalPath(ctx, depth = 0) {
            if (depth > 4) return;
            
            const branches = Math.floor(3 + this.resonance * 3);
            const angleStep = (Math.PI * 2) / branches;
            
            ctx.save();
            ctx.translate(this.position.x, this.position.y);
            ctx.rotate(this.rotation);
            
            for (let i = 0; i < branches; i++) {
                const angle = i * angleStep + this.fractalSeed * Math.PI;
                const length = this.radius * (1 - depth * 0.2);
                
                ctx.beginPath();
                ctx.moveTo(0, 0);
                
                // Fractal curve based on entropy
                const controlX = Math.cos(angle) * length * 0.5;
                const controlY = Math.sin(angle) * length * 0.5 + 
                                this.entropy * length * 0.3;
                const endX = Math.cos(angle) * length;
                const endY = Math.sin(angle) * length;
                
                ctx.quadraticCurveTo(controlX, controlY, endX, endY);
                
                // Color based on cognitive state
                ctx.strokeStyle = this.getStateColor(depth);
                ctx.lineWidth = Math.max(1, (5 - depth) * this.opacity);
                ctx.stroke();
                
                // Recursive branches
                if (this.resonance > 0.5) {
                    ctx.save();
                    ctx.translate(endX, endY);
                    this.generateFractalPath(ctx, depth + 1);
                    ctx.restore();
                }
            }
            
            ctx.restore();
        }
        
        getStateColor(depth = 0) {
            // Base color from mood/urgency/entropy
            const hue = (this.mood + 1) * 120; // Blue(calm) to Red(agitated)
            const saturation = 30 + this.urgency * 70;
            const lightness = 20 + (1 - this.entropy) * 40 - depth * 10;
            const alpha = this.opacity * (1 - depth * 0.2);
            
            return `hsla(${hue}, ${saturation}%, ${lightness}%, ${alpha})`;
        }
    }
    
    // Entropy field renderer
    renderEntropyField() {
        const imageData = this.ctx.createImageData(this.width, this.height);
        const data = imageData.data;
        
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                const idx = y * this.width + x;
                const entropy = this.entropyField[idx];
                
                // Entropy visualization as heat map
                const heat = entropy * 255;
                const r = heat;
                const g = heat * 0.3;
                const b = heat * 0.8;
                const a = entropy * 50; // Subtle overlay
                
                const pixelIdx = idx * 4;
                data[pixelIdx] = r;
                data[pixelIdx + 1] = g;
                data[pixelIdx + 2] = b;
                data[pixelIdx + 3] = a;
            }
        }
        
        this.ctx.putImageData(imageData, 0, 0);
    }
    
    // Vector field visualization
    renderVectorField() {
        this.ctx.strokeStyle = 'rgba(100, 150, 255, 0.3)';
        this.ctx.lineWidth = 1;
        
        const gridSize = 20;
        for (let y = 0; y < this.height; y += gridSize) {
            for (let x = 0; x < this.width; x += gridSize) {
                const idx = Math.floor(y / gridSize) * Math.floor(this.width / gridSize) + 
                           Math.floor(x / gridSize);
                
                if (this.vectorField[idx]) {
                    const vector = this.vectorField[idx];
                    const magnitude = Math.sqrt(vector.x ** 2 + vector.y ** 2);
                    
                    this.ctx.beginPath();
                    this.ctx.moveTo(x, y);
                    this.ctx.lineTo(
                        x + vector.x * 10 * magnitude,
                        y + vector.y * 10 * magnitude
                    );
                    this.ctx.stroke();
                }
            }
        }
    }
    
    // Connection renderer with pulsing
    renderConnections() {
        this.activeConnections.forEach(conn => {
            const bloom1 = this.memoryBlooms.get(conn.from);
            const bloom2 = this.memoryBlooms.get(conn.to);
            
            if (!bloom1 || !bloom2) return;
            
            const pulse = Math.sin(this.tick * this.config.pulseRate + conn.phase) * 0.5 + 0.5;
            
            this.ctx.beginPath();
            this.ctx.moveTo(bloom1.position.x, bloom1.position.y);
            
            // Bezier curve based on resonance
            const midX = (bloom1.position.x + bloom2.position.x) / 2;
            const midY = (bloom1.position.y + bloom2.position.y) / 2;
            const resonanceOffset = (bloom1.resonance + bloom2.resonance) * 20;
            
            this.ctx.quadraticCurveTo(
                midX + resonanceOffset * Math.sin(conn.phase),
                midY + resonanceOffset * Math.cos(conn.phase),
                bloom2.position.x,
                bloom2.position.y
            );
            
            // Gradient stroke
            const gradient = this.ctx.createLinearGradient(
                bloom1.position.x, bloom1.position.y,
                bloom2.position.x, bloom2.position.y
            );
            gradient.addColorStop(0, bloom1.getStateColor());
            gradient.addColorStop(1, bloom2.getStateColor());
            
            this.ctx.strokeStyle = gradient;
            this.ctx.lineWidth = 2 + pulse * 2;
            this.ctx.globalAlpha = 0.5 + pulse * 0.3;
            this.ctx.stroke();
            this.ctx.globalAlpha = 1.0;
        });
    }
    
    // Main render loop
    render() {
        // Clear canvas
        this.ctx.fillStyle = 'rgba(10, 10, 10, 0.9)';
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        // Layer 1: Entropy field
        this.renderEntropyField();
        
        // Layer 2: Vector field
        this.renderVectorField();
        
        // Layer 3: Connections
        this.renderConnections();
        
        // Layer 4: Memory blooms
        this.memoryBlooms.forEach(bloom => {
            bloom.generateFractalPath(this.ctx);
            
            // Core bloom circle
            this.ctx.beginPath();
            this.ctx.arc(bloom.position.x, bloom.position.y, bloom.radius, 0, Math.PI * 2);
            this.ctx.fillStyle = bloom.getStateColor();
            this.ctx.fill();
            
            // Resonance halo
            if (bloom.resonance > 0.5) {
                this.ctx.beginPath();
                this.ctx.arc(bloom.position.x, bloom.position.y, 
                           bloom.radius + bloom.resonance * 10, 0, Math.PI * 2);
                this.ctx.strokeStyle = 'rgba(255, 215, 0, ' + bloom.resonance * 0.3 + ')';
                this.ctx.lineWidth = 2;
                this.ctx.stroke();
            }
        });
        
        // Update animation state
        this.updateBlooms();
        this.updateEntropyField();
        this.tick++;
        
        this.animationId = requestAnimationFrame(() => this.render());
    }
    
    // Bloom lifecycle management
    updateBlooms() {
        this.memoryBlooms.forEach(bloom => {
            bloom.age++;
            bloom.rotation += 0.01 * bloom.entropy;
            
            // Decay non-active blooms
            if (!bloom.blooming) {
                bloom.decay += 0.01;
                bloom.opacity = Math.max(0, 1 - bloom.decay);
                bloom.radius *= this.config.bloomDecayRate;
                
                if (bloom.opacity <= 0) {
                    this.memoryBlooms.delete(bloom.id);
                }
            }
            
            // Pulse based on heat
            bloom.radius = bloom.radius * 0.95 + 
                          (this.config.baseNodeSize + bloom.heat * 10) * 0.05;
        });
    }
    
    // Entropy field dynamics
    updateEntropyField() {
        // Diffusion
        const newField = new Float32Array(this.entropyField.length);
        
        for (let y = 1; y < this.height - 1; y++) {
            for (let x = 1; x < this.width - 1; x++) {
                const idx = y * this.width + x;
                
                // Simple diffusion kernel
                let sum = this.entropyField[idx] * 0.6;
                sum += this.entropyField[idx - 1] * 0.1;
                sum += this.entropyField[idx + 1] * 0.1;
                sum += this.entropyField[idx - this.width] * 0.1;
                sum += this.entropyField[idx + this.width] * 0.1;
                
                newField[idx] = sum * 0.98; // Decay
            }
        }
        
        // Add entropy from blooms
        this.memoryBlooms.forEach(bloom => {
            const x = Math.floor(bloom.position.x);
            const y = Math.floor(bloom.position.y);
            const idx = y * this.width + x;
            
            if (idx >= 0 && idx < newField.length) {
                newField[idx] = Math.min(1, newField[idx] + bloom.entropy * 0.1);
            }
        });
        
        this.entropyField = newField;
    }
    
    // API for adding new blooms
    addBloom(id, x, y, parentId = null) {
        const parent = parentId ? this.memoryBlooms.get(parentId) : null;
        const depth = parent ? parent.depth + 1 : 0;
        
        const bloom = new this.BloomNode(id, {x, y}, depth, parent);
        this.memoryBlooms.set(id, bloom);
        
        if (parent) {
            parent.children.push(bloom);
            this.activeConnections.add({
                from: parentId,
                to: id,
                phase: Math.random() * Math.PI * 2
            });
        }
        
        return bloom;
    }
    
    // API for updating bloom state
    updateBloomState(id, metrics) {
        const bloom = this.memoryBlooms.get(id);
        if (!bloom) return;
        
        Object.assign(bloom, metrics);
    }
    
    // Start/stop animation
    start() {
        if (!this.animationId) {
            this.render();
        }
    }
    
    stop() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
    }
}

// Usage example:
/*
const canvas = document.getElementById('dawn-visual-cortex');
const visualizer = new DAWNVisualCortex(canvas, {
    baseNodeSize: 10,
    maxRecursionDepth: 4,
    entropyColorShift: true
});

// Add some blooms
const bloom1 = visualizer.addBloom('genesis', 400, 300);
visualizer.updateBloomState('genesis', {
    heat: 0.8,
    entropy: 0.3,
    mood: 0.2,
    urgency: 0.5,
    resonance: 0.7
});

// Add child blooms
visualizer.addBloom('thought_1', 450, 280, 'genesis');
visualizer.addBloom('thought_2', 380, 340, 'genesis');

// Start visualization
visualizer.start();
*/

// SVG Alternative Implementation
class DAWNFractalSVG {
    constructor(svgElement) {
        this.svg = svgElement;
        this.defs = this.createDefs();
        this.bloomGroup = this.createGroup('blooms');
        this.connectionGroup = this.createGroup('connections');
        this.effectGroup = this.createGroup('effects');
    }
    
    createDefs() {
        const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        
        // Entropy gradient
        const entropyGradient = document.createElementNS('http://www.w3.org/2000/svg', 'radialGradient');
        entropyGradient.id = 'entropy-gradient';
        entropyGradient.innerHTML = `
            <stop offset="0%" stop-color="#ff0080" stop-opacity="0.8"/>
            <stop offset="50%" stop-color="#8000ff" stop-opacity="0.4"/>
            <stop offset="100%" stop-color="#0080ff" stop-opacity="0.1"/>
        `;
        defs.appendChild(entropyGradient);
        
        // Bloom filter
        const bloomFilter = document.createElementNS('http://www.w3.org/2000/svg', 'filter');
        bloomFilter.id = 'bloom-glow';
        bloomFilter.innerHTML = `
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        `;
        defs.appendChild(bloomFilter);
        
        this.svg.appendChild(defs);
        return defs;
    }
    
    createGroup(id) {
        const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        group.id = id;
        this.svg.appendChild(group);
        return group;
    }
    
    createFractalBloom(id, x, y, metrics) {
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.id = `bloom-${id}`;
        g.setAttribute('transform', `translate(${x}, ${y})`);
        
        // Generate fractal path
        const path = this.generateFractalPath(metrics);
        path.setAttribute('fill', 'none');
        path.setAttribute('stroke', this.getColorFromMetrics(metrics));
        path.setAttribute('stroke-width', '2');
        path.setAttribute('filter', 'url(#bloom-glow)');
        
        g.appendChild(path);
        
        // Add core circle
        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('r', metrics.heat * 10 + 5);
        circle.setAttribute('fill', this.getColorFromMetrics(metrics));
        circle.setAttribute('opacity', 0.8);
        
        g.appendChild(circle);
        
        this.bloomGroup.appendChild(g);
        return g;
    }
    
    generateFractalPath(metrics) {
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        const branches = 3 + Math.floor(metrics.resonance * 3);
        let d = '';
        
        for (let i = 0; i < branches; i++) {
            const angle = (i / branches) * Math.PI * 2;
            const length = 20 + metrics.heat * 20;
            const curve = metrics.entropy * 10;
            
            const x1 = Math.cos(angle) * length;
            const y1 = Math.sin(angle) * length;
            const cx = Math.cos(angle + 0.5) * length * 0.7;
            const cy = Math.sin(angle + 0.5) * length * 0.7 + curve;
            
            d += `M 0,0 Q ${cx},${cy} ${x1},${y1} `;
        }
        
        path.setAttribute('d', d);
        return path;
    }
    
    getColorFromMetrics(metrics) {
        const hue = (metrics.mood + 1) * 120;
        const saturation = 30 + metrics.urgency * 70;
        const lightness = 30 + (1 - metrics.entropy) * 40;
        return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
    }
}

// Export for use
export { DAWNVisualCortex, DAWNFractalSVG };