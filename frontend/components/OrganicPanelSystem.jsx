import React, { useRef, useEffect, useState } from 'react';

/**
 * OrganicPanelSystem Props
 * @param {Array} panels - Array of panel objects: { id, label, x, y, color, glow, data }
 * @param {Array} relationships - Array of relationships: { from, to, strength }
 * @param {Function} renderPanel - Optional function to render custom panel content
 */

// Utility: Generate random panels and relationships for demo
const generatePanels = (count = 6) => {
  const panels = [];
  for (let i = 0; i < count; i++) {
    panels.push({
      id: i,
      label: `Panel ${i + 1}`,
      x: 300 + Math.random() * 400,
      y: 200 + Math.random() * 300,
      vx: 0,
      vy: 0,
      color: `hsl(${Math.random() * 360}, 80%, 60%)`,
      glow: `hsl(${Math.random() * 360}, 100%, 80%)`,
      data: { value: Math.random() }
    });
  }
  // Random relationships
  const relationships = [];
  for (let i = 0; i < count; i++) {
    for (let j = i + 1; j < count; j++) {
      if (Math.random() < 0.5) {
        relationships.push({
          from: i,
          to: j,
          strength: 0.5 + Math.random() * 0.5
        });
      }
    }
  }
  return { panels, relationships };
};

// Ripple effect state
const useRipples = () => {
  const [ripples, setRipples] = useState([]);
  const addRipple = (x, y, color) => {
    setRipples(ripples => [...ripples, { x, y, color, t: 0 }]);
  };
  // Animate and clean up
  useEffect(() => {
    if (ripples.length === 0) return;
    const id = setInterval(() => {
      setRipples(ripples => ripples.filter(r => r.t < 1).map(r => ({ ...r, t: r.t + 0.04 })));
    }, 16);
    return () => clearInterval(id);
  }, [ripples]);
  return [ripples, addRipple];
};

const PANEL_RADIUS = 60;
const DRIFT_STRENGTH = 0.3;
const ATTRACTION = 0.04;
const REPULSION = 12000;
const CURSOR_MAGNET_RADIUS = 120;
const CURSOR_MAGNET_STRENGTH = 0.12;

export default function OrganicPanelSystem({ panels: propPanels, relationships: propRelationships, renderPanel }) {
  const canvasRef = useRef(null);
  const [dimensions, setDimensions] = useState({ width: 1200, height: 700 });
  // Use props if provided, else demo
  const [{ panels, relationships }] = useState(() => {
    if (propPanels && propRelationships) {
      return { panels: propPanels, relationships: propRelationships };
    }
    return generatePanels(6);
  });
  const [panelStates, setPanelStates] = useState(panels);
  const [dragged, setDragged] = useState(null);
  const [cursor, setCursor] = useState({ x: -1000, y: -1000 });
  const [ripples, addRipple] = useRipples();

  // Handle window resize
  useEffect(() => {
    const handleResize = () => {
      setDimensions({ width: window.innerWidth, height: window.innerHeight });
    };
    window.addEventListener('resize', handleResize);
    handleResize();
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Animation loop: drift, attract/repel, cursor magnet
  useEffect(() => {
    let running = true;
    const animate = () => {
      setPanelStates(prev => {
        return prev.map((panel, i) => {
          let { x, y, vx, vy } = panel;
          // Subtle random drift
          vx += (Math.random() - 0.5) * DRIFT_STRENGTH;
          vy += (Math.random() - 0.5) * DRIFT_STRENGTH;
          // Attraction/repulsion
          relationships.forEach(rel => {
            if (rel.from === i || rel.to === i) {
              const otherIdx = rel.from === i ? rel.to : rel.from;
              const other = prev[otherIdx];
              const dx = other.x - x;
              const dy = other.y - y;
              const dist = Math.sqrt(dx * dx + dy * dy) || 1;
              // Attraction
              vx += (dx / dist) * rel.strength * ATTRACTION;
              vy += (dy / dist) * rel.strength * ATTRACTION;
              // Repulsion (strong if too close)
              if (dist < PANEL_RADIUS * 2.2) {
                vx -= (dx / dist) * (REPULSION / (dist * dist));
                vy -= (dy / dist) * (REPULSION / (dist * dist));
              }
            }
          });
          // Magnetic cursor effect
          const dx = cursor.x - x;
          const dy = cursor.y - y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < CURSOR_MAGNET_RADIUS) {
            vx += (dx / dist) * CURSOR_MAGNET_STRENGTH * (1 - dist / CURSOR_MAGNET_RADIUS);
            vy += (dy / dist) * CURSOR_MAGNET_STRENGTH * (1 - dist / CURSOR_MAGNET_RADIUS);
          }
          // Drag override
          if (dragged && dragged.id === panel.id) {
            x = dragged.x;
            y = dragged.y;
            vx = 0;
            vy = 0;
          } else {
            // Integrate velocity
            x += vx;
            y += vy;
            // Damping
            vx *= 0.92;
            vy *= 0.92;
            // Stay in bounds
            x = Math.max(PANEL_RADIUS, Math.min(dimensions.width - PANEL_RADIUS, x));
            y = Math.max(PANEL_RADIUS, Math.min(dimensions.height - PANEL_RADIUS, y));
          }
          return { ...panel, x, y, vx, vy };
        });
      });
      if (running) requestAnimationFrame(animate);
    };
    animate();
    return () => { running = false; };
  }, [relationships, cursor, dragged, dimensions]);

  // Canvas draw: panels, glows, energy lines, ripples
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, dimensions.width, dimensions.height);
    // Draw energy lines (animated, flowing)
    relationships.forEach(rel => {
      const a = panelStates[rel.from];
      const b = panelStates[rel.to];
      if (!a || !b) return;
      // Flowing Bezier
      const mx = (a.x + b.x) / 2 + Math.sin(Date.now() * 0.001 + rel.from) * 30;
      const my = (a.y + b.y) / 2 + Math.cos(Date.now() * 0.001 + rel.to) * 30;
      const grad = ctx.createLinearGradient(a.x, a.y, b.x, b.y);
      grad.addColorStop(0, a.glow);
      grad.addColorStop(1, b.glow);
      ctx.save();
      ctx.strokeStyle = grad;
      ctx.shadowColor = a.glow;
      ctx.shadowBlur = 18;
      ctx.lineWidth = 3 + Math.sin(Date.now() * 0.002 + rel.strength) * 1.5;
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.bezierCurveTo(a.x, a.y, mx, my, b.x, b.y);
      ctx.stroke();
      ctx.restore();
    });
    // Draw ripples (expanding, fading circles)
    ripples.forEach(r => {
      ctx.save();
      ctx.globalAlpha = 1 - r.t;
      const rad = 20 + r.t * 60;
      const grad = ctx.createRadialGradient(r.x, r.y, 0, r.x, r.y, rad);
      grad.addColorStop(0, r.color);
      grad.addColorStop(1, 'rgba(255,255,255,0)');
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(r.x, r.y, rad, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    });
    // Draw panels (glow first, then core)
    panelStates.forEach(panel => {
      ctx.save();
      // Glow
      const grad = ctx.createRadialGradient(panel.x, panel.y, PANEL_RADIUS * 0.7, panel.x, panel.y, PANEL_RADIUS * 1.2);
      grad.addColorStop(0, panel.glow);
      grad.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.globalAlpha = 0.7;
      ctx.beginPath();
      ctx.arc(panel.x, panel.y, PANEL_RADIUS * 1.2, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();
      ctx.restore();
    });
    panelStates.forEach(panel => {
      ctx.save();
      ctx.beginPath();
      ctx.arc(panel.x, panel.y, PANEL_RADIUS, 0, Math.PI * 2);
      ctx.fillStyle = panel.color;
      ctx.shadowColor = panel.glow;
      ctx.shadowBlur = 24;
      ctx.fill();
      ctx.restore();
      // Label
      ctx.save();
      ctx.font = 'bold 18px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillStyle = 'rgba(255,255,255,0.92)';
      ctx.shadowColor = panel.glow;
      ctx.shadowBlur = 8;
      ctx.fillText(panel.label, panel.x, panel.y);
      ctx.restore();
    });
  }, [panelStates, relationships, ripples, dimensions]);

  // Mouse events for drag, ripple, and cursor magnet
  const handleMouseMove = e => {
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    setCursor({ x, y });
    if (dragged) {
      setDragged({ ...dragged, x, y });
    }
  };
  const handleMouseDown = e => {
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    // Find panel under cursor
    for (let panel of panelStates) {
      const dx = panel.x - x;
      const dy = panel.y - y;
      if (dx * dx + dy * dy < PANEL_RADIUS * PANEL_RADIUS) {
        setDragged({ id: panel.id, x, y });
        addRipple(x, y, panel.glow);
        break;
      }
    }
  };
  const handleMouseUp = e => {
    setDragged(null);
  };
  const handleClick = e => {
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    // Ripple on click
    addRipple(x, y, 'rgba(255,255,255,0.7)');
  };

  // Draw panel content (HTML overlay, supports custom content)
  const panelContent = panelStates.map(panel => (
    <div
      key={panel.id}
      style={{
        position: 'absolute',
        left: panel.x - PANEL_RADIUS,
        top: panel.y - PANEL_RADIUS,
        width: PANEL_RADIUS * 2,
        height: PANEL_RADIUS * 2,
        pointerEvents: 'none',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 10,
      }}
    >
      {renderPanel ? renderPanel(panel) : null}
    </div>
  ));

  return (
    <div style={{ width: '100vw', height: '100vh', overflow: 'hidden', position: 'fixed', left: 0, top: 0, zIndex: 100 }}>
      {/* Canvas for all organic visuals */}
      <canvas
        ref={canvasRef}
        width={dimensions.width}
        height={dimensions.height}
        style={{ width: '100vw', height: '100vh', display: 'block', cursor: 'pointer', position: 'absolute', left: 0, top: 0 }}
        onMouseMove={handleMouseMove}
        onMouseDown={handleMouseDown}
        onMouseUp={handleMouseUp}
        onClick={handleClick}
      />
      {/* Panel content overlays (HTML, pointerEvents: none) */}
      <div style={{ position: 'absolute', left: 0, top: 0, width: '100vw', height: '100vh', pointerEvents: 'none' }}>
        {panelContent}
      </div>
    </div>
  );
} 