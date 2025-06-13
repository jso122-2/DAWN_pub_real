import React, { useEffect, useRef, useState, useCallback, useMemo } from 'react';
import { motion, AnimatePresence, useSpring, useMotionValue } from 'framer-motion';
import { EventEmitter } from '../../lib/EventEmitter';

// Types
interface Vector2D {
  x: number;
  y: number;
}

interface ModuleNode {
  id: string;
  position: Vector2D;
  velocity: Vector2D;
  mass: number;
  radius: number;
  category: string;
  importance: number; // 0-1, affects z-index
  connections: Set<string>;
  dataFlow: Map<string, number>; // targetId -> flow rate
  group?: string;
  isOrbital?: boolean;
  parentId?: string;
}

interface Connection {
  id: string;
  source: string;
  target: string;
  strength: number; // 0-1
  dataVolume: number; // 0-1
  type: 'data' | 'consciousness' | 'quantum' | 'neural';
  particles: Particle[];
  entangled?: boolean;
}

interface Particle {
  id: string;
  position: Vector2D;
  progress: number; // 0-1 along path
  speed: number;
  size: number;
  color: string;
}

interface SpatialConfig {
  attractionStrength: number;
  repulsionStrength: number;
  damping: number;
  maxVelocity: number;
  connectionDistance: number;
  orbitalRadius: number;
  quantumEntanglementThreshold: number;
}

interface SpatialManagerProps {
  modules: Array<{
    id: string;
    position: Vector2D;
    category: string;
    connections?: string[];
    importance?: number;
    group?: string;
  }>;
  onPositionUpdate: (id: string, position: Vector2D) => void;
  emitter?: EventEmitter;
  config?: Partial<SpatialConfig>;
}

// Default configuration
const DEFAULT_CONFIG: SpatialConfig = {
  attractionStrength: 0.001,
  repulsionStrength: 5000,
  damping: 0.95,
  maxVelocity: 5,
  connectionDistance: 300,
  orbitalRadius: 150,
  quantumEntanglementThreshold: 0.8
};

// Connection type colors
const CONNECTION_COLORS = {
  data: '#3b82f6',
  consciousness: '#a855f7',
  quantum: '#06b6d4',
  neural: '#8b5cf6'
};

// Particle component
const DataParticle: React.FC<{
  particle: Particle;
  path: { start: Vector2D; end: Vector2D };
}> = ({ particle, path }) => {
  const x = path.start.x + (path.end.x - path.start.x) * particle.progress;
  const y = path.start.y + (path.end.y - path.start.y) * particle.progress;
  
  return (
    <motion.div
      className="absolute rounded-full"
      style={{
        left: x,
        top: y,
        width: particle.size,
        height: particle.size,
        backgroundColor: particle.color,
        boxShadow: `0 0 ${particle.size * 2}px ${particle.color}`,
        transform: 'translate(-50%, -50%)'
      }}
      initial={{ opacity: 0, scale: 0 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0 }}
    />
  );
};

// Connection line component with flowing particles
const ConnectionLine: React.FC<{
  connection: Connection;
  sourcePos: Vector2D;
  targetPos: Vector2D;
}> = ({ connection, sourcePos, targetPos }) => {
  const midX = (sourcePos.x + targetPos.x) / 2;
  const midY = (sourcePos.y + targetPos.y) / 2;
  
  // Calculate control points for bezier curve
  const dx = targetPos.x - sourcePos.x;
  const dy = targetPos.y - sourcePos.y;
  const distance = Math.sqrt(dx * dx + dy * dy);
  
  // Quantum entanglement effect
  const entanglementOffset = connection.entangled ? Math.sin(Date.now() * 0.001) * 20 : 0;
  
  const controlPoint1 = {
    x: sourcePos.x + dx * 0.25 + dy * 0.1 + entanglementOffset,
    y: sourcePos.y + dy * 0.25 - dx * 0.1
  };
  
  const controlPoint2 = {
    x: sourcePos.x + dx * 0.75 - dy * 0.1 - entanglementOffset,
    y: sourcePos.y + dy * 0.75 + dx * 0.1
  };
  
  const pathData = `M ${sourcePos.x} ${sourcePos.y} C ${controlPoint1.x} ${controlPoint1.y}, ${controlPoint2.x} ${controlPoint2.y}, ${targetPos.x} ${targetPos.y}`;
  
  return (
    <g>
      {/* Connection line with gradient */}
      <defs>
        <linearGradient id={`gradient-${connection.id}`} x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor={CONNECTION_COLORS[connection.type]} stopOpacity="0.2" />
          <stop offset="50%" stopColor={CONNECTION_COLORS[connection.type]} stopOpacity="0.6" />
          <stop offset="100%" stopColor={CONNECTION_COLORS[connection.type]} stopOpacity="0.2" />
        </linearGradient>
      </defs>
      
      {/* Main connection path */}
      <motion.path
        d={pathData}
        fill="none"
        stroke={`url(#gradient-${connection.id})`}
        strokeWidth={2 + connection.strength * 4}
        initial={{ pathLength: 0, opacity: 0 }}
        animate={{ 
          pathLength: 1, 
          opacity: 0.3 + connection.strength * 0.4,
          strokeWidth: connection.entangled ? 
            [2 + connection.strength * 4, 4 + connection.strength * 6, 2 + connection.strength * 4] : 
            2 + connection.strength * 4
        }}
        transition={{
          pathLength: { duration: 1, ease: "easeOut" },
          opacity: { duration: 0.5 },
          strokeWidth: connection.entangled ? { duration: 2, repeat: Infinity } : undefined
        }}
      />
      
      {/* Glow effect */}
      <motion.path
        d={pathData}
        fill="none"
        stroke={CONNECTION_COLORS[connection.type]}
        strokeWidth={(2 + connection.strength * 4) * 3}
        opacity={0.1}
        filter="blur(8px)"
      />
      
      {/* Data volume indicator */}
      <motion.circle
        cx={midX}
        cy={midY}
        r={5 + connection.dataVolume * 10}
        fill={CONNECTION_COLORS[connection.type]}
        opacity={0.3}
        animate={{
          r: [5 + connection.dataVolume * 10, 8 + connection.dataVolume * 15, 5 + connection.dataVolume * 10],
          opacity: [0.3, 0.5, 0.3]
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
    </g>
  );
};

const SpatialManager: React.FC<SpatialManagerProps> = ({
  modules,
  onPositionUpdate,
  emitter = new EventEmitter(),
  config = {}
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const animationFrameRef = useRef<number>();
  const [nodes, setNodes] = useState<Map<string, ModuleNode>>(new Map());
  const [connections, setConnections] = useState<Map<string, Connection>>(new Map());
  const [dimensions, setDimensions] = useState({ width: window.innerWidth, height: window.innerHeight });
  
  const spatialConfig = { ...DEFAULT_CONFIG, ...config };
  
  // Initialize nodes from modules
  useEffect(() => {
    const newNodes = new Map<string, ModuleNode>();
    
    modules.forEach(module => {
      newNodes.set(module.id, {
        id: module.id,
        position: { ...module.position },
        velocity: { x: 0, y: 0 },
        mass: 1,
        radius: 50,
        category: module.category,
        importance: module.importance || 0.5,
        connections: new Set(module.connections || []),
        dataFlow: new Map(),
        group: module.group,
        isOrbital: false,
        parentId: undefined
      });
    });
    
    setNodes(newNodes);
  }, [modules]);
  
  // Create connections between nodes
  useEffect(() => {
    const newConnections = new Map<string, Connection>();
    
    nodes.forEach((sourceNode, sourceId) => {
      sourceNode.connections.forEach(targetId => {
        if (nodes.has(targetId)) {
          const connectionId = `${sourceId}-${targetId}`;
          const reverseId = `${targetId}-${sourceId}`;
          
          // Avoid duplicate connections
          if (!newConnections.has(connectionId) && !newConnections.has(reverseId)) {
            const targetNode = nodes.get(targetId)!;
            const distance = Math.sqrt(
              Math.pow(targetNode.position.x - sourceNode.position.x, 2) +
              Math.pow(targetNode.position.y - sourceNode.position.y, 2)
            );
            
            const strength = Math.max(0, 1 - distance / spatialConfig.connectionDistance);
            const dataVolume = sourceNode.dataFlow.get(targetId) || 0.5;
            
            // Determine connection type based on categories
            let type: Connection['type'] = 'data';
            if (sourceNode.category === 'neural' && targetNode.category === 'neural') {
              type = 'neural';
            } else if (sourceNode.category === 'quantum' || targetNode.category === 'quantum') {
              type = 'quantum';
            } else if (sourceNode.category === 'neural' || targetNode.category === 'neural') {
              type = 'consciousness';
            }
            
            newConnections.set(connectionId, {
              id: connectionId,
              source: sourceId,
              target: targetId,
              strength,
              dataVolume,
              type,
              particles: [],
              entangled: type === 'quantum' && strength > spatialConfig.quantumEntanglementThreshold
            });
          }
        }
      });
    });
    
    setConnections(newConnections);
  }, [nodes, spatialConfig]);
  
  // Physics simulation
  const updatePhysics = useCallback(() => {
    const newNodes = new Map(nodes);
    const groups = new Map<string, Set<string>>();
    
    // Group nodes by their group ID
    newNodes.forEach((node, id) => {
      if (node.group) {
        if (!groups.has(node.group)) {
          groups.set(node.group, new Set());
        }
        groups.get(node.group)!.add(id);
      }
    });
    
    // Apply forces
    newNodes.forEach((node, nodeId) => {
      if (node.isOrbital && node.parentId) {
        // Orbital movement for subsidiary modules
        const parent = newNodes.get(node.parentId);
        if (parent) {
          const angle = Date.now() * 0.001 + parseFloat(nodeId) * Math.PI;
          node.position.x = parent.position.x + Math.cos(angle) * spatialConfig.orbitalRadius;
          node.position.y = parent.position.y + Math.sin(angle) * spatialConfig.orbitalRadius;
        }
      } else {
        // Regular physics for main modules
        let forceX = 0;
        let forceY = 0;
        
        // Apply forces from all other nodes
        newNodes.forEach((otherNode, otherId) => {
          if (nodeId === otherId) return;
          
          const dx = otherNode.position.x - node.position.x;
          const dy = otherNode.position.y - node.position.y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          
          if (distance > 0) {
            // Repulsion force (collision avoidance)
            if (distance < node.radius + otherNode.radius + 50) {
              const repulsion = spatialConfig.repulsionStrength / (distance * distance);
              forceX -= (dx / distance) * repulsion;
              forceY -= (dy / distance) * repulsion;
            }
            
            // Attraction force for connected nodes
            if (node.connections.has(otherId)) {
              const attraction = distance * spatialConfig.attractionStrength;
              forceX += (dx / distance) * attraction;
              forceY += (dy / distance) * attraction;
            }
            
            // Group cohesion
            if (node.group && node.group === otherNode.group && distance > 200) {
              const cohesion = spatialConfig.attractionStrength * 2;
              forceX += (dx / distance) * cohesion;
              forceY += (dy / distance) * cohesion;
            }
          }
        });
        
        // Apply forces to velocity
        node.velocity.x += forceX;
        node.velocity.y += forceY;
        
        // Apply damping
        node.velocity.x *= spatialConfig.damping;
        node.velocity.y *= spatialConfig.damping;
        
        // Limit velocity
        const speed = Math.sqrt(node.velocity.x * node.velocity.x + node.velocity.y * node.velocity.y);
        if (speed > spatialConfig.maxVelocity) {
          node.velocity.x = (node.velocity.x / speed) * spatialConfig.maxVelocity;
          node.velocity.y = (node.velocity.y / speed) * spatialConfig.maxVelocity;
        }
        
        // Update position
        node.position.x += node.velocity.x;
        node.position.y += node.velocity.y;
        
        // Keep within bounds with elastic bouncing
        const margin = 50;
        if (node.position.x < margin) {
          node.position.x = margin;
          node.velocity.x = Math.abs(node.velocity.x) * 0.8;
        } else if (node.position.x > dimensions.width - margin) {
          node.position.x = dimensions.width - margin;
          node.velocity.x = -Math.abs(node.velocity.x) * 0.8;
        }
        
        if (node.position.y < margin) {
          node.position.y = margin;
          node.velocity.y = Math.abs(node.velocity.y) * 0.8;
        } else if (node.position.y > dimensions.height - margin) {
          node.position.y = dimensions.height - margin;
          node.velocity.y = -Math.abs(node.velocity.y) * 0.8;
        }
      }
      
      // Notify position update
      onPositionUpdate(nodeId, node.position);
    });
    
    setNodes(newNodes);
  }, [nodes, dimensions, spatialConfig, onPositionUpdate]);
  
  // Update particles in connections
  const updateParticles = useCallback(() => {
    setConnections(prevConnections => {
      const newConnections = new Map(prevConnections);
      
      newConnections.forEach((connection, id) => {
        // Update existing particles
        connection.particles = connection.particles
          .map(particle => ({
            ...particle,
            progress: particle.progress + particle.speed
          }))
          .filter(particle => particle.progress <= 1);
        
        // Spawn new particles based on data volume
        if (Math.random() < connection.dataVolume * 0.1) {
          connection.particles.push({
            id: `${id}-${Date.now()}`,
            position: { x: 0, y: 0 },
            progress: 0,
            speed: 0.01 + connection.dataVolume * 0.02,
            size: 2 + connection.strength * 4,
            color: CONNECTION_COLORS[connection.type]
          });
        }
      });
      
      return newConnections;
    });
  }, []);
  
  // Animation loop
  useEffect(() => {
    const animate = () => {
      updatePhysics();
      updateParticles();
      animationFrameRef.current = requestAnimationFrame(animate);
    };
    
    animationFrameRef.current = requestAnimationFrame(animate);
    
    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [updatePhysics, updateParticles]);
  
  // Handle window resize
  useEffect(() => {
    const handleResize = () => {
      setDimensions({ width: window.innerWidth, height: window.innerHeight });
    };
    
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);
  
  // Calculate z-index layers based on importance
  const sortedNodes = useMemo(() => {
    return Array.from(nodes.entries()).sort((a, b) => a[1].importance - b[1].importance);
  }, [nodes]);
  
  return (
    <div className="absolute inset-0 pointer-events-none">
      <svg
        ref={svgRef}
        className="absolute inset-0 w-full h-full"
        style={{ zIndex: 1 }}
      >
        {/* Render connections */}
        <g className="connections">
          {Array.from(connections.values()).map(connection => {
            const sourceNode = nodes.get(connection.source);
            const targetNode = nodes.get(connection.target);
            
            if (!sourceNode || !targetNode) return null;
            
            return (
              <ConnectionLine
                key={connection.id}
                connection={connection}
                sourcePos={sourceNode.position}
                targetPos={targetNode.position}
              />
            );
          })}
        </g>
      </svg>
      
      {/* Render particles */}
      <div className="absolute inset-0" style={{ zIndex: 2 }}>
        <AnimatePresence>
          {Array.from(connections.values()).flatMap(connection => {
            const sourceNode = nodes.get(connection.source);
            const targetNode = nodes.get(connection.target);
            
            if (!sourceNode || !targetNode) return [];
            
            return connection.particles.map(particle => (
              <DataParticle
                key={particle.id}
                particle={particle}
                path={{
                  start: sourceNode.position,
                  end: targetNode.position
                }}
              />
            ));
          })}
        </AnimatePresence>
      </div>
      
      {/* Group indicators */}
      <div className="absolute inset-0" style={{ zIndex: 0 }}>
        {Array.from(new Set(Array.from(nodes.values()).map(n => n.group)))
          .filter(Boolean)
          .map(groupId => {
            const groupNodes = Array.from(nodes.values()).filter(n => n.group === groupId);
            if (groupNodes.length === 0) return null;
            
            // Calculate group center
            const centerX = groupNodes.reduce((sum, n) => sum + n.position.x, 0) / groupNodes.length;
            const centerY = groupNodes.reduce((sum, n) => sum + n.position.y, 0) / groupNodes.length;
            
            // Calculate group radius
            const radius = Math.max(...groupNodes.map(n => 
              Math.sqrt(Math.pow(n.position.x - centerX, 2) + Math.pow(n.position.y - centerY, 2))
            )) + 100;
            
            return (
              <motion.div
                key={groupId}
                className="absolute rounded-full"
                style={{
                  left: centerX,
                  top: centerY,
                  width: radius * 2,
                  height: radius * 2,
                  transform: 'translate(-50%, -50%)',
                  background: `radial-gradient(circle, rgba(168, 85, 247, 0.1) 0%, transparent 70%)`,
                  border: '1px solid rgba(168, 85, 247, 0.2)'
                }}
                animate={{
                  scale: [1, 1.05, 1],
                  opacity: [0.3, 0.5, 0.3]
                }}
                transition={{
                  duration: 4,
                  repeat: Infinity,
                  ease: 'easeInOut'
                }}
              />
            );
          })}
      </div>
    </div>
  );
};

export default SpatialManager;