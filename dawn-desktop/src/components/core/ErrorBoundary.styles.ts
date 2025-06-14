import { css } from '@emotion/css';

export const errorContainer = css`
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  padding: 2rem;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(248, 113, 113, 0.2);
  border-radius: 12px;
  backdrop-filter: blur(10px);
`;

export const errorContent = css`
  text-align: center;
  max-width: 400px;
`;

export const errorIcon = css`
  color: rgba(248, 113, 113, 0.8);
  margin-bottom: 1rem;
`;

export const errorTitle = css`
  font-size: 1.5rem;
  font-weight: 600;
  color: rgba(248, 113, 113, 0.9);
  margin: 0 0 0.5rem 0;
`;

export const errorMessage = css`
  color: rgba(226, 232, 240, 0.8);
  margin: 0 0 1.5rem 0;
  line-height: 1.5;
`;

export const retryButton = css`
  padding: 0.75rem 1.5rem;
  background: rgba(248, 113, 113, 0.2);
  border: 1px solid rgba(248, 113, 113, 0.4);
  border-radius: 8px;
  color: rgba(248, 113, 113, 0.9);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: rgba(248, 113, 113, 0.3);
    transform: translateY(-1px);
  }
`; 