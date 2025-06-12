import React, { useRef, useEffect } from 'react';
const AwakenessMeter = ({ awakeness = 0.7 }) => {
  const canvasRef = useRef(null);
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let running = true;
    function draw() {
      if (!running) return;
      ctx.clearRect(0, 0, 48, 180);
      // Background
      ctx.save();
      ctx.globalAlpha = 0.18;
      ctx.fillStyle = '#64748b';
      ctx.fillRect(16, 16, 16, 148);
      ctx.restore();
      // Meter
      const h = Math.max(8, 148 * awakeness);
      ctx.save();
      ctx.globalAlpha = 0.8;
      ctx.fillStyle = awakeness > 0.7 ? '#14b8a6' : awakeness > 0.3 ? '#f59e0b' : '#ef4444';
      ctx.shadowColor = ctx.fillStyle;
      ctx.shadowBlur = 12;
      ctx.fillRect(16, 164 - h, 16, h);
      ctx.restore();
      // Label
      ctx.save();
      ctx.globalAlpha = 0.9;
      ctx.fillStyle = '#fff';
      ctx.font = 'bold 13px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('Awakeness', 24, 14);
      ctx.font = 'bold 16px Inter, sans-serif';
      ctx.fillText(`${Math.round(awakeness * 100)}%`, 24, 172);
      ctx.restore();
      requestAnimationFrame(draw);
    }
    draw();
    return () => { running = false; };
  }, [awakeness]);
  return (
    <div style={{ position: 'absolute', right: 12, top: 80, width: 48, height: 180, zIndex: 15, pointerEvents: 'none' }}>
      <canvas ref={canvasRef} width={48} height={180} style={{ width: 48, height: 180, background: 'none' }} />
    </div>
  );
};
export default AwakenessMeter; 