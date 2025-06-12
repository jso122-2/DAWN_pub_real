import React, { useState } from 'react';

const TabSystem = ({ activeTab, onTabChange }) => {
  const tabs = [
    { id: 'neural', label: 'Neural Monitor', icon: '🧠' },
    { id: 'fractal', label: 'Fractal', icon: '🌀' },
    { id: 'talk', label: 'Talk To', icon: '💬' },
    { id: 'processes', label: 'Processes', icon: '⚙️' }
  ];

  return (
    <div className="bg-gray-900 border-b border-gray-700">
      <div className="flex items-center justify-between px-6 py-3">
        <div className="flex items-center space-x-1">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`
                flex items-center space-x-2 px-4 py-2 rounded-t-lg transition-all duration-200
                ${activeTab === tab.id 
                  ? 'bg-gray-800 text-white border-t border-l border-r border-gray-600' 
                  : 'bg-gray-950 text-gray-400 hover:bg-gray-800 hover:text-white'
                }
              `}
            >
              <span className="text-lg">{tab.icon}</span>
              <span className="font-medium">{tab.label}</span>
              {activeTab === tab.id && (
                <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse ml-2"></span>
              )}
            </button>
          ))}
        </div>
        
        <div className="flex items-center space-x-2">
          <span className="text-xs text-gray-500">Active: {activeTab}</span>
          <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></div>
        </div>
      </div>
    </div>
  );
};

export default TabSystem;
