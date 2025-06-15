import React from 'react';
import { Play } from 'lucide-react';

const DemoPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-orange-900 to-amber-900 text-white p-6">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4 flex items-center justify-center gap-3">
            <Play className="w-10 h-10 text-amber-400" />
            Live Demo
          </h1>
          <p className="text-gray-300 text-lg">
            Experience real-time consciousness simulation and interaction
          </p>
        </div>
        
        <div className="bg-white/5 backdrop-blur-lg rounded-xl p-8 border border-white/10">
          <p className="text-gray-300">
            Live demonstration interface coming soon...
          </p>
        </div>
      </div>
    </div>
  );
};

export default DemoPage; 