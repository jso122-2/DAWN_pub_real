import React, { useRef, useEffect } from 'react';
function lerp(a, b, t) { return a + (b - a) * t; }
const EntropyTurbulence = ({ entropy = 0.5 }) => {
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
      const w = 800, h = 600;
      const intensity = typeof entropy === 'number' ? (entropy > 1 ? entropy / 100 : entropy) : 0.5;
      const turbulence = 12 + 48 * intensity;
      const imageData = ctx.createImageData(w, h);
      for (let y = 0; y < h; y += 2) {
        for (let x = 0; x < w; x += 2) {
          const n = Math.abs(Math.sin((x + frame * 0.7) * 0.01 + (y - frame * 0.5) * 0.012)) * intensity;
          const c = Math.floor(lerp(10, 60, n));
          const idx = (y * w + x) * 4;
          imageData.data[idx] = c;
          imageData.data[idx + 1] = c + 10;
          imageData.data[idx + 2] = c + 20;
          imageData.data[idx + 3] = Math.floor(lerp(18, 38, n));
        }
      }
      ctx.putImageData(imageData, 0, 0);
      requestAnimationFrame(draw);
    }
    draw();
    return () => { running = false; };
  }, [entropy]);
  return (
    <div style={{ position: 'absolute', left: 0, top: 0, width: 800, height: 600, zIndex: 1, pointerEvents: 'none' }}>
      <canvas ref={canvasRef} width={800} height={600} style={{ width: 800, height: 600, background: 'none' }} />
    </div>
  );
};
export default EntropyTurbulence; 