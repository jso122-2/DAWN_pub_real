import React from 'react';
import { HistogramProps } from '../../types/neural';

export const Histogram: React.FC<HistogramProps> = ({ 
  data, 
  bins = 10, 
  height = 15 
}) => {
  const renderASCIIHistogram = () => {
    if (!data.length) return 'NO DATA';
    
    // Calculate bins
    const min = Math.min(...data);
    const max = Math.max(...data);
    const range = max - min;
    const binWidth = range / bins;
    
    // Count values in each bin
    const counts = Array(bins).fill(0);
    data.forEach(value => {
      const binIndex = Math.min(
        Math.floor((value - min) / binWidth), 
        bins - 1
      );
      counts[binIndex]++;
    });
    
    const maxCount = Math.max(...counts);
    const lines: string[] = [];
    
    // Draw histogram from top to bottom
    for (let h = height; h >= 0; h--) {
      let line = '';
      const threshold = (h / height) * maxCount;
      
      counts.forEach((count, i) => {
        if (i > 0) line += ' ';
        if (count >= threshold) {
          line += '███';
        } else if (count >= threshold - maxCount / height / 2) {
          line += '▄▄▄';
        } else {
          line += '   ';
        }
      });
      
      // Y-axis labels
      if (h === height) {
        lines.push(`${maxCount.toString().padStart(3)} │${line}│`);
      } else if (h === 0) {
        lines.push(`  0 │${line}│`);
      } else {
        lines.push(`    │${line}│`);
      }
    }
    
    // X-axis
    lines.push(`    └${'───'.repeat(bins)}┘`);
    lines.push(`     ENTROPY DISTRIBUTION`);
    
    return lines.join('\n');
  };

  return (
    <div className="histogram">
      <pre className="ascii-display">
        {renderASCIIHistogram()}
      </pre>
      <div className="histogram-stats">
        <div>SAMPLES: {data.length}</div>
        <div>MEAN: {(data.reduce((a, b) => a + b, 0) / data.length).toFixed(2)}</div>
        <div>MAX: {Math.max(...data).toFixed(2)}</div>
        <div>MIN: {Math.min(...data).toFixed(2)}</div>
      </div>
    </div>
  );
}; 