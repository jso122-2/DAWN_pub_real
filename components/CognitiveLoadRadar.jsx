import React, { useState, useEffect, useRef } from 'react';
import eventBus, { emitPrediction } from './eventBus';

const CognitiveLoadRadar = () => {
  const canvasRef = useRef(null);
  const animationRef = useRef(null);

  const [metrics, setMetrics] = useState({
    scup: { current: 0.440, history: [0.440] },
    entropy: { current: 0.698, history: [0.698] },
    heat: { current: 0.364, history: [0.364] },
    mood: { current: 0.750, history: [0.750] },
    focus: { current: 0.820, history: [0.820] },
    stress: { current: 0.290, history: [0.290] }
  });

  const [thresholds] = useState({
    critical: 0.85,
    warning: 0.65,
    normal: 0.35
  });

  const labels = ['SCUP', 'ENTROPY', 'HEAT', 'MOOD', 'FOCUS', 'STRESS'];
  const colors = {
    scup: '#ec4899',
    entropy: '#3b82f6',
    heat: '#f59e0b',
    mood: '#8b5cf6',
    focus: '#10b981',
    stress: '#ef4444'
  };

  // Draw radar chart
  const drawRadar = (ctx, width, height) => {
    const centerX = width / 2;
    const centerY = height / 2;
    const maxRadius = Math.min(width, height) * 0.4;
    const numPoints = labels.length;
    const angleStep = (Math.PI * 2) / numPoints;

    // Clear canvas
    ctx.fillStyle = '#0a0f1b';
    ctx.fillRect(0, 0, width, height);

    // Draw threshold rings
    const drawRing = (radius, color, label) => {
      ctx.strokeStyle = color;
      ctx.lineWidth = 1;
      ctx.setLineDash([5, 5]);
      ctx.beginPath();

      for (let i = 0; i <= numPoints; i++) {
        const angle = i * angleStep - Math.PI / 2;
        const x = centerX + Math.cos(angle) * radius;
        const y = centerY + Math.sin(angle) * radius;

        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      }

      ctx.closePath();
      ctx.stroke();
      ctx.setLineDash([]);

      // Label
      ctx.fillStyle = color;
      ctx.font = '10px monospace';
      ctx.fillText(label, centerX + radius + 5, centerY);
    };

    drawRing(maxRadius * thresholds.critical, '#ef4444', 'Critical');
    drawRing(maxRadius * thresholds.warning, '#f59e0b', 'Warning');
    drawRing(maxRadius * thresholds.normal, '#10b981', 'Normal');

    // Draw axes
    ctx.strokeStyle = '#374151';
    ctx.lineWidth = 1;

    for (let i = 0; i < numPoints; i++) {
      const angle = i * angleStep - Math.PI / 2;
      const x = centerX + Math.cos(angle) * maxRadius;
      const y = centerY + Math.sin(angle) * maxRadius;

      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(x, y);
      ctx.stroke();

      // Draw labels
      const labelX = centerX + Math.cos(angle) * (maxRadius + 20);
      const labelY = centerY + Math.sin(angle) * (maxRadius + 20);

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 12px monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(labels[i], labelX, labelY);
    }

    // Draw historical traces (ghost lines)
    const metricKeys = Object.keys(metrics);
    metricKeys.forEach((key, idx) => {
      const history = metrics[key].history.slice(-5);

      history.forEach((value, histIdx) => {
        ctx.strokeStyle = `${colors[key]}${Math.floor(30 + histIdx * 10).toString(16)}`;
        ctx.lineWidth = 1;
        ctx.beginPath();

        for (let i = 0; i <= numPoints; i++) {
          const angle = i * angleStep - Math.PI / 2;
          const metricIdx = i % numPoints;
          const metricKey = metricKeys[metricIdx];
          const metricValue = metricIdx === idx ? value : metrics[metricKey].current;
          const radius = metricValue * maxRadius;

          const x = centerX + Math.cos(angle) * radius;
          const y = centerY + Math.sin(angle) * radius;

          if (i === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        }

        ctx.closePath();
        ctx.stroke();
      });
    });

    // Draw current values
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2;
    ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
    ctx.beginPath();

    metricKeys.forEach((key, i) => {
      const angle = i * angleStep - Math.PI / 2;
      const value = metrics[key].current;
      const radius = value * maxRadius;

      const x = centerX + Math.cos(angle) * radius;
      const y = centerY + Math.sin(angle) * radius;

      if (i === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }

      // Draw point
      ctx.save();
      ctx.fillStyle = colors[key];
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI * 2);
      ctx.fill();

      // Draw value
      ctx.fillStyle = '#ffffff';
      ctx.font = '10px monospace';
      ctx.fillText(value.toFixed(3), x + 10, y - 10);
      ctx.restore();
    });

    ctx.closePath();
    ctx.stroke();
    ctx.fill();

    // Draw center point
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.arc(centerX, centerY, 3, 0, Math.PI * 2);
    ctx.fill();
  };

  // Animation loop
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    const animate = () => {
      drawRadar(ctx, width, height);
      animationRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [metrics]);

  // Update metrics
  useEffect(() => {
    const prevStatus = { current: null };
    const interval = setInterval(() => {
      setMetrics(prev => {
        const newMetrics = {};
        Object.keys(prev).forEach(key => {
          const currentValue = prev[key].current;
          const change = (Math.random() - 0.5) * 0.1;
          const newValue = Math.min(1, Math.max(0, currentValue + change));
          newMetrics[key] = {
            current: newValue,
            history: [...prev[key].history.slice(-10), newValue]
          };
        });
        // Check for threshold crossing
        const values = Object.values(newMetrics).map(m => m.current);
        const average = values.reduce((a, b) => a + b, 0) / values.length;
        let status = 'Optimal';
        if (average > thresholds.critical) status = 'Critical';
        else if (average > thresholds.warning) status = 'Warning';
        else if (average > thresholds.normal) status = 'Normal';
        if (status !== prevStatus.current && (status === 'Critical' || status === 'Warning')) {
          prevStatus.current = status;
          // Emit to event bus
          eventBus.dispatchEvent(new CustomEvent('threshold-alert', { detail: { status, average, timestamp: new Date() } }));
        }
        return newMetrics;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [thresholds]);

  // Predictive analysis for cognitive load
  useEffect(() => {
    const predictionInterval = setInterval(() => {
      const values = Object.values(metrics).map(m => m.current);
      const average = values.reduce((a, b) => a + b, 0) / values.length;
      // Simple trend: if average is rising and near threshold, predict crossing
      if (average > thresholds.warning - 0.05 && average < thresholds.critical) {
        emitPrediction({
          message: `Cognitive load likely to reach critical in next 60s (currently ${(average * 100).toFixed(1)}%)`,
          probability: 70,
          severity: 'high',
          type: 'cognitive-load'
        });
      } else if (average > thresholds.normal - 0.05 && average < thresholds.warning) {
        emitPrediction({
          message: `Cognitive load likely to reach warning in next 60s (currently ${(average * 100).toFixed(1)}%)`,
          probability: 60,
          severity: 'medium',
          type: 'cognitive-load'
        });
      }
    }, 12000);
    return () => clearInterval(predictionInterval);
  }, [metrics, thresholds]);

  // Calculate overall cognitive load
  const calculateOverallLoad = () => {
    const values = Object.values(metrics).map(m => m.current);
    const average = values.reduce((a, b) => a + b, 0) / values.length;
    return average;
  };

  const overallLoad = calculateOverallLoad();
  const loadStatus = overallLoad > thresholds.critical ? 'Critical' :
                    overallLoad > thresholds.warning ? 'Warning' :
                    overallLoad > thresholds.normal ? 'Normal' : 'Optimal';

  return (
    <div style={{ background: '#0a0f1b', border: '1px solid #374151' }} className="rounded-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-white">Cognitive Load Analysis</h3>
        <div className="flex items-center space-x-4">
          <div className="text-sm">
            <span className="text-gray-400">Overall Load: </span>
            <span className={`font-bold ${
              loadStatus === 'Critical' ? 'text-red-500' :
              loadStatus === 'Warning' ? 'text-yellow-500' :
              loadStatus === 'Normal' ? 'text-green-500' : 'text-blue-500'
            }`}>
              {(overallLoad * 100).toFixed(1)}% ({loadStatus})
            </span>
          </div>
        </div>
      </div>

      <canvas
        ref={canvasRef}
        width={600}
        height={400}
        style={{ width: '100%', borderRadius: '0.5rem', background: '#0a0f1b' }}
      />

      <div className="mt-4 grid grid-cols-3 gap-4">
        <div style={{ background: '#111827' }} className="rounded p-3">
          <p className="text-xs text-gray-400 mb-1">Peak Metric</p>
          <p className="text-sm font-bold text-white">
            {Object.entries(metrics).reduce((a, b) => a[1].current > b[1].current ? a : b)[0].toUpperCase()}
          </p>
        </div>
        <div style={{ background: '#111827' }} className="rounded p-3">
          <p className="text-xs text-gray-400 mb-1">Volatility</p>
          <p className="text-sm font-bold text-white">±12.3%</p>
        </div>
        <div style={{ background: '#111827' }} className="rounded p-3">
          <p className="text-xs text-gray-400 mb-1">Trend</p>
          <p className="text-sm font-bold text-green-400">↑ Stabilizing</p>
        </div>
      </div>
    </div>
  );
};

export default CognitiveLoadRadar; 