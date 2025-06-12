import React, { useRef, useEffect } from 'react';
function randomBetween(a, b) { return a + Math.random() * (b - a); }
const MemoryCrystallization = ({ memoryEvents = [] }) => {
  const canvasRef = useRef(null);
  const crystalsRef = useRef([]);
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let running = true;
    function spawnCrystal(event) {
      return {
        x: randomBetween(600, 760),
        y: randomBetween(480, 560),
        r: 0,
        maxR: randomBetween(16, 28),
        alpha: 0,
        phase: 0,
        text: event.label || 'memory',
        vx: randomBetween(-0.5, -1.2),
        vy: randomBetween(-0.5, -1.2),
      };
    }
    // Add new crystals for new memory events
    if (memoryEvents && memoryEvents.length) {
      memoryEvents.forEach((e, i) => {
        if (!crystalsRef.current.some(c => c.text === (e.label || 'memory'))) {
          crystalsRef.current.push(spawnCrystal(e));
        }
      });
    }
    function draw() {
      if (!running) return;
      ctx.clearRect(0, 0, 800, 600);
      // Animate and draw crystals
      crystalsRef.current.forEach((c, i) => {
        if (c.phase === 0) { // Growing
          c.r += 0.7;
          c.alpha += 0.04;
          if (c.r >= c.maxR) c.phase = 1;
        } else if (c.phase === 1) { // Moving
          c.x += c.vx;
          c.y += c.vy;
          c.alpha -= 0.01;
          if (c.alpha <= 0) c.phase = 2;
        }
        // Draw crystal (polygon/star)
        ctx.save();
        ctx.globalAlpha = Math.max(0, c.alpha);
        ctx.translate(c.x, c.y);
        ctx.rotate(i * 0.2);
        ctx.beginPath();
        for (let j = 0; j < 6; j++) {
          const angle = (j / 6) * Math.PI * 2;
          const r = c.r * (j % 2 === 0 ? 1 : 0.6);
          ctx.lineTo(Math.cos(angle) * r, Math.sin(angle) * r);
        }
        ctx.closePath();
        ctx.fillStyle = 'rgba(59,130,246,0.7)';
        ctx.shadowColor = '#3b82f6';
        ctx.shadowBlur = 16;
        ctx.fill();
        ctx.restore();
        ctx.save();
        ctx.globalAlpha = Math.max(0, c.alpha);
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 11px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(c.text, c.x, c.y + 4);
        ctx.restore();
      });
      // Remove finished crystals
      crystalsRef.current = crystalsRef.current.filter(c => c.phase < 2);
      requestAnimationFrame(draw);
    }
    draw();
    return () => { running = false; };
  }, [memoryEvents]);
  return (
    <div style={{ position: 'absolute', left: 0, top: 0, width: 800, height: 600, pointerEvents: 'none', zIndex: 10 }}>
      <canvas ref={canvasRef} width={800} height={600} style={{ width: 800, height: 600, background: 'none' }} />
    </div>
  );
};
export default MemoryCrystallization; 