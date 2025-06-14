import { css } from '@emotion/css';

export const container = css`
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 600px;
`;

export const header = css`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
`;

export const title = css`
  font-size: 1.25rem;
  font-weight: 600;
  color: rgba(226, 232, 240, 0.9);
  margin: 0;
`;

export const modeSelector = css`
  display: flex;
  gap: 0.5rem;
`;

export const modeButton = (isActive: boolean) => css`
  padding: 0.5rem 1rem;
  background: ${isActive 
    ? 'rgba(59, 130, 246, 0.2)' 
    : 'rgba(15, 23, 42, 0.4)'};
  border: 1px solid ${isActive 
    ? 'rgba(59, 130, 246, 0.4)' 
    : 'rgba(148, 163, 184, 0.2)'};
  border-radius: 6px;
  color: ${isActive 
    ? 'rgba(147, 197, 253, 0.9)' 
    : 'rgba(148, 163, 184, 0.8)'};
  font-size: 0.875rem;
  font-weight: 500;
  text-transform: capitalize;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: ${isActive 
      ? 'rgba(59, 130, 246, 0.3)' 
      : 'rgba(15, 23, 42, 0.6)'};
  }
`;

export const visualizationContainer = css`
  flex: 1;
  position: relative;
  overflow: hidden;
`;

export const combinedView = css`
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 1px;
  height: 100%;
  background: rgba(148, 163, 184, 0.1);
`;

export const quadrant = css`
  background: rgba(15, 23, 42, 0.4);
  position: relative;
  overflow: hidden;
`;

export const metrics = css`
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;

  h4 {
    margin: 0 0 1rem 0;
    color: rgba(226, 232, 240, 0.9);
    font-size: 1rem;
    font-weight: 600;
  }
`;

export const metricItem = css`
  display: grid;
  grid-template-columns: 100px 1fr 60px;
  align-items: center;
  gap: 1rem;
  font-size: 0.875rem;
  color: rgba(148, 163, 184, 0.9);
`;

export const metricBar = css`
  height: 8px;
  background: rgba(30, 41, 59, 0.6);
  border-radius: 4px;
  overflow: hidden;
  position: relative;
`;

export const metricFill = css`
  height: 100%;
  transition: width 0.3s ease;
  border-radius: 4px;
`;

export const moodIndicator = css`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 1rem;
`;

export const moodDisplay = css`
  padding: 1rem;
  border-radius: 12px;
  text-align: center;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  text-transform: capitalize;
  transition: all 0.5s ease;
`;

export const waveformContainer = (fullscreen?: boolean) => css`
  position: relative;
  width: 100%;
  height: 100%;
  min-height: ${fullscreen ? '500px' : '150px'};
`;

export const particleContainer = (fullscreen?: boolean) => css`
  position: relative;
  width: 100%;
  height: 100%;
  min-height: ${fullscreen ? '500px' : '150px'};
`;

export const canvas = css`
  width: 100%;
  height: 100%;
`;

export const waveformInfo = css`
  position: absolute;
  bottom: 1rem;
  left: 1rem;
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
  color: rgba(148, 163, 184, 0.7);
  background: rgba(15, 23, 42, 0.8);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  backdrop-filter: blur(10px);
`;

export const particleInfo = css`
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
  color: rgba(148, 163, 184, 0.7);
  background: rgba(15, 23, 42, 0.8);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  backdrop-filter: blur(10px);
`; 