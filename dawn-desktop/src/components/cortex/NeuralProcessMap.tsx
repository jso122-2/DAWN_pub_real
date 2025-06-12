import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';

interface NeuralNode {
  id: string;
  label: string;
  type: 'processor' | 'memory' | 'sensor' | 'actuator';
  activity: number; // 0-1
  x?: number;
  y?: number;
}

interface NeuralEdge {
  source: string;
  target: string;
  strength: number; // 0-1
  active: boolean;
}

interface NeuralData {
  nodes: NeuralNode[];
  edges: NeuralEdge[];
}

const NeuralProcessMap: React.FC = () => {
  const svgRef = useRef<SVGSVGElement>(null);
  const [data, setData] = useState<NeuralData>({
    nodes: [
      { id: 'core', label: 'Core Processor', type: 'processor', activity: 0.8 },
      { id: 'mem1', label: 'Symbolic Memory', type: 'memory', activity: 0.6 },
      { id: 'vis1', label: 'Visual Cortex', type: 'sensor', activity: 0.9 },
      { id: 'lang1', label: 'Language Model', type: 'processor', activity: 0.7 },
      { id: 'act1', label: 'Action Planner', type: 'actuator', activity: 0.5 },
      { id: 'mem2', label: 'Working Memory', type: 'memory', activity: 0.4 },
      { id: 'sens1', label: 'Input Parser', type: 'sensor', activity: 0.8 },
    ],
    edges: [
      { source: 'core', target: 'mem1', strength: 0.8, active: true },
      { source: 'vis1', target: 'core', strength: 0.7, active: true },
      { source: 'core', target: 'lang1', strength: 0.9, active: true },
      { source: 'lang1', target: 'act1', strength: 0.6, active: false },
      { source: 'mem1', target: 'mem2', strength: 0.5, active: true },
      { source: 'sens1', target: 'core', strength: 0.8, active: true },
      { source: 'mem2', target: 'act1', strength: 0.4, active: false },
    ],
  });

  useEffect(() => {
    if (!svgRef.current) return;

    const width = 800;
    const height = 600;

    // Clear previous
    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height);

    // Add glow filter
    const defs = svg.append('defs');
    
    const filter = defs.append('filter')
      .attr('id', 'glow');
    
    filter.append('feGaussianBlur')
      .attr('stdDeviation', '3.5')
      .attr('result', 'coloredBlur');
    
    const feMerge = filter.append('feMerge');
    feMerge.append('feMergeNode')
      .attr('in', 'coloredBlur');
    feMerge.append('feMergeNode')
      .attr('in', 'SourceGraphic');

    // Create gradient for edges
    const gradient = defs.append('linearGradient')
      .attr('id', 'edge-gradient')
      .attr('gradientUnits', 'userSpaceOnUse');
    
    gradient.append('stop')
      .attr('offset', '0%')
      .attr('stop-color', '#00ffff')
      .attr('stop-opacity', 0.3);
    
    gradient.append('stop')
      .attr('offset', '100%')
      .attr('stop-color', '#ff00ff')
      .attr('stop-opacity', 0.3);

    // Force simulation
    const simulation = d3.forceSimulation(data.nodes as d3.SimulationNodeDatum[])
      .force('link', d3.forceLink(data.edges).id((d: any) => d.id).distance(120))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(50));

    // Create edge elements
    const link = svg.append('g')
      .selectAll('path')
      .data(data.edges)
      .enter().append('path')
      .attr('class', 'neural-edge')
      .attr('stroke', d => d.active ? 'url(#edge-gradient)' : '#1a1a2e')
      .attr('stroke-width', d => d.strength * 3)
      .attr('fill', 'none')
      .attr('opacity', d => d.active ? 0.8 : 0.3)
      .style('filter', d => d.active ? 'url(#glow)' : 'none');

    // Create node group
    const node = svg.append('g')
      .selectAll('g')
      .data(data.nodes)
      .enter().append('g')
      .attr('class', 'neural-node')
      .call(d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended) as any);

    // Add node circles
    node.append('circle')
      .attr('r', 25)
      .attr('fill', d => {
        const colors = {
          processor: '#00ffff',
          memory: '#ff00ff',
          sensor: '#00ff00',
          actuator: '#ffaa00'
        };
        return colors[d.type];
      })
      .attr('opacity', d => 0.3 + d.activity * 0.7)
      .style('filter', 'url(#glow)');

    // Add halo
    node.append('circle')
      .attr('class', 'halo')
      .attr('r', 30)
      .attr('fill', 'none')
      .attr('stroke', d => {
        const colors = {
          processor: '#00ffff',
          memory: '#ff00ff',
          sensor: '#00ff00',
          actuator: '#ffaa00'
        };
        return colors[d.type];
      })
      .attr('stroke-width', 2)
      .attr('opacity', d => d.activity * 0.5);

    // Add labels
    node.append('text')
      .text(d => d.label)
      .attr('text-anchor', 'middle')
      .attr('dy', 40)
      .attr('fill', '#ffffff')
      .attr('font-size', '12px')
      .attr('opacity', 0.8);

    // Animation for halos
    function animateHalos() {
      svg.selectAll('.halo')
        .transition()
        .duration(2000)
        .attr('r', (d: any) => 30 + d.activity * 10)
        .attr('opacity', (d: any) => d.activity * 0.2)
        .transition()
        .duration(2000)
        .attr('r', 30)
        .attr('opacity', (d: any) => d.activity * 0.5)
        .on('end', animateHalos);
    }
    animateHalos();

    // Hover effects
    node.on('mouseenter', function() {
      d3.select(this).select('circle')
        .transition()
        .duration(200)
        .attr('opacity', 1);
    }).on('mouseleave', function(event, d) {
      d3.select(this).select('circle')
        .transition()
        .duration(200)
        .attr('opacity', 0.3 + d.activity * 0.7);
    });

    // Update positions on tick
    simulation.on('tick', () => {
      link.attr('d', (d: any) => {
        const dx = d.target.x - d.source.x;
        const dy = d.target.y - d.source.y;
        const dr = Math.sqrt(dx * dx + dy * dy);
        return `M${d.source.x},${d.source.y}A${dr},${dr} 0 0,1 ${d.target.x},${d.target.y}`;
      });

      node.attr('transform', (d: any) => `translate(${d.x},${d.y})`);
    });

    // Drag functions
    function dragstarted(event: any, d: any) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event: any, d: any) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event: any, d: any) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    // Animate edges
    function animateEdges() {
      svg.selectAll('.neural-edge')
        .filter((d: any) => d.active)
        .transition()
        .duration(3000)
        .attr('stroke-dasharray', '10,10')
        .attr('stroke-dashoffset', 0)
        .transition()
        .duration(3000)
        .attr('stroke-dashoffset', -20)
        .on('end', animateEdges);
    }
    animateEdges();

  }, [data]);

  return (
    <div className="w-full h-full bg-gray-900 rounded-lg shadow-2xl p-4">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold text-cyan-400 glow-text">Neural Process Map</h2>
        <div className="space-x-2">
          <button
            onClick={() => {
              const newNode: NeuralNode = {
                id: `node-${Date.now()}`,
                label: 'New Process',
                type: 'processor',
                activity: Math.random()
              };
              setData(prev => ({
                ...prev,
                nodes: [...prev.nodes, newNode]
              }));
            }}
            className="px-4 py-2 bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-400 rounded-lg transition-all duration-200"
          >
            Add Node
          </button>
        </div>
      </div>
      <svg ref={svgRef} className="w-full h-full"></svg>
      <style jsx>{`
        .glow-text {
          text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
        }
      `}</style>
    </div>
  );
};

export default NeuralProcessMap; 