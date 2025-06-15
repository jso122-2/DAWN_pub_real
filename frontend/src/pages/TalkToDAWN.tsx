import React from 'react';
import { Terminal } from '../components/Terminal';

const TalkToDAWN: React.FC = () => {
  return (
    <div className="talk-to-dawn">
      <h1>Talk to DAWN</h1>
      <div className="terminal-container">
        <Terminal />
      </div>
    </div>
  );
};

export default TalkToDAWN; 