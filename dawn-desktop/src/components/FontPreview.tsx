import React, { useState } from 'react';

const FontPreview: React.FC = () => {
  const [selectedFont, setSelectedFont] = useState('dawn');
  const [fontSize, setFontSize] = useState('base');
  const [sampleText, setSampleText] = useState('The quick brown fox jumps over the lazy dog');
  
  const fonts = [
    { name: 'dawn', label: 'DAWN Stack' },
    { name: 'iosevka', label: 'Iosevka Term' },
    { name: 'jetbrains', label: 'JetBrains Mono' },
    { name: 'fantasque', label: 'Fantasque Sans Mono' },
  ];
  
  const sizes = ['xxs', 'xs', 'sm', 'base', 'lg', 'xl', '2xl'];
  
  const codeSample = `// DAWN Cognitive Architecture
function processNeuralInput(data) {
  const entropy = calculateEntropy(data);
  if (entropy > THRESHOLD) {
    return stabilizeSystem();
  }
  return { status: 'coherent', value: 0.42 };
}`;

  const fontClassName = `font-${selectedFont}`;
  const sizeClassName = `text-${fontSize}`;

  return (
    <div className="glass border-0 shadow-glow-sm p-6 hover:shadow-glow-md transition-all duration-300">
      <h2 className="text-2xl font-bold text-cyan-400 mb-6">Font Configuration Preview</h2>
      
      <div className="grid grid-cols-2 gap-6 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Font Family</label>
          <select
            value={selectedFont}
            onChange={(e) => setSelectedFont(e.target.value)}
            className="w-full px-3 py-2 glass-dark animate-breathe text-gray-200 rounded-md border-0 focus:border-cyan-500 hover:shadow-glow-md transition-all duration-300"
          >
            {fonts.map(font => (
              <option key={font.name} value={font.name}>{font.label}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Font Size</label>
          <select
            value={fontSize}
            onChange={(e) => setFontSize(e.target.value)}
            className="w-full px-3 py-2 glass-dark animate-breathe text-gray-200 rounded-md border-0 focus:border-cyan-500 hover:shadow-glow-md transition-all duration-300"
          >
            {sizes.map(size => (
              <option key={size} value={size}>text-{size}</option>
            ))}
          </select>
        </div>
      </div>
      
      <div className="space-y-6">
        <div>
          <h3 className="text-sm font-medium text-gray-400 mb-2">Text Sample</h3>
          <input
            type="text"
            value={sampleText}
            onChange={(e) => setSampleText(e.target.value)}
            className={`w-full px-4 py-3 glass-dark animate-breathe text-gray-200 rounded-md border border-gray-700 ${fontClassName} ${sizeClassName}`}
          />
        </div>
        
        <div>
          <h3 className="text-sm font-medium text-gray-400 mb-2">Code Sample</h3>
          <pre className={`p-4 glass-dark animate-breathe rounded-md overflow-x-auto ${fontClassName} ${sizeClassName} text-green-400 hover:shadow-glow-md transition-all duration-300`}>
            <code>{codeSample}</code>
          </pre>
        </div>
        
        <div>
          <h3 className="text-sm font-medium text-gray-400 mb-2">Character Set</h3>
          <div className={`p-4 glass-dark animate-breathe rounded-md ${fontClassName} ${sizeClassName} text-gray-300 hover:shadow-glow-md transition-all duration-300`}>
            <div>0123456789</div>
            <div>ABCDEFGHIJKLMNOPQRSTUVWXYZ</div>
            <div>abcdefghijklmnopqrstuvwxyz</div>
            <div>!@#$%^&*()_+-=[]{}|;:'",./?</div>
            <div>≈ ≠ ≤ ≥ ± × ÷ ∞ ∑ ∏ √ ∫ ∂ ∇ ∈ ∉ ⊂ ⊃ ∪ ∩</div>
          </div>
        </div>
        
        <div>
          <h3 className="text-sm font-medium text-gray-400 mb-2">Ligatures Test</h3>
          <div className={`p-4 glass-dark animate-breathe rounded-md ${fontClassName} ${sizeClassName} text-gray-300 space-y-1 hover:shadow-glow-md transition-all duration-300`}>
            <div>!= == === =&gt; -&gt; &lt;- &lt;=&gt; ++ -- ** // /* */</div>
            <div>.. ... :: :: &lt;&lt; &gt;&gt; |&gt; &lt;| || &amp;&amp; ??</div>
            <div>www ffi ffl ff fi fl</div>
          </div>
        </div>
      </div>
      
      <div className="mt-6 p-4 glass-dark animate-breathe rounded-md hover:shadow-glow-md transition-all duration-300">
        <p className="text-sm text-gray-400">
          Current class: <code className="text-cyan-400">{fontClassName} {sizeClassName}</code>
        </p>
      </div>
    </div>
  );
};

export default FontPreview; 