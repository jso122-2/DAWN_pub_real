import { useEffect, useRef } from "react";

/**
 * useTickStream - React hook to subscribe to the DAWN tick WebSocket stream.
 * @param {function} onTick - Callback to receive each tick's state (parsed JSON).
 * @param {string} [wsUrl] - Optional override for the WebSocket URL.
 */
export function useTickStream(onTick, wsUrl) {
  const wsRef = useRef(null);

  useEffect(() => {
    // Default to local backend if not provided
    const url = wsUrl || `ws://${window.location.hostname}:8000/ws`;
    const ws = new window.WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => {
      // Optionally: console.log("Tick stream connected");
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onTick(data);
      } catch (e) {
        // Optionally: console.error("Tick stream parse error", e);
      }
    };

    ws.onerror = (err) => {
      // Optionally: console.error("Tick stream error", err);
    };

    ws.onclose = () => {
      // Optionally: console.log("Tick stream closed");
    };

    return () => {
      ws.close();
    };
  }, [onTick, wsUrl]);
} 