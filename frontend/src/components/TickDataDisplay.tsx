import { useEffect, useState, useRef } from 'react';

interface TickData {
  tick_number: number;
  scup: number;
  entropy: number;
  mood: 'calm' | 'energetic' | 'chaotic';
}

interface SCUPDataPoint {
  tick: number;
  value: number;
}

const TickDataDisplay = () => {
  const [data, setData] = useState<TickData>({
    tick_number: 0,
    scup: 0,
    entropy: 0,
    mood: 'calm'
  });
  const [scupHistory, setScupHistory] = useState<SCUPDataPoint[]>([]);
  const [isPulsing, setIsPulsing] = useState(false);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'disconnected' | 'error'>('disconnected');
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');
    
    ws.onopen = () => {
      console.log('WebSocket connected');
      setConnectionStatus('connected');
    };
    
    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setConnectionStatus('disconnected');
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setConnectionStatus('error');
    };
    
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'tick') {
          setData({
            tick_number: data.tick_number,
            scup: data.scup,
            entropy: data.entropy,
            mood: data.mood
          });
          setLastUpdate(new Date());
          
          // Add to SCUP history
          setScupHistory(prev => {
            const newHistory = [...prev, { tick: data.tick_number, value: data.scup }];
            return newHistory.slice(-50); // Keep last 50 points
          });

          // Trigger pulse animation
          setIsPulsing(true);
          setTimeout(() => setIsPulsing(false), 500);
        }
      } catch (error) {
        console.error('Failed to parse tick data:', error);
      }
    };
    
    return () => {
      ws.close();
    };
  }, []);

  // Draw SCUP graph
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Set up graph
    const padding = 20;
    const width = canvas.width - padding * 2;
    const height = canvas.height - padding * 2;

    // Find min/max SCUP values
    const values = scupHistory.map(point => point.value);
    const min = Math.min(...values, 0);
    const max = Math.max(...values, 1);

    // Draw axes
    ctx.strokeStyle = '#4b5563';
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, canvas.height - padding);
    ctx.lineTo(canvas.width - padding, canvas.height - padding);
    ctx.stroke();

    // Draw SCUP line
    if (scupHistory.length > 0) {
      ctx.strokeStyle = '#00ff88';
      ctx.lineWidth = 2;
      ctx.beginPath();

      scupHistory.forEach((point, index) => {
        const x = padding + (index / (scupHistory.length - 1)) * width;
        const y = canvas.height - padding - ((point.value - min) / (max - min)) * height;
        
        if (index === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });

      ctx.stroke();
    }
  }, [scupHistory]);

  const getMoodColor = (mood: string) => {
    switch (mood) {
      case 'calm': return '#3b82f6'; // blue
      case 'energetic': return '#f97316'; // orange
      case 'chaotic': return '#ef4444'; // red
      default: return '#4b5563'; // gray
    }
  };

  const formatNumber = (num: number) => {
    return num.toFixed(3);
  };

  return (
    <div
      style={{
        background: 'rgba(255, 255, 255, 0.1)',
        backdropFilter: 'blur(8px)',
        WebkitBackdropFilter: 'blur(8px)',
        borderRadius: '1rem',
        border: '1px solid rgba(255, 255, 255, 0.2)',
        padding: '1.5rem',
        margin: '1rem',
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        transition: 'all 0.3s ease',
        borderColor: getMoodColor(data.mood)
      }}
    >
      <h3 style={{ 
        margin: '0 0 1rem 0',
        color: '#00ff88',
        fontSize: '1.25rem',
        fontFamily: 'var(--font-mono)'
      }}>
        Live Tick Data
      </h3>
      
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(2, 1fr)',
        gap: '1rem',
        marginBottom: '1rem'
      }}>
        <div>
          <div style={{ color: '#9ca3af', fontSize: '0.875rem' }}>Tick</div>
          <div style={{ 
            color: '#ffffff',
            fontSize: '1.5rem',
            fontFamily: 'var(--font-mono)',
            transition: 'all 0.3s ease',
            animation: isPulsing ? 'pulse 0.5s ease' : 'none'
          }}>
            {data.tick_number}
          </div>
        </div>

        <div>
          <div style={{ color: '#9ca3af', fontSize: '0.875rem' }}>SCUP</div>
          <div style={{ 
            color: '#ffffff',
            fontSize: '1.5rem',
            fontFamily: 'var(--font-mono)',
            transition: 'all 0.3s ease'
          }}>
            {formatNumber(data.scup)}
          </div>
        </div>

        <div>
          <div style={{ color: '#9ca3af', fontSize: '0.875rem' }}>Entropy</div>
          <div style={{ 
            color: '#ffffff',
            fontSize: '1.5rem',
            fontFamily: 'var(--font-mono)',
            transition: 'all 0.3s ease'
          }}>
            {formatNumber(data.entropy)}
          </div>
        </div>

        <div>
          <div style={{ color: '#9ca3af', fontSize: '0.875rem' }}>Mood</div>
          <div style={{ 
            color: getMoodColor(data.mood),
            fontSize: '1.5rem',
            fontFamily: 'var(--font-mono)',
            transition: 'all 0.3s ease'
          }}>
            {data.mood}
          </div>
        </div>
      </div>

      <div style={{ marginTop: '1rem' }}>
        <div style={{ color: '#9ca3af', fontSize: '0.875rem', marginBottom: '0.5rem' }}>
          SCUP History (Last 50 Ticks)
        </div>
        <canvas
          ref={canvasRef}
          width={400}
          height={200}
          style={{
            width: '100%',
            height: '200px',
            background: 'rgba(0, 0, 0, 0.2)',
            borderRadius: '0.5rem'
          }}
        />
      </div>

      <style>
        {`
          @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
          }
        `}
      </style>
    </div>
  );
};

export default TickDataDisplay; 