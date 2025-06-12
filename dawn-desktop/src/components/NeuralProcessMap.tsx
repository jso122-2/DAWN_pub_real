import React, { useEffect, useRef, useState, useCallback } from 'react';
import * as d3 from 'd3';
import { Brain, Cpu, Zap, Network, Activity, Sparkles } from 'lucide-react';

// Node types for different processing units
const NODE_TYPES = {
  CORE: { icon: Brain, color: '#00ffcc', size: 40 },
  PROCESS: { icon: Cpu, color: '#9945ff', size: 30 },
  MEMORY: { icon: Activity, color: '#ffaa00', size: 25 },
  NEURAL: { icon: Network, color: '#ff0080', size: 35 },
  SPARK: { icon: Sparkles, color: '#14b8a6', size: 20 }
};

interface Node {
  id: string;
  type: keyof typeof NODE_TYPES;
  label: string;
  active: boolean;
  intensity: number;
  x?: number;
  y?: number;
  fx?: number | null;
  fy?: number | null;
}

interface Link {
  source: string | Node;
  target: string | Node;
  strength: number;
}

// Mock data generator - replace with real neural network data
const generateNeuralData = (): { nodes: Node[], links: Link[] } => {
  const nodes: Node[] = [
    { id: 'dawn-core', type: 'CORE', label: 'DAWN Core', active: true, intensity: 0.9 },
    { id: 'claude-api', type: 'NEURAL', label: 'Claude API', active: true, intensity: 0.7 },
    { id: 'cursor-sync', type: 'PROCESS', label: 'Cursor Sync', active: false, intensity: 0.3 },
    { id: 'memory-cortex', type: 'MEMORY', label: 'Memory Cortex', active: true, intensity: 0.6 },
    { id: 'entropy-calc', type: 'SPARK', label: 'Entropy Calculator', active: true, intensity: 0.8 },
    { id: 'sigil-processor', type: 'NEURAL', label: 'Sigil Processor', active: false, intensity: 0.4 },
    { id: 'timeline-engine', type: 'PROCESS', label: 'Timeline Engine', active: true, intensity: 0.5 },
    { id: 'pattern-matcher', type: 'MEMORY', label: 'Pattern Matcher', active: true, intensity: 0.7 }
  ];

  const links: Link[] = [
    { source: 'dawn-core', target: 'claude-api', strength: 0.9 },
    { source: 'dawn-core', target: 'memory-cortex', strength: 0.7 },
    { source: 'claude-api', target: 'cursor-sync', strength: 0.5 },
    { source: 'memory-cortex', target: 'pattern-matcher', strength: 0.8 },
    { source: 'entropy-calc', target: 'dawn-core', strength: 0.6 },
    { source: 'sigil-processor', target: 'memory-cortex', strength: 0.4 },
    { source: 'timeline-engine', target: 'pattern-matcher', strength: 0.6 },
    { source: 'claude-api', target: 'sigil-processor', strength: 0.3 }
  ];

  return { nodes, links };
};

interface NeuralProcessMapProps {
  width?: number;
  height?: number;
}

const NeuralProcessMap: React.FC<NeuralProcessMapProps> = ({ width = 800, height = 600 }) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const [data, setData] = useState(() => generateNeuralData());
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [activityPulse, setActivityPulse] = useState<Record<string, number>>({});
  const simulationRef = useRef<d3.Simulation<Node, Link> | null>(null);

  // Send activity pulse through network
  const sendPulse = useCallback((sourceId: string, targetId: string) => {
    setActivityPulse(prev => ({
      ...prev,
      [`${sourceId}-${targetId}`]: Date.now()
    }));
  }, []);

  // Initialize D3 force simulation
  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    // Create container groups
    const g = svg.append('g');
    const linksGroup = g.append('g').attr('class', 'links');
    const nodesGroup = g.append('g').attr('class', 'nodes');
    const labelsGroup = g.append('g').attr('class', 'labels');

    // Create force simulation
    const simulation = d3.forceSimulation(data.nodes)
      .force('link', d3.forceLink<Node, Link>(data.links).id(d => d.id).distance(150))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide<Node>().radius(d => NODE_TYPES[d.type].size + 10));

    simulationRef.current = simulation;

    // Create gradient definitions
    const defs = svg.append('defs');
    
    // Glow filter
    const filter = defs.append('filter')
      .attr('id', 'glow')
      .attr('x', '-50%')
      .attr('y', '-50%')
      .attr('width', '200%')
      .attr('height', '200%');
    
    filter.append('feGaussianBlur')
      .attr('stdDeviation', '4')
      .attr('result', 'coloredBlur');
    
    const feMerge = filter.append('feMerge');
    feMerge.append('feMergeNode').attr('in', 'coloredBlur');
    feMerge.append('feMergeNode').attr('in', 'SourceGraphic');

    // Create links
    const links = linksGroup.selectAll('line')
      .data(data.links)
      .enter().append('line')
      .attr('stroke', '#ffffff')
      .attr('stroke-opacity', (d: Link) => d.strength * 0.3)
      .attr('stroke-width', (d: Link) => d.strength * 3)
      .attr('filter', 'url(#glow)');

    // Create link paths for animated pulses
    const linkPaths = linksGroup.selectAll('.link-path')
      .data(data.links)
      .enter().append('path')
      .attr('class', 'link-path')
      .attr('id', (d: Link) => {
        const sourceId = typeof d.source === 'string' ? d.source : d.source.id;
        const targetId = typeof d.target === 'string' ? d.target : d.target.id;
        return `path-${sourceId}-${targetId}`;
      })
      .attr('fill', 'none')
      .attr('stroke', 'none');

    // Create nodes
    const nodeGroups = nodesGroup.selectAll('g')
      .data(data.nodes)
      .enter().append('g')
      .attr('class', 'node-group')
      .style('cursor', 'pointer')
      .call(d3.drag<SVGGElement, Node>()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended));

    // Node backgrounds (halos)
    nodeGroups.append('circle')
      .attr('r', (d: Node) => NODE_TYPES[d.type].size + 10)
      .attr('fill', (d: Node) => NODE_TYPES[d.type].color)
      .attr('opacity', (d: Node) => d.active ? 0.2 : 0.1)
      .attr('filter', 'url(#glow)')
      .attr('class', 'node-halo');

    // Node circles
    nodeGroups.append('circle')
      .attr('r', (d: Node) => NODE_TYPES[d.type].size)
      .attr('fill', (d: Node) => d.active ? NODE_TYPES[d.type].color : '#1a1b2e')
      .attr('stroke', (d: Node) => NODE_TYPES[d.type].color)
      .attr('stroke-width', 2)
      .attr('filter', (d: Node) => d.active ? 'url(#glow)' : 'none')
      .attr('class', 'node-circle');

    // Add labels
    const labels = labelsGroup.selectAll('text')
      .data(data.nodes)
      .enter().append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', (d: Node) => NODE_TYPES[d.type].size + 20)
      .attr('fill', '#ffffff')
      .attr('font-size', '12px')
      .attr('font-family', 'monospace')
      .attr('opacity', 0.8)
      .text((d: Node) => d.label);

    // Node click handler
    nodeGroups.on('click', (event: MouseEvent, d: Node) => {
      setSelectedNode(d);
      // Send pulse to connected nodes
      data.links.forEach(link => {
        const sourceId = typeof link.source === 'string' ? link.source : link.source.id;
        const targetId = typeof link.target === 'string' ? link.target : link.target.id;
        if (sourceId === d.id) {
          sendPulse(d.id, targetId);
        }
      });
    });

    // Update positions on simulation tick
    simulation.on('tick', () => {
      links
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      linkPaths
        .attr('d', (d: any) => `M${d.source.x},${d.source.y} L${d.target.x},${d.target.y}`);

      nodeGroups
        .attr('transform', (d: any) => `translate(${d.x},${d.y})`);

      labels
        .attr('x', (d: any) => d.x)
        .attr('y', (d: any) => d.y);
    });

    // Zoom behavior
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.5, 3])
      .on('zoom', (event) => {
        g.attr('transform', event.transform.toString());
      });

    svg.call(zoom);

    // Drag functions
    function dragstarted(event: d3.D3DragEvent<SVGGElement, Node, Node>, d: Node) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event: d3.D3DragEvent<SVGGElement, Node, Node>, d: Node) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event: d3.D3DragEvent<SVGGElement, Node, Node>, d: Node) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    // Animate active nodes
    const animateNodes = () => {
      nodeGroups.selectAll('.node-halo')
        .filter((d: any) => d.active)
        .transition()
        .duration(2000)
        .attr('r', (d: any) => NODE_TYPES[d.type].size + 15)
        .attr('opacity', 0.3)
        .transition()
        .duration(2000)
        .attr('r', (d: any) => NODE_TYPES[d.type].size + 10)
        .attr('opacity', 0.2)
        .on('end', animateNodes);
    };
    animateNodes();

    // Cleanup
    return () => {
      simulation.stop();
    };
  }, [data, width, height, sendPulse]);

  // Animate activity pulses
  useEffect(() => {
    Object.entries(activityPulse).forEach(([pathId, timestamp]) => {
      if (Date.now() - timestamp < 3000) {
        const svg = d3.select(svgRef.current);
        const path = svg.select(`#path-${pathId}`);
        
        if (!path.empty()) {
          const pathNode = path.node() as SVGPathElement;
          const pathLength = pathNode.getTotalLength();
          
          const pulse = svg.append('circle')
            .attr('r', 5)
            .attr('fill', '#00ffcc')
            .attr('filter', 'url(#glow)');
          
          pulse.transition()
            .duration(1500)
            .ease(d3.easeLinear)
            .attrTween('transform', () => {
              return (t: number) => {
                const point = pathNode.getPointAtLength(t * pathLength);
                return `translate(${point.x},${point.y})`;
              };
            })
            .on('end', () => pulse.remove());
        }
      }
    });
  }, [activityPulse]);

  // Simulate data updates
  useEffect(() => {
    const interval = setInterval(() => {
      setData(prev => ({
        ...prev,
        nodes: prev.nodes.map(node => ({
          ...node,
          active: Math.random() > 0.3,
          intensity: Math.random()
        }))
      }));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative glass rounded-lg p-4 bg-black/40 backdrop-blur-xl border border-white/10">
      <div className="absolute top-4 left-4 z-10">
        <h3 className="text-lg font-bold mb-2 text-cyan-300">
          Neural Process Map
        </h3>
        {selectedNode && (
          <div className="glass rounded p-2 mt-2 bg-black/60">
            <p className="text-sm text-gray-300">Selected: {selectedNode.label}</p>
            <p className="text-xs text-gray-400">Type: {selectedNode.type}</p>
            <p className="text-xs text-gray-400">Intensity: {(selectedNode.intensity * 100).toFixed(0)}%</p>
          </div>
        )}
      </div>
      
      <svg 
        ref={svgRef} 
        width={width} 
        height={height}
        className="w-full h-full"
        style={{ background: 'transparent' }}
      />
      
      <div className="absolute bottom-4 right-4 flex gap-2">
        {Object.entries(NODE_TYPES).map(([type, config]) => {
          const Icon = config.icon;
          return (
            <div key={type} className="flex items-center gap-1">
              <Icon size={16} color={config.color} />
              <span className="text-xs text-gray-400">{type}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export { NeuralProcessMap };
