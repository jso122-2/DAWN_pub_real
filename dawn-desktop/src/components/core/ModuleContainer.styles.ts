import { css, keyframes } from '@emotion/css';

const shimmer = keyframes`
  0% { background-position: -1000px 0; }
  100% { background-position: 1000px 0; }
`;

export const container = css`
  position: relative;
  min-width: 300px;
  min-height: 200px;
  border-radius: 16px;
  overflow: hidden;
  backdrop-filter: blur(20px);
  background: rgba(15, 23, 42, 0.3);
  border: 1px solid rgba(148, 163, 184, 0.1);
  transition: all 0.3s ease;
  
  &:hover {
    border-color: rgba(148, 163, 184, 0.2);
  }
`;

export const glassLayer = css`
  position: absolute;
  inset: 0;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.1) 0%,
    rgba(255, 255, 255, 0.05) 50%,
    transparent 100%
  );
  pointer-events: none;
`;

export const contentLayer = css`
  position: relative;
  z-index: 1;
  height: 100%;
  width: 100%;
`;

export const glowBorder = css`
  position: absolute;
  inset: -1px;
  border-radius: 16px;
  opacity: 0.5;
  z-index: -1;
  animation: ${shimmer} 3s ease-out infinite;
  background-size: 1000px 100%;
`;

export const closeButton = css`
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 8px;
  color: rgba(148, 163, 184, 0.8);
  cursor: pointer;
  z-index: 10;
  transition: all 0.2s ease;

  &:hover {
    background: rgba(15, 23, 42, 0.8);
    color: rgba(226, 232, 240, 0.9);
    border-color: rgba(148, 163, 184, 0.4);
  }
`; 