import React, { useRef, useEffect } from 'react';
const CoherenceWave = ({ coherence = 0.7 }) => {
  const canvasRef = useRef(null);
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let frame = 0;
    let running = true;
    function draw() {
      if (!running) return;
      frame++;
      ctx.clearRect(0, 0, 800, 120);
      const amp = 18 + 32 * coherence;
      const color = coherence > 0.7 ? '#14b8a6' : coherence > 0.3 ? '#f59e0b' : '#ef4444';
      ctx.save();
      ctx.globalAlpha = 0.18 + 0.18 * coherence;
      ctx.lineWidth = 6;
      ctx.strokeStyle = color;
      ctx.shadowColor = color;
      ctx.shadowBlur = 16;
      ctx.beginPath();
      for (let x = 0; x <= 800; x += 4) {
        const y = 60 + Math.sin((x * 0.012) + frame * 0.04) * amp * Math.sin(frame * 0.01 + x * 0.002);
        ctx.lineTo(x, y);
      }
      ctx.stroke();
      ctx.restore();
      requestAnimationFrame(draw);
    }
    draw();
    return () => { running = false; };
  }, [coherence]);
  return (
    <div style={{ position: 'absolute', left: 0, top: 0, width: 800, height: 120, zIndex: 2, pointerEvents: 'none' }}>
      <canvas ref={canvasRef} width={800} height={120} style={{ width: 800, height: 120, background: 'none' }} />
    </div>
  );
};
export default CoherenceWave; 