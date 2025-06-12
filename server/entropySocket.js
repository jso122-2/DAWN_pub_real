const { Server } = require('socket.io');
const si = require('systeminformation');

function calculateSystemEntropy({ cpuUsage, memoryUsage, processCount }) {
  // Simple entropy calculation: average of normalized metrics
  return Math.min(100, (
    (cpuUsage / 100) * 0.4 +
    (memoryUsage / 100) * 0.4 +
    (processCount / 300) * 0.2
  ) * 100);
}

function initEntropySocket(httpServer) {
  const io = new Server(httpServer, {
    cors: { origin: "http://localhost:5173" }
  });
  
  io.on('connection', (socket) => {
    console.log('Entropy monitor connected');
    
    const interval = setInterval(async () => {
      // Get system metrics
      const cpu = await si.currentLoad();
      const mem = await si.mem();
      const processes = await si.processes();
      
      // Calculate entropy
      const entropy = calculateSystemEntropy({
        cpuUsage: cpu.currentLoad,
        memoryUsage: (mem.used / mem.total) * 100,
        processCount: processes.all
      });
      
      socket.emit('entropy-update', { 
        entropy,
        coherence: 100 - entropy,
        timestamp: Date.now()
      });
      
      // Send top processes
      const topProcesses = processes.list
        .sort((a, b) => b.cpu - a.cpu)
        .slice(0, 5)
        .map(p => ({
          pid: p.pid,
          name: p.name,
          cpu: p.cpu,
          memory: p.memVsz / 1024 / 1024,
          status: p.state === 'running' ? 'active' : 'idle',
          entropy: (p.cpu + (p.memVsz / mem.total * 100)) / 2
        }));
      
      socket.emit('subprocess-update', { processes: topProcesses });
    }, 1000);
    
    socket.on('disconnect', () => {
      clearInterval(interval);
    });
  });
}

module.exports = { initEntropySocket }; 