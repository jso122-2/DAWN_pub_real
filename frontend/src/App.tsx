import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ActivityMonitor from './pages/ActivityMonitor';
import TalkToDAWN from './pages/TalkToDAWN';
import VisualProcesses from './pages/VisualProcesses';
import ViteHealthCheck from './components/ViteHealthCheck';
import ConnectionStatusBadge from './components/ConnectionStatusBadge';
import './App.css';

function App() {
  return (
    <>
      <ViteHealthCheck />
      <ConnectionStatusBadge />
      <nav style={{ background: '#111', padding: '10px', display: 'flex', gap: '2rem' }}>
        <Link style={{ color: '#00ff88', textDecoration: 'none', fontWeight: 'bold' }} to="/">Activity Monitor</Link>
        <Link style={{ color: '#00ff88', textDecoration: 'none', fontWeight: 'bold' }} to="/talk">Talk to DAWN</Link>
        <Link style={{ color: '#00ff88', textDecoration: 'none', fontWeight: 'bold' }} to="/visuals">Visual Processes</Link>
      </nav>
      <div className="app">
        <Routes>
          <Route path="/" element={<ActivityMonitor />} />
          <Route path="/talk" element={<TalkToDAWN />} />
          <Route path="/visuals" element={<VisualProcesses />} />
        </Routes>
      </div>
    </>
  );
}

export default App; 