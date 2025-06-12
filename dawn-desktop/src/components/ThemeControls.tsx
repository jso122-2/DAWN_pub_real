import React, { useState, useEffect } from 'react';
import {
  themes,
  setTheme,
  getTheme,
  setEntropy,
  startAutoSwitch,
  stopAutoSwitch,
  registerComponentOverride,
  unregisterComponentOverride,
} from '../theme/themeSystem';

const ThemeControls: React.FC = () => {
  const [open, setOpen] = useState(false);
  const [theme, setThemeState] = useState(getTheme());
  const [entropy, setEntropyState] = useState(0);
  const [autoSwitch, setAutoSwitch] = useState(false);

  useEffect(() => {
    setTheme(theme, { smooth: true });
    if (theme === 'entropy') setEntropy(entropy);
  }, [theme]);

  useEffect(() => {
    if (theme === 'entropy') setEntropy(entropy);
  }, [entropy, theme]);

  useEffect(() => {
    if (autoSwitch) startAutoSwitch();
    else stopAutoSwitch();
    return stopAutoSwitch;
  }, [autoSwitch]);

  return (
    <div
      style={{
        position: 'fixed',
        top: 24,
        right: 24,
        zIndex: 1000,
        background: 'var(--color-bg, #18181b)',
        color: 'var(--color-fg, #e0eaff)',
        borderRadius: 16,
        boxShadow: '0 4px 32px rgba(0,0,0,0.25)',
        border: '1px solid var(--color-border, #3b82f6)',
        padding: open ? 20 : 8,
        transition: 'all 0.3s cubic-bezier(.4,2,.6,1)',
        opacity: 0.95,
        minWidth: open ? 220 : 48,
        minHeight: 48,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-end',
      }}
    >
      <button
        style={{
          background: 'none',
          border: 'none',
          color: 'inherit',
          fontSize: 24,
          cursor: 'pointer',
          marginBottom: open ? 12 : 0,
        }}
        title="Theme Picker"
        onClick={() => setOpen(o => !o)}
      >
        {open ? '🎨' : '🌈'}
      </button>
      {open && (
        <div style={{ width: 180 }}>
          <div style={{ marginBottom: 12 }}>
            <strong>Theme</strong>
            <select
              value={theme}
              onChange={e => setThemeState(e.target.value as any)}
              style={{
                width: '100%',
                marginTop: 6,
                padding: 6,
                borderRadius: 8,
                border: '1px solid var(--color-border, #3b82f6)',
                background: 'var(--color-bg, #18181b)',
                color: 'var(--color-fg, #e0eaff)',
              }}
            >
              {Object.values(themes).map(t => (
                <option key={t.name} value={t.name}>{t.displayName}</option>
              ))}
            </select>
          </div>
          {theme === 'entropy' && (
            <div style={{ marginBottom: 12 }}>
              <label>
                <span>Entropy: {entropy}</span>
                <input
                  type="range"
                  min={0}
                  max={100}
                  value={entropy}
                  onChange={e => setEntropyState(Number(e.target.value))}
                  style={{ width: '100%' }}
                />
              </label>
            </div>
          )}
          <div style={{ marginBottom: 12 }}>
            <label style={{ display: 'flex', alignItems: 'center' }}>
              <input
                type="checkbox"
                checked={autoSwitch}
                onChange={e => setAutoSwitch(e.target.checked)}
                style={{ marginRight: 8 }}
              />
              Auto-switch by time
            </label>
          </div>
          <div style={{ fontSize: 12, color: 'var(--color-accent, #a78bfa)' }}>
            Current: <b>{themes[theme].displayName}</b>
          </div>
        </div>
      )}
    </div>
  );
};

export default ThemeControls; 