import React, { useRef, useEffect } from 'react';
import * as d3 from 'd3';
import { eventBus } from '../../utils/eventBus';

interface PatternEvent {
  type: string;
  value: number;
  timestamp: number;
}

export const TemporalPatterns: React.FC = () => {
  const svgRef = useRef<SVGSVGElement>(null);
  const dataRef = useRef<PatternEvent[]>([]);
  const particleCount = 12;

  useEffect(() => {
    const width = 320, height = 120;
    const svg = d3.select(svgRef.current as SVGSVGElement)
      .attr('width', width)
      .attr('height', height)
      .style('background', 'rgba(10,15,27,0.8)')
      .style('border-radius', '16px');

    // Particle state
    let particles: { t: number; color: string; }[] = Array.from({ length: particleCount }, (_, i) => ({ t: i / particleCount, color: '#00fff7' }));

    function render() {
      const now = Date.now();
      dataRef.current = dataRef.current.filter(d => now - d.timestamp < 20000);
      svg.selectAll('*').remove();
      // X: time, Y: value
      const x = d3.scaleLinear().domain([now - 20000, now]).range([24, width - 12]);
      const y = d3.scaleLinear().domain([0, 1]).range([height - 24, 16]);
      // Draw energy stream (animated line)
      const line = d3.line<PatternEvent>()
        .x(d => x(d.timestamp))
        .y(d => y(d.value))
        .curve(d3.curveBasis);
      svg.append('path')
        .datum(dataRef.current)
        .attr('fill', 'none')
        .attr('stroke', '#00fff7')
        .attr('stroke-width', 3)
        .attr('filter', 'url(#glow)')
        .attr('d', line as any);
      // Animate particles along the path
      const path = svg.select('path').node() as SVGPathElement | null;
      if (path && dataRef.current.length > 1) {
        const totalLength = path.getTotalLength();
        particles.forEach((p, i) => {
          p.t = (p.t + 0.008 + Math.random() * 0.002) % 1;
          const pos = path.getPointAtLength(p.t * totalLength);
          svg.append('circle')
            .attr('cx', pos.x)
            .attr('cy', pos.y)
            .attr('r', 7 - 3 * Math.abs(Math.sin(Date.now() * 0.002 + i)))
            .attr('fill', p.color)
            .attr('opacity', 0.7)
            .attr('filter', 'url(#glow)');
        });
      }
      // Neon glow filter
      svg.append('defs').append('filter').attr('id', 'glow')
        .html('<feGaussianBlur stdDeviation="6" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>');
    }
    let running = true;
    function animate() {
      if (!running) return;
      render();
      requestAnimationFrame(animate);
    }
    animate();
    // Event subscription
    const handler = (event: any) => {
      dataRef.current.push({
        type: event.type,
        value: event.payload.value || event.payload.intensity || 0.5,
        timestamp: event.payload.timestamp || Date.now(),
      });
    };
    eventBus.on('entropy:spike', handler, 'TemporalPatterns');
    eventBus.on('neural:pulse', handler, 'TemporalPatterns');
    return () => {
      running = false;
      eventBus.off('entropy:spike', handler);
      eventBus.off('neural:pulse', handler);
    };
  }, []);

  return <svg ref={svgRef} style={{ width: 320, height: 120, boxShadow: '0 0 24px #a78bfa', margin: 8 }} />;
};

export default TemporalPatterns; 