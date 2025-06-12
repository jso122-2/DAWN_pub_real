import React, { useRef, useEffect } from 'react';
const HeartbeatPulse = ({ tickRate = 1.0 }) => {
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
      ctx.clearRect(0, 0, 160, 160);
      const center = 80;
      const baseRadius = 38;
      const pulse = 1 + Math.sin(Date.now() * 0.002 * tickRate) * 0.12;
      // Outer glow
      ctx.save();
      ctx.globalAlpha = 0.5;
      ctx.beginPath();
      ctx.arc(center, center, baseRadius * pulse + 10, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(0,255,247,0.18)';
      ctx.shadowColor = '#00fff7';
      ctx.shadowBlur = 32;
      ctx.fill();
      ctx.restore();
      // Main pulse ring
      ctx.save();
      ctx.beginPath();
      ctx.arc(center, center, baseRadius * pulse, 0, Math.PI * 2);
      ctx.strokeStyle = '#00fff7';
      ctx.lineWidth = 6;
      ctx.shadowColor = '#00fff7';
      ctx.shadowBlur = 16;
      ctx.stroke();
      ctx.restore();
      // Core
      ctx.save();
      ctx.beginPath();
      ctx.arc(center, center, 18 + 2 * Math.sin(Date.now() * 0.003 * tickRate), 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(0,255,247,0.7)';
      ctx.shadowColor = '#00fff7';
      ctx.shadowBlur = 12;
      ctx.fill();
      ctx.restore();
      requestAnimationFrame(draw);
    }
    draw();
    return () => { running = false; };
  }, [tickRate]);
  return (
    <div style={{ position: 'absolute', left: '50%', top: '50%', transform: 'translate(-50%,-50%)', zIndex: 12, pointerEvents: 'none' }}>
      <canvas ref={canvasRef} width={160} height={160} style={{ width: 160, height: 160, background: 'none' }} />
    </div>
  );
};
export default HeartbeatPulse; 