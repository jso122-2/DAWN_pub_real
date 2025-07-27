import React, { useRef, useEffect, useState, useCallback } from 'react';
import './MyceliumOverlay.css';

interface MyceliumNode {
  id: string;
  label: string;
  type: string;
  tick_created?: number;
  timestamp: number;
  connections?: number;
  x?: number;
  y?: number;
  vx?: number;
  vy?: number;
}

interface MyceliumEdge {
  id: string;
  from: string;
  to: string;
  type: string;
  weight: number;
  tick_created?: number;
  timestamp: number;
}

interface MyceliumGraph {
  metadata: {
    export_time: string;
    timestamp: number;
    tick_id?: number;
    node_count: number;
    edge_count: number;
    source: string;
  };
  nodes: MyceliumNode[];
  edges: MyceliumEdge[];
}

const EnhancedMyceliumOverlay: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>();
  const [graph, setGraph] = useState<MyceliumGraph | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [lastUpdate, setLastUpdate] = useState<number>(0);
  const [isAnimating, setIsAnimating] = useState(true);
  const [hoveredNode, setHoveredNode] = useState<string | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<string>('disconnected');
  const [autoRefresh, setAutoRefresh] = useState<boolean>(true);
  
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

  // Auto-refresh interval
  const refreshIntervalRef = useRef<number>();

  const loadGraphData = useCallback(async () => {
    if (isLoading) return;
    
    setIsLoading(true);
    setConnectionStatus('loading');
    
    try {
      const response = await fetch('/api/memory/mycelium_graph');
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      const data: MyceliumGraph = await response.json();
      
      // Validate data structure
      if (!data.nodes || !data.edges || !data.metadata) {
        throw new Error('Invalid graph data structure');
      }
      
      setGraph(data);
      setLastUpdate(Date.now());
      setConnectionStatus('connected');
      
      // Initialize simulation with new data
      if (data.nodes.length > 0) {
        initializeSimulation(data);
      }
      
    } catch (error) {
      console.error('Error loading mycelium graph:', error);
      setConnectionStatus('error');
      
      // Use mock data for demo if real data unavailable in development
      if (typeof window !== 'undefined' && window.location.hostname === 'localhost') {
        setGraph(createMockGraphData());
        setConnectionStatus('mock');
      }
    } finally {
      setIsLoading(false);
    }
  }, [isLoading]);

  const createMockGraphData = (): MyceliumGraph => {
    const nodes: MyceliumNode[] = [];
    const edges: MyceliumEdge[] = [];
    
    // Create some mock nodes
    for (let i = 0; i < 8; i++) {
      nodes.push({
        id: `memory_${i}`,
        label: `Memory ${i}`,
        type: 'memory_chunk',
        timestamp: Date.now() - (i * 10000),
        connections: Math.floor(Math.random() * 3) + 1
      });
    }
    
    // Create some mock edges
    for (let i = 0; i < nodes.length - 1; i++) {
      if (Math.random() > 0.3) {
        edges.push({
          id: `edge_${i}`,
          from: nodes[i].id,
          to: nodes[i + 1].id,
          type: 'semantic_link',
          weight: Math.random(),
          timestamp: Date.now()
        });
      }
    }
    
    return {
      metadata: {
        export_time: new Date().toISOString(),
        timestamp: Date.now(),
        node_count: nodes.length,
        edge_count: edges.length,
        source: 'mock_data'
      },
      nodes,
      edges
    };
  };

  const initializeSimulation = (graphData: MyceliumGraph) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const rect = canvas.getBoundingClientRect();
    simulation.current.width = rect.width;
    simulation.current.height = rect.height;
    
    // Initialize node positions
    simulation.current.nodes = graphData.nodes.map(node => ({
      ...node,
      x: Math.random() * simulation.current.width,
      y: Math.random() * simulation.current.height,
      vx: 0,
      vy: 0
    }));
    
    simulation.current.edges = [...graphData.edges];
    
    if (isAnimating) {
      startAnimation();
    }
  };

  const startAnimation = () => {
    if (animationRef.current) return;
    
    const animate = () => {
      updateSimulation();
      render();
      animationRef.current = requestAnimationFrame(animate);
    };
    
    animationRef.current = requestAnimationFrame(animate);
  };

  const stopAnimation = () => {
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
      animationRef.current = undefined;
    }
  };

  const updateSimulation = () => {
    const sim = simulation.current;
    const centerX = sim.width / 2;
    const centerY = sim.height / 2;
    
    // Apply forces to each node
    for (const node of sim.nodes) {
      if (!node.x || !node.y || !node.vx || !node.vy) continue;
      
      // Center force
      const centerDx = centerX - node.x;
      const centerDy = centerY - node.y;
      node.vx += centerDx * sim.centerForceStrength;
      node.vy += centerDy * sim.centerForceStrength;
      
      // Repulsion between nodes
      for (const other of sim.nodes) {
        if (other.id === node.id || !other.x || !other.y || !node.x || !node.y || !node.vx || !node.vy) continue;
        
        const dx = node.x - other.x;
        const dy = node.y - other.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance > 0 && distance < 100) {
          const force = sim.chargeForceStrength / (distance * distance);
          node.vx += (dx / distance) * force;
          node.vy += (dy / distance) * force;
        }
      }
      
      // Link forces
      for (const edge of sim.edges) {
        let targetNode: MyceliumNode | undefined;
        let isSource = false;
        
        if (edge.from === node.id) {
          targetNode = sim.nodes.find(n => n.id === edge.to);
          isSource = true;
        } else if (edge.to === node.id) {
          targetNode = sim.nodes.find(n => n.id === edge.from);
          isSource = false;
        }
        
        if (targetNode && targetNode.x && targetNode.y) {
          const dx = targetNode.x - node.x;
          const dy = targetNode.y - node.y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          const targetDistance = 80;
          
          if (distance > 0) {
            const force = (distance - targetDistance) * sim.linkForceStrength * edge.weight;
            node.vx += (dx / distance) * force;
            node.vy += (dy / distance) * force;
          }
        }
      }
      
      // Apply dampening
      node.vx *= sim.dampening;
      node.vy *= sim.dampening;
      
      // Update position
      node.x += node.vx;
      node.y += node.vy;
      
      // Boundary constraints
      node.x = Math.max(20, Math.min(sim.width - 20, node.x));
      node.y = Math.max(20, Math.min(sim.height - 20, node.y));
    }
  };

  const render = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw edges
    ctx.strokeStyle = '#444';
    ctx.lineWidth = 1;
    
    for (const edge of simulation.current.edges) {
      const fromNode = simulation.current.nodes.find(n => n.id === edge.from);
      const toNode = simulation.current.nodes.find(n => n.id === edge.to);
      
      if (fromNode && toNode && fromNode.x && fromNode.y && toNode.x && toNode.y) {
        // Animate new edges
        const age = Date.now() - edge.timestamp;
        if (age < 5000) { // Highlight new edges for 5 seconds
          ctx.strokeStyle = `rgba(79, 171, 247, ${Math.max(0, 1 - age / 5000)})`;
          ctx.lineWidth = 2;
        } else {
          ctx.strokeStyle = '#444';
          ctx.lineWidth = 1;
        }
        
        ctx.beginPath();
        ctx.moveTo(fromNode.x, fromNode.y);
        ctx.lineTo(toNode.x, toNode.y);
        ctx.stroke();
      }
    }
    
    // Draw nodes
    for (const node of simulation.current.nodes) {
      if (!node.x || !node.y) continue;
      
      const isHovered = hoveredNode === node.id;
      const radius = isHovered ? 12 : 8;
      
      // Node color based on type and age
      let fillColor = '#2196F3';
      const age = Date.now() - node.timestamp;
      
      if (node.type === 'memory_chunk') {
        fillColor = age < 10000 ? '#4CAF50' : '#2196F3'; // Green for new, blue for established
      }
      
      if (isHovered) {
        fillColor = '#FF9800'; // Orange for hovered
      }
      
      // Draw node
      ctx.fillStyle = fillColor;
      ctx.beginPath();
      ctx.arc(node.x, node.y, radius, 0, Math.PI * 2);
      ctx.fill();
      
      // Draw node border
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 2;
      ctx.stroke();
      
      // Draw connection count
      if (node.connections && node.connections > 0) {
        ctx.fillStyle = '#fff';
        ctx.font = '10px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(node.connections.toString(), node.x, node.y + 3);
      }
      
      // Draw label for hovered node
      if (isHovered) {
        ctx.fillStyle = '#333';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(node.label, node.x, node.y - 20);
      }
    }
  };

  const handleMouseMove = (event: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    
    // Find hovered node
    let hoveredNodeId: string | null = null;
    
    for (const node of simulation.current.nodes) {
      if (!node.x || !node.y) continue;
      
      const distance = Math.sqrt((x - node.x) ** 2 + (y - node.y) ** 2);
      if (distance < 15) {
        hoveredNodeId = node.id;
        break;
      }
    }
    
    setHoveredNode(hoveredNodeId);
  };

  const handleMouseLeave = () => {
    setHoveredNode(null);
  };

  const toggleAnimation = () => {
    setIsAnimating(!isAnimating);
  };

  const resetPositions = () => {
    if (graph) {
      initializeSimulation(graph);
    }
  };

  const getConnectionStatusClass = (): string => {
    switch (connectionStatus) {
      case 'connected': return 'status-connected';
      case 'loading': return 'status-loading';
      case 'error': return 'status-error';
      case 'mock': return 'status-mock';
      default: return 'status-disconnected';
    }
  };

  // Auto-refresh setup
  useEffect(() => {
    if (autoRefresh) {
      refreshIntervalRef.current = window.setInterval(() => {
        loadGraphData();
      }, 5000); // Refresh every 5 seconds
    } else {
      if (refreshIntervalRef.current) {
        clearInterval(refreshIntervalRef.current);
      }
    }
    
    return () => {
      if (refreshIntervalRef.current) {
        clearInterval(refreshIntervalRef.current);
      }
    };
  }, [autoRefresh, loadGraphData]);

  // Animation control
  useEffect(() => {
    if (isAnimating) {
      startAnimation();
    } else {
      stopAnimation();
    }
    
    return () => stopAnimation();
  }, [isAnimating]);

  // Initial load
  useEffect(() => {
    loadGraphData();
  }, [loadGraphData]);

  // Canvas resize handling
  useEffect(() => {
    const handleResize = () => {
      const canvas = canvasRef.current;
      if (!canvas) return;
      
      const rect = canvas.getBoundingClientRect();
      canvas.width = rect.width;
      canvas.height = rect.height;
      simulation.current.width = rect.width;
      simulation.current.height = rect.height;
    };
    
    handleResize();
    window.addEventListener('resize', handleResize);
    
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div className="mycelium-overlay enhanced">
      <div className="overlay-header">
        <h3>🧬 Enhanced Memory Network Graph</h3>
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
          <button
            className={`control-button ${autoRefresh ? 'active' : ''}`}
            onClick={() => setAutoRefresh(!autoRefresh)}
          >
            {autoRefresh ? '🔄 Auto' : '⏸️ Manual'}
          </button>
        </div>
      </div>

      <div className="overlay-stats">
        {graph && (
          <>
            <span className="stat">Nodes: {graph.metadata.node_count}</span>
            <span className="stat">Edges: {graph.metadata.edge_count}</span>
            <span className="stat">
              Density: {graph.metadata.edge_count > 0 && graph.metadata.node_count > 1 
                ? ((2 * graph.metadata.edge_count) / (graph.metadata.node_count * (graph.metadata.node_count - 1)) * 100).toFixed(1)
                : 0}%
            </span>
            <span className="stat">
              Source: {graph.metadata.source}
            </span>
          </>
        )}
        <span className={`stat ${getConnectionStatusClass()}`}>
          {connectionStatus.toUpperCase()}
        </span>
        {lastUpdate > 0 && (
          <span className="stat">
            Updated: {new Date(lastUpdate).toLocaleTimeString()}
          </span>
        )}
      </div>

      <div className="canvas-container">
        <canvas
          ref={canvasRef}
          onMouseMove={handleMouseMove}
          onMouseLeave={handleMouseLeave}
          className="mycelium-canvas"
          width={800}
          height={600}
        />
        
        {hoveredNode && graph && (
          <div className="node-tooltip">
            {(() => {
              const node = graph.nodes.find(n => n.id === hoveredNode);
              return node ? (
                <div>
                  <div className="tooltip-title">{node.label}</div>
                  <div className="tooltip-info">Type: {node.type}</div>
                  <div className="tooltip-info">Connections: {node.connections || 0}</div>
                  {node.tick_created && (
                    <div className="tooltip-info">Created: Tick {node.tick_created}</div>
                  )}
                  <div className="tooltip-info">
                    Time: {new Date(node.timestamp * 1000).toLocaleString()}
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
          <div>
            {connectionStatus === 'error' 
              ? 'Connection failed - check if cognition runtime is active'
              : 'Run the cognition runtime to generate network data'
            }
          </div>
          {connectionStatus === 'error' && typeof window !== 'undefined' && window.location.hostname === 'localhost' && (
            <button 
              className="control-button"
              onClick={() => {
                setGraph(createMockGraphData());
                setConnectionStatus('mock');
              }}
            >
              📊 Load Demo Data
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default EnhancedMyceliumOverlay; 