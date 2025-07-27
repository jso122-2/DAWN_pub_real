import React, { useRef, useEffect, useState, useCallback } from 'react';
import './MyceliumOverlay.css';

interface MyceliumNode {
  id: string;
  label: string;
  type: string;
  connections: number;
  timestamp: number;
  x?: number;
  y?: number;
  vx?: number;
  vy?: number;
  radius?: number;
}

interface MyceliumEdge {
  id: string;
  from: string;
  to: string;
  type: string;
  weight: number;
  timestamp: number;
}

interface MyceliumGraph {
  metadata: {
    export_time: string;
    timestamp: number;
    node_count: number;
    edge_count: number;
    density: number;
    source: string;
  };
  nodes: MyceliumNode[];
  edges: MyceliumEdge[];
  clusters: any[];
  routing_paths: any[];
}

const MyceliumOverlay: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>();
  const [graph, setGraph] = useState<MyceliumGraph | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [lastUpdate, setLastUpdate] = useState<number>(0);
  const [isAnimating, setIsAnimating] = useState(true);
  const [hoveredNode, setHoveredNode] = useState<string | null>(null);

  // Physics simulation parameters
  const simulation = useRef({
    nodes: [] as MyceliumNode[],
    edges: [] as MyceliumEdge[],
    centerForceStrength: 0.02,
    linkForceStrength: 0.1,
    chargeForceStrength: -100,
    dampening: 0.9,
    width: 800,
    height: 600
  });

  // Load graph data
  const loadGraphData = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/memory/mycelium_graph');
      if (response.ok) {
        const graphData: MyceliumGraph = await response.json();
        setGraph(graphData);
        initializeSimulation(graphData);
        setLastUpdate(Date.now());
      }
    } catch (error) {
      console.error('Error loading mycelium graph:', error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Initialize physics simulation
  const initializeSimulation = (graphData: MyceliumGraph) => {
    if (!canvasRef.current) return;

    const canvas = canvasRef.current;
    const width = canvas.width;
    const height = canvas.height;

    // Initialize nodes with random positions
    const nodes = graphData.nodes.map(node => ({
      ...node,
      x: Math.random() * width,
      y: Math.random() * height,
      vx: 0,
      vy: 0,
      radius: Math.max(8, Math.min(20, 8 + node.connections * 2))
    }));

    simulation.current = {
      ...simulation.current,
      nodes,
      edges: graphData.edges,
      width,
      height
    };

    if (isAnimating) {
      startAnimation();
    }
  };

  // Start animation loop
  const startAnimation = () => {
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
    }

    const animate = () => {
      updateSimulation();
      render();
      animationRef.current = requestAnimationFrame(animate);
    };

    animate();
  };

  // Update physics simulation
  const updateSimulation = () => {
    const { nodes, edges, centerForceStrength, linkForceStrength, chargeForceStrength, dampening, width, height } = simulation.current;

    // Apply forces
    nodes.forEach(node => {
      if (!node.x || !node.y || !node.vx || !node.vy) return;

      // Center force
      const centerX = width / 2;
      const centerY = height / 2;
      const dx = centerX - node.x;
      const dy = centerY - node.y;
      node.vx += dx * centerForceStrength;
      node.vy += dy * centerForceStrength;

             // Charge force (repulsion between nodes)
       nodes.forEach(other => {
         if (other.id === node.id || !other.x || !other.y || !node.x || !node.y || !node.vx || !node.vy) return;
         
         const dx = node.x - other.x;
         const dy = node.y - other.y;
         const distance = Math.sqrt(dx * dx + dy * dy);
         
         if (distance > 0) {
           const force = chargeForceStrength / (distance * distance);
           node.vx += (dx / distance) * force;
           node.vy += (dy / distance) * force;
         }
       });
    });

    // Link forces
    edges.forEach(edge => {
      const source = nodes.find(n => n.id === edge.from);
      const target = nodes.find(n => n.id === edge.to);
      
      if (!source || !target || !source.x || !source.y || !target.x || !target.y) return;

      const dx = target.x - source.x;
      const dy = target.y - source.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance > 0) {
        const idealDistance = 100;
        const force = (distance - idealDistance) * linkForceStrength * edge.weight;
        
        const fx = (dx / distance) * force;
        const fy = (dy / distance) * force;
        
        source.vx! += fx;
        source.vy! += fy;
        target.vx! -= fx;
        target.vy! -= fy;
      }
    });

    // Update positions and apply dampening
    nodes.forEach(node => {
      if (!node.x || !node.y || !node.vx || !node.vy) return;

      node.vx *= dampening;
      node.vy *= dampening;
      
      node.x += node.vx;
      node.y += node.vy;

      // Keep nodes within bounds
      const margin = node.radius || 8;
      node.x = Math.max(margin, Math.min(width - margin, node.x));
      node.y = Math.max(margin, Math.min(height - margin, node.y));
    });
  };

  // Render the graph
  const render = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const { nodes, edges } = simulation.current;

    // Clear canvas
    ctx.fillStyle = '#1e2328';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw edges
    ctx.strokeStyle = '#394b59';
    ctx.lineWidth = 1;
    
    edges.forEach(edge => {
      const source = nodes.find(n => n.id === edge.from);
      const target = nodes.find(n => n.id === edge.to);
      
      if (!source || !target || !source.x || !source.y || !target.x || !target.y) return;

      // Adjust opacity based on edge weight
      ctx.globalAlpha = Math.min(1, edge.weight * 0.8 + 0.2);
      
      ctx.beginPath();
      ctx.moveTo(source.x, source.y);
      ctx.lineTo(target.x, target.y);
      ctx.stroke();
    });

    ctx.globalAlpha = 1;

    // Draw nodes
    nodes.forEach(node => {
      if (!node.x || !node.y) return;

      const radius = node.radius || 8;
      const isHovered = hoveredNode === node.id;

      // Node color based on type
      let color = '#48aff0';
      switch (node.type) {
        case 'memory_chunk': color = '#51cf66'; break;
        case 'mycelium_root': color = '#69db7c'; break;
        case 'rebloom_node': color = '#ffa500'; break;
        case 'consciousness_node': color = '#845ec2'; break;
        default: color = '#48aff0';
      }

      // Draw node
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(node.x, node.y, radius, 0, 2 * Math.PI);
      ctx.fill();

      // Draw node border
      ctx.strokeStyle = isHovered ? '#ffffff' : '#1e2328';
      ctx.lineWidth = isHovered ? 3 : 2;
      ctx.stroke();

      // Draw node label if hovered
      if (isHovered) {
        ctx.fillStyle = '#f5f8fa';
        ctx.font = '12px monospace';
        ctx.textAlign = 'center';
        ctx.fillText(node.label, node.x, node.y - radius - 8);
      }
    });
  };

  // Handle mouse events
  const handleMouseMove = (event: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    // Find hovered node
    const { nodes } = simulation.current;
    const hoveredNodeId = nodes.find(node => {
      if (!node.x || !node.y) return false;
      const radius = node.radius || 8;
      const dx = x - node.x;
      const dy = y - node.y;
      return Math.sqrt(dx * dx + dy * dy) <= radius;
    })?.id || null;

    setHoveredNode(hoveredNodeId);
  };

  const handleMouseLeave = () => {
    setHoveredNode(null);
  };

  // Setup canvas and load initial data
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    // Set canvas size
    const updateCanvasSize = () => {
      const container = canvas.parentElement;
      if (container) {
        canvas.width = container.clientWidth;
        canvas.height = container.clientHeight;
        simulation.current.width = canvas.width;
        simulation.current.height = canvas.height;
      }
    };

    updateCanvasSize();
    window.addEventListener('resize', updateCanvasSize);

    // Load initial data
    loadGraphData();

    return () => {
      window.removeEventListener('resize', updateCanvasSize);
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [loadGraphData]);

  // Auto-refresh data
  useEffect(() => {
    const interval = setInterval(loadGraphData, 10000); // Refresh every 10 seconds
    return () => clearInterval(interval);
  }, [loadGraphData]);

  const toggleAnimation = () => {
    setIsAnimating(!isAnimating);
    if (!isAnimating) {
      startAnimation();
    } else if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
    }
  };

  const resetPositions = () => {
    if (graph) {
      initializeSimulation(graph);
    }
  };

  return (
    <div className="mycelium-overlay">
      <div className="overlay-header">
        <h3>🧬 Memory Network Graph</h3>
        <div className="overlay-controls">
          <button 
            className={`control-button ${isAnimating ? 'active' : ''}`}
            onClick={toggleAnimation}
          >
            {isAnimating ? '⏸️ Pause' : '▶️ Animate'}
          </button>
          <button 
            className="control-button"
            onClick={resetPositions}
          >
            🔄 Reset
          </button>
          <button 
            className="control-button"
            onClick={loadGraphData}
            disabled={isLoading}
          >
            {isLoading ? '⏳ Loading...' : '🔄 Refresh'}
          </button>
        </div>
      </div>

      {graph && (
        <div className="overlay-stats">
          <span className="stat">Nodes: {graph.metadata.node_count}</span>
          <span className="stat">Edges: {graph.metadata.edge_count}</span>
          <span className="stat">Density: {(graph.metadata.density * 100).toFixed(1)}%</span>
          <span className="stat">Updated: {new Date(lastUpdate).toLocaleTimeString()}</span>
        </div>
      )}

      <div className="canvas-container">
        <canvas
          ref={canvasRef}
          onMouseMove={handleMouseMove}
          onMouseLeave={handleMouseLeave}
          className="mycelium-canvas"
        />
        
        {hoveredNode && graph && (
          <div className="node-tooltip">
            {(() => {
              const node = graph.nodes.find(n => n.id === hoveredNode);
              return node ? (
                <div>
                  <div className="tooltip-title">{node.label}</div>
                  <div className="tooltip-info">Type: {node.type}</div>
                  <div className="tooltip-info">Connections: {node.connections}</div>
                  <div className="tooltip-info">
                    Created: {new Date(node.timestamp * 1000).toLocaleString()}
                  </div>
                </div>
              ) : null;
            })()}
          </div>
        )}
      </div>

      {!graph && !isLoading && (
        <div className="no-data">
          <div>🌿 No memory network data available</div>
          <div>Run the cognition runtime to generate network data</div>
        </div>
      )}
    </div>
  );
};

export default MyceliumOverlay; 