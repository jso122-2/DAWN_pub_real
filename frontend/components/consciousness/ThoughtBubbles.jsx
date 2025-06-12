import React, { useRef, useEffect } from 'react';
const colors = ['#a855f7', '#22c55e', '#f59e0b', '#3b82f6', '#ff6b9d', '#fbbf24'];
function randomBetween(a, b) { return a + Math.random() * (b - a); }
const ThoughtBubbles = ({ thoughts = [] }) => {
  const canvasRef = useRef(null);
  const bubblesRef = useRef([]);
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let running = true;
    function spawnBubble(thought) {
      return {
        x: randomBetween(40, 720),
        y: randomBetween(300, 500),
        r: randomBetween(18, 32),
        color: colors[Math.floor(Math.random() * colors.length)],
        alpha: 0,
        life: 0,
        maxLife: randomBetween(120, 220),
        text: thought.label || thought.type || 'thought',
        vy: randomBetween(-0.4, -1.2),
      };
    }
    // Add new bubbles for new thoughts
    if (thoughts && thoughts.length) {
      thoughts.forEach((t, i) => {
        if (!bubblesRef.current.some(b => b.text === (t.label || t.type))) {
          bubblesRef.current.push(spawnBubble(t));
        }
      });
    }
    function draw() {
      if (!running) return;
      ctx.clearRect(0, 0, 800, 600);
      // Animate and draw bubbles
      bubblesRef.current.forEach((b, i) => {
        b.life++;
        if (b.life < 30) b.alpha = b.life / 30;
        else if (b.life > b.maxLife - 30) b.alpha = (b.maxLife - b.life) / 30;
        else b.alpha = 1;
        b.y += b.vy;
        ctx.save();
        ctx.globalAlpha = 0.18 * b.alpha;
        ctx.beginPath();
        ctx.arc(b.x, b.y, b.r + 8, 0, Math.PI * 2);
        ctx.fillStyle = b.color;
        ctx.shadowColor = b.color;
        ctx.shadowBlur = 24;
        ctx.fill();
        ctx.restore();
        ctx.save();
        ctx.globalAlpha = 0.7 * b.alpha;
        ctx.beginPath();
        ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
        ctx.fillStyle = b.color;
        ctx.shadowColor = b.color;
        ctx.shadowBlur = 8;
        ctx.fill();
        ctx.restore();
        ctx.save();
        ctx.globalAlpha = b.alpha;
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 13px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(b.text, b.x, b.y + 4);
        ctx.restore();
      });
      // Remove dead bubbles
      bubblesRef.current = bubblesRef.current.filter(b => b.life < b.maxLife);
      requestAnimationFrame(draw);
    }
    draw();
    return () => { running = false; };
  }, [thoughts]);
  return (
    <div style={{ position: 'absolute', left: 0, top: 0, width: 800, height: 600, pointerEvents: 'none', zIndex: 11 }}>
      <canvas ref={canvasRef} width={800} height={600} style={{ width: 800, height: 600, background: 'none' }} />
    </div>
  );
};
export default ThoughtBubbles; 