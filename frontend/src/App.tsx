import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import VisualProcesses from './pages/VisualProcesses';
import TalkToDAWN from './pages/TalkToDAWN';
import ActivityMonitor from './pages/ActivityMonitor';
import './styles/global.css';

const App: React.FC = () => {
  return (
    <Router>
      <div className="app">
        <nav className="nav">
          <Link to="/visuals">Visual Processes</Link>
          <Link to="/talk">Talk to DAWN</Link>
          <Link to="/monitor">Activity Monitor</Link>
        </nav>
        <main className="main">
          <Routes>
            <Route path="/" element={<TalkToDAWN />} />
            <Route path="/visuals" element={<VisualProcesses />} />
            <Route path="/talk" element={<TalkToDAWN />} />
            <Route path="/monitor" element={<ActivityMonitor />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App; 