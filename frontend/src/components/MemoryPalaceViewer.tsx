import { useEffect, useState, useRef } from 'react';

interface MemoryNode {
  id: string;
  type: string;
  content: string;
  timestamp: number;
  connections: string[];
  position: {
    x: number;
    y: number;
    z: number;
  };
  strength: number;
  color: string;
}

interface MemoryConnection {
  from: string;
  to: string;
  strength: number;
}

interface MemoryDetails {
  id: string;
  type: string;
  content: string;
  timestamp: number;
  connections: string[];
  metadata: {
    [key: string]: any;
  };
}

const MemoryPalaceViewer = () => {
  const [nodes, setNodes] = useState<MemoryNode[]>([]);
  const [connections, setConnections] = useState<MemoryConnection[]>([]);
  const [selectedNode, setSelectedNode] = useState<MemoryNode | null>(null);
  const [viewDetails, setViewDetails] = useState<MemoryDetails | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [rotation, setRotation] = useState({ x: 0, y: 0 });

  // WebSocket connection for real-time updates
  useEffect(() => {
    wsRef.current = new WebSocket('ws://localhost:8000/ws');

    wsRef.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'memory_update') {
          handleMemoryUpdate(data);
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  const handleMemoryUpdate = (data: any) => {
    if (data.action === 'add') {
      addMemoryNode(data.memory);
    } else if (data.action === 'update') {
      updateMemoryNode(data.memory);
    } else if (data.action === 'connect') {
      addConnection(data.from, data.to, data.strength);
    }
  };

  const addMemoryNode = (memory: any) => {
    const newNode: MemoryNode = {
      id: memory.id,
      type: memory.type,
      content: memory.content,
      timestamp: memory.timestamp,
      connections: memory.connections || [],
      position: generateRandomPosition(),
      strength: memory.strength || 1,
      color: getMemoryColor(memory.type)
    };

    setNodes(prev => [...prev, newNode]);
    updateConnections(newNode);
  };

  const updateMemoryNode = (memory: any) => {
    setNodes(prev => prev.map(node => 
      node.id === memory.id ? { ...node, ...memory } : node
    ));
  };

  const addConnection = (from: string, to: string, strength: number) => {
    setConnections(prev => [...prev, { from, to, strength }]);
  };

  const updateConnections = (node: MemoryNode) => {
    const newConnections = node.connections.map(targetId => ({
      from: node.id,
      to: targetId,
      strength: 1
    }));
    setConnections(prev => [...prev, ...newConnections]);
  };

  const generateRandomPosition = () => {
    return {
      x: (Math.random() - 0.5) * 800,
      y: (Math.random() - 0.5) * 600,
      z: (Math.random() - 0.5) * 200
    };
  };

  const getMemoryColor = (type: string): string => {
    const colors: { [key: string]: string } = {
      'experience': '#3b82f6', // blue
      'concept': '#10b981', // green
      'emotion': '#f97316', // orange
      'pattern': '#8b5cf6', // purple
      'default': '#00ff88' // default green
    };
    return colors[type] || colors.default;
  };

  const handleNodeClick = async (node: MemoryNode) => {
    setSelectedNode(node);
    try {
      const response = await fetch(`http://localhost:8000/memories/${node.id}`);
      const details = await response.json();
      setViewDetails(details);
    } catch (error) {
      console.error('Error fetching memory details:', error);
    }
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (containerRef.current) {
      const rect = containerRef.current.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width;
      const y = (e.clientY - rect.top) / rect.height;
      setRotation({
        x: (y - 0.5) * 20,
        y: (x - 0.5) * 20
      });
    }
  };

  return (
    <div style={{ position: 'relative', width: '100%', height: '600px' }}>
      {/* 3D Memory Space */}
      <div
        ref={containerRef}
        onMouseMove={handleMouseMove}
        style={{
          position: 'relative',
          width: '100%',
          height: '100%',
          perspective: '1000px',
          transformStyle: 'preserve-3d',
          transform: `rotateX(${rotation.x}deg) rotateY(${rotation.y}deg)`,
          transition: 'transform 0.1s ease-out'
        }}
      >
        {/* Connection Lines */}
        <svg
          style={{
            position: 'absolute',
            width: '100%',
            height: '100%',
            pointerEvents: 'none'
          }}
        >
          {connections.map((conn, index) => {
            const fromNode = nodes.find(n => n.id === conn.from);
            const toNode = nodes.find(n => n.id === conn.to);
            if (!fromNode || !toNode) return null;

            return (
              <line
                key={index}
                x1={fromNode.position.x + 400}
                y1={fromNode.position.y + 300}
                x2={toNode.position.x + 400}
                y2={toNode.position.y + 300}
                stroke={fromNode.color}
                strokeWidth={conn.strength * 2}
                opacity={0.3}
                style={{
                  filter: 'blur(2px)',
                  transition: 'all 0.3s ease'
                }}
              />
            );
          })}
        </svg>

        {/* Memory Nodes */}
        {nodes.map(node => (
          <div
            key={node.id}
            onClick={() => handleNodeClick(node)}
            style={{
              position: 'absolute',
              left: '50%',
              top: '50%',
              transform: `translate3d(${node.position.x}px, ${node.position.y}px, ${node.position.z}px)`,
              width: '40px',
              height: '40px',
              background: `radial-gradient(circle at 30% 30%, ${node.color}, rgba(0,0,0,0.8))`,
              borderRadius: '50%',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              boxShadow: `0 0 20px ${node.color}`,
              border: selectedNode?.id === node.id ? '2px solid #fff' : 'none'
            }}
          />
        ))}
      </div>

      {/* Memory Details Panel */}
      {viewDetails && (
        <div
          style={{
            position: 'absolute',
            right: '2rem',
            top: '2rem',
            background: 'rgba(0, 0, 0, 0.8)',
            backdropFilter: 'blur(8px)',
            WebkitBackdropFilter: 'blur(8px)',
            padding: '1.5rem',
            borderRadius: '1rem',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            maxWidth: '400px',
            color: '#fff',
            fontFamily: 'var(--font-mono)'
          }}
        >
          <h3 style={{ 
            color: getMemoryColor(viewDetails.type),
            marginBottom: '1rem'
          }}>
            {viewDetails.type}
          </h3>
          <div style={{ marginBottom: '1rem' }}>
            <div style={{ color: '#9ca3af', fontSize: '0.875rem' }}>Content</div>
            <div style={{ color: '#fff' }}>{viewDetails.content}</div>
          </div>
          <div style={{ marginBottom: '1rem' }}>
            <div style={{ color: '#9ca3af', fontSize: '0.875rem' }}>Timestamp</div>
            <div style={{ color: '#fff' }}>
              {new Date(viewDetails.timestamp).toLocaleString()}
            </div>
          </div>
          <div>
            <div style={{ color: '#9ca3af', fontSize: '0.875rem' }}>Connections</div>
            <div style={{ color: '#fff' }}>
              {viewDetails.connections.length} connections
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MemoryPalaceViewer; 