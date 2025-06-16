import { useEffect, useState } from 'react';

const ViteHealthCheck = () => {
  const [isOffline, setIsOffline] = useState(false);

  useEffect(() => {
    const checkViteHealth = async () => {
      try {
        // Try to fetch from the Vite dev server
        const response = await fetch('/@vite/client');
        if (!response.ok) {
          setIsOffline(true);
        } else {
          setIsOffline(false);
        }
      } catch (error) {
        setIsOffline(true);
      }
    };

    // Check immediately and then every 5 seconds
    checkViteHealth();
    const interval = setInterval(checkViteHealth, 5000);

    return () => clearInterval(interval);
  }, []);

  if (!isOffline) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      zIndex: 9999,
      background: 'rgba(0, 0, 0, 0.5)',
      backdropFilter: 'blur(8px)',
      WebkitBackdropFilter: 'blur(8px)'
    }}>
      <div style={{
        background: 'rgba(255, 255, 255, 0.1)',
        padding: '2rem 3rem',
        borderRadius: '1rem',
        border: '1px solid rgba(255, 255, 255, 0.2)',
        boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
        textAlign: 'center',
        animation: 'pulse 2s infinite'
      }}>
        <h2 style={{
          color: '#ff4444',
          margin: '0 0 1rem 0',
          fontSize: '1.5rem'
        }}>Dev Server Offline</h2>
        <p style={{
          color: '#ffffff',
          margin: 0,
          fontSize: '1.1rem',
          fontFamily: 'monospace'
        }}>Please restart: npm run dev</p>
      </div>
    </div>
  );
};

export default ViteHealthCheck; 