import React, { Suspense, lazy } from 'react';
import GlassPanel from '../GlassPanel';
import '../../dashboard.css';
// Lazy load heavy components
const NeuralProcessMap = lazy(() => import('../cortex/NeuralProcessMap'));
const EntropyRingHUD = lazy(() => import('../overlays/EntropyRingHUD'));
const ModulationConsole = lazy(() => import('../controls/ModulationConsole'));
const LiveMemoryScroll = lazy(() => import('../logs/LiveMemoryScroll'));

// DAWN logo SVG (inline for demo)
const DawnLogo = () => (
  <svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="DAWN Logo" style={{position:'absolute',top:24,left:32,zIndex:10}}>
    <circle cx="32" cy="32" r="28" stroke="#00fff7" strokeWidth="4" fill="#0f172a"/>
    <path d="M32 16L40 48L32 40L24 48L32 16Z" fill="#a855f7"/>
  </svg>
);

// Easter egg: fun mode toggle
const useEasterEgg = () => {
  const [active, setActive] = React.useState(false);
  React.useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.ctrlKey && e.altKey && e.key.toLowerCase() === 'e') setActive(a => !a);
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, []);
  return active;
};

// Placeholder: Floating NeuroShell Terminal
const NeuroShellTerminal = () => (
  <div
    className="glass-panel neon-glow-cyan neural-terminal"
    style={{
      position: 'fixed',
      bottom: 32,
      left: '50%',
      transform: 'translateX(-50%)',
      minWidth: 420,
      zIndex: 100,
      padding: '1.5rem 2rem',
      backdropFilter: 'blur(16px)',
      borderRadius: 24,
      boxShadow: '0 0 32px 4px #00fff7, 0 0 64px 8px #a855f7',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'stretch',
      fontFamily: 'JetBrains Mono, monospace',
      fontSize: 18,
      letterSpacing: 1.2,
      background: 'rgba(20,30,40,0.7)',
      cursor: 'grab',
    }}
    tabIndex={0}
    aria-label="NeuroShell Terminal"
  >
    <div style={{marginBottom: 8, color: '#00fff7', fontWeight: 700}}>NeuroShell Terminal</div>
    <div style={{color: '#fff', opacity: 0.8}}>&gt; <span className="neural-cursor">█</span></div>
    {/* TODO: Command input, neural pulse feedback, drag logic */}
  </div>
);

// Placeholder: Voice Input Waveform
const VoiceWaveform = () => (
  <div
    className="glass-panel neon-glow-purple neural-waveform"
    style={{
      position: 'fixed',
      top: 32,
      left: '50%',
      transform: 'translateX(-50%)',
      width: 320,
      height: 64,
      zIndex: 101,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'rgba(30,20,50,0.5)',
      borderRadius: 32,
      pointerEvents: 'none',
    }}
    aria-label="Voice Input Waveform"
  >
    {/* TODO: Animated neural waveform responding to mic input */}
    <svg width="300" height="48">
      <polyline points="0,24 30,12 60,36 90,18 120,30 150,12 180,36 210,18 240,30 270,12 300,24" stroke="#a855f7" strokeWidth="4" fill="none" opacity="0.7"/>
    </svg>
  </div>
);

// Placeholder: GesturePanelWrapper
const GesturePanelWrapper = ({children}:{children:React.ReactNode}) => (
  <div className="neural-gesture-wrapper" style={{position:'relative'}}>{children}</div>
  // TODO: Add gesture listeners, neural ripple feedback
);

// Placeholder: CommandPreview with NLP indicator
const CommandPreview = () => (
  <div
    className="glass-panel neon-glow-mixed neural-command-preview"
    style={{
      position: 'fixed',
      bottom: 120,
      left: '50%',
      transform: 'translateX(-50%)',
      minWidth: 340,
      zIndex: 102,
      padding: '1rem 1.5rem',
      borderRadius: 20,
      background: 'rgba(30,30,60,0.7)',
      color: '#fff',
      fontFamily: 'JetBrains Mono, monospace',
      fontSize: 16,
      display: 'flex',
      alignItems: 'center',
      gap: 16,
      boxShadow: '0 0 32px 4px #00fff7, 0 0 64px 8px #a855f7',
    }}
    aria-label="Command Preview"
  >
    <span style={{color:'#00fff7'}}>Predict:</span>
    <span style={{flex:1,opacity:0.85}}>Reboot neural subsystem</span>
    <span className="nlp-indicator" style={{width:24,height:24,display:'inline-block',borderRadius:'50%',background:'radial-gradient(circle,#a855f7 60%,#00fff7 100%)',boxShadow:'0 0 12px #a855f7,0 0 24px #00fff7',animation:'pulse 1.2s infinite alternate'}}></span>
    {/* TODO: NLP confidence, animated outcome, real command preview */}
  </div>
);

// Placeholder: ClaudeStatusBeacon
const ClaudeStatusBeacon = () => (
  <div
    className="neural-claude-beacon"
    style={{
      position: 'fixed',
      top: 32,
      right: 48,
      zIndex: 200,
      width: 48,
      height: 48,
      borderRadius: '50%',
      background: 'radial-gradient(circle,#00fff7 60%,#a855f7 100%)',
      boxShadow: '0 0 24px 8px #00fff7,0 0 48px 16px #a855f7',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      border: '2px solid #00fff7',
      animation: 'pulse 1.5s infinite alternate',
    }}
    aria-label="Claude AI Status"
  >
    <span style={{fontSize:28,color:'#fff',fontWeight:700,textShadow:'0 0 8px #a855f7'}}>C</span>
    {/* TODO: Dynamic status, neural glow, Claude API integration */}
  </div>
);

const VisualizationDashboard: React.FC = () => {
  const easterEgg = useEasterEgg();
  // Keyboard navigation: focus trap for panels
  const panelRefs = [React.useRef<HTMLDivElement>(null), React.useRef<HTMLDivElement>(null), React.useRef<HTMLDivElement>(null), React.useRef<HTMLDivElement>(null)];
  const focusPanel = (idx: number) => panelRefs[idx].current?.focus();

  return (
    <div
      className={`dashboard-container${easterEgg ? ' fun-mode' : ''}`}
      style={{
        minHeight: '100vh',
        background: '#000',
        position: 'relative',
        overflow: 'hidden',
      }}
      aria-label="DAWN Cognitive Dashboard"
    >
      {/* DAWN Logo/Branding */}
      <DawnLogo />
      {/* Subtle grid pattern overlay */}
      <div
        aria-hidden="true"
        style={{
          pointerEvents: 'none',
          position: 'absolute',
          inset: 0,
          zIndex: 0,
          backgroundImage:
            'linear-gradient(rgba(0,255,255,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(168,85,247,0.04) 1px, transparent 1px)',
          backgroundSize: '40px 40px',
        }}
      />
      {/* Floating neural overlays */}
      <NeuroShellTerminal />
      <VoiceWaveform />
      <CommandPreview />
      <ClaudeStatusBeacon />
      {/* Main panels wrapped with gesture controls */}
      <GesturePanelWrapper>
        <GlassPanel
          ref={panelRefs[0]}
          glow="mixed"
          tabIndex={0}
          aria-label="Neural Process Map"
          style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            maxWidth: 600,
            width: '60vw',
            zIndex: 2,
            outline: 'none',
          }}
          onKeyDown={(e: React.KeyboardEvent<HTMLDivElement>) => { if (e.key === 'ArrowRight') focusPanel(1); if (e.key === 'ArrowLeft') focusPanel(2); }}
        >
          <Suspense fallback={<div>Loading Neural Map...</div>}>
            <NeuralProcessMap />
          </Suspense>
        </GlassPanel>
        <GlassPanel
          ref={panelRefs[1]}
          glow="purple"
          tabIndex={0}
          aria-label="Entropy Ring HUD"
          style={{
            position: 'absolute',
            top: 32,
            right: 48,
            zIndex: 3,
            outline: 'none',
          }}
          onKeyDown={(e: React.KeyboardEvent<HTMLDivElement>) => { if (e.key === 'ArrowLeft') focusPanel(0); if (e.key === 'ArrowDown') focusPanel(3); }}
        >
          <Suspense fallback={<div>Loading HUD...</div>}>
            <EntropyRingHUD />
          </Suspense>
        </GlassPanel>
        <GlassPanel
          ref={panelRefs[2]}
          glow="cyan"
          tabIndex={0}
          aria-label="Modulation Console"
          style={{
            position: 'absolute',
            top: '50%',
            left: 48,
            transform: 'translateY(-50%)',
            zIndex: 3,
            outline: 'none',
          }}
          onKeyDown={(e: React.KeyboardEvent<HTMLDivElement>) => { if (e.key === 'ArrowRight') focusPanel(0); if (e.key === 'ArrowUp') focusPanel(1); }}
        >
          <Suspense fallback={<div>Loading Console...</div>}>
            <ModulationConsole />
          </Suspense>
        </GlassPanel>
        <GlassPanel
          ref={panelRefs[3]}
          glow="mixed"
          tabIndex={0}
          aria-label="Live Memory Scroll"
          style={{
            position: 'fixed',
            top: 0,
            right: 0,
            height: '100vh',
            width: 340,
            borderLeft: '2px solid #a855f7',
            borderRadius: '24px 0 0 24px',
            zIndex: 4,
            display: 'flex',
            flexDirection: 'column',
            outline: 'none',
          }}
          onKeyDown={(e: React.KeyboardEvent<HTMLDivElement>) => { if (e.key === 'ArrowLeft') focusPanel(0); }}
        >
          <Suspense fallback={<div>Loading Memory...</div>}>
            <LiveMemoryScroll />
          </Suspense>
        </GlassPanel>
      </GesturePanelWrapper>
      {/* Easter egg fun mode overlay */}
      {easterEgg && (
        <div style={{position:'fixed',inset:0,zIndex:100,background:'rgba(0,0,0,0.7)',display:'flex',alignItems:'center',justifyContent:'center',color:'#00fff7',fontSize:'2rem',fontWeight:700,backdropFilter:'blur(8px)'}}>
          <span>💜 Eat your heart out! 💙</span>
        </div>
      )}
    </div>
  );
};

export default VisualizationDashboard; 