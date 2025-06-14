import React, { useState, useEffect } from 'react';
import { useOwlState } from '../hooks/useOwlState';
import { Observation, StrategicPlan, StrategicRecommendation } from '../types/owl.types';
import { owlConfig } from '../config/owl.config';

interface OwlDashboardProps {
  className?: string;
  showFullDetail?: boolean;
}

export const OwlDashboard: React.FC<OwlDashboardProps> = ({
  className = '',
  showFullDetail = false
}) => {
  const {
    isConnected,
    connectionStatus,
    lastError,
    observations,
    activePlans,
    recommendations,
    observationCount,
    getRecentObservations,
    getHighSignificanceObservations,
    getActiveRecommendations,
    requestObservations,
    requestPlans
  } = useOwlState({
    onObservation: (obs) => {
      if (obs.significance > 0.8) {
        console.log('🦉 High significance observation:', obs);
      }
    },
    onRecommendation: (rec) => {
      if (rec.urgency >= 8) {
        console.log('🦉 Urgent recommendation:', rec);
      }
    }
  });

  const [selectedTab, setSelectedTab] = useState<'observations' | 'plans' | 'insights'>('observations');
  const [filter, setFilter] = useState<string>('all');

  useEffect(() => {
    if (isConnected) {
      requestObservations(50);
      requestPlans();
    }
  }, [isConnected, requestObservations, requestPlans]);

  const getStatusColor = () => {
    switch (connectionStatus) {
      case 'connected': return 'text-green-500';
      case 'connecting': return 'text-yellow-500';
      case 'error': return 'text-red-500';
      default: return 'text-gray-500';
    }
  };

  const getStatusIcon = () => {
    switch (connectionStatus) {
      case 'connected': return '🟢';
      case 'connecting': return '🟡';
      case 'error': return '🔴';
      default: return '⚫';
    }
  };

  const formatObservationType = (type: string) => {
    return type.charAt(0).toUpperCase() + type.slice(1);
  };

  const getSignificanceColor = (significance: number) => {
    if (significance >= 0.8) return 'text-red-500';
    if (significance >= 0.6) return 'text-yellow-500';
    return 'text-blue-500';
  };

  const getPriorityColor = (urgency: number) => {
    if (urgency >= 8) return 'bg-red-100 text-red-800';
    if (urgency >= 6) return 'bg-yellow-100 text-yellow-800';
    return 'bg-blue-100 text-blue-800';
  };

  const filteredObservations = observations.filter(obs => {
    if (filter === 'all') return true;
    if (filter === 'high-significance') return obs.significance >= 0.7;
    return obs.type === filter;
  });

  const recentObservations = getRecentObservations(10);
  const highSigObservations = getHighSignificanceObservations();
  const urgentRecommendations = getActiveRecommendations();

  return (
    <div className={`bg-white rounded-lg shadow-lg ${className}`}>
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <span className="text-2xl">🦉</span>
            <h2 className="text-xl font-semibold text-gray-900">Owl Strategic Observer</h2>
            <span className={`flex items-center space-x-1 text-sm ${getStatusColor()}`}>
              <span>{getStatusIcon()}</span>
              <span className="capitalize">{connectionStatus}</span>
            </span>
          </div>
          
          <div className="flex items-center space-x-4 text-sm text-gray-600">
            <span>Observations: {observationCount}</span>
            <span>Plans: {activePlans.length}</span>
            <span>Recommendations: {recommendations.length}</span>
          </div>
        </div>

        {lastError && (
          <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
            {lastError}
          </div>
        )}
      </div>

      {/* Navigation Tabs */}
      <div className="px-6 py-3 border-b border-gray-200">
        <nav className="flex space-x-8">
          {(['observations', 'plans', 'insights'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setSelectedTab(tab)}
              className={`pb-2 text-sm font-medium capitalize transition-colors ${
                selectedTab === tab
                  ? 'border-b-2 border-indigo-500 text-indigo-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              {tab}
            </button>
          ))}
        </nav>
      </div>

      {/* Content */}
      <div className="p-6">
        {selectedTab === 'observations' && (
          <div>
            {/* Filters */}
            <div className="mb-4 flex items-center space-x-4">
              <label className="text-sm font-medium text-gray-700">Filter:</label>
              <select
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                className="px-3 py-1 border border-gray-300 rounded text-sm"
              >
                <option value="all">All Types</option>
                <option value="high-significance">High Significance</option>
                <option value="pattern">Patterns</option>
                <option value="anomaly">Anomalies</option>
                <option value="transition">Transitions</option>
                <option value="milestone">Milestones</option>
              </select>
            </div>

            {/* Observations List */}
            <div className="space-y-3">
              {filteredObservations.slice(-20).reverse().map((obs) => (
                <div
                  key={obs.id}
                  className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-1">
                        <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded font-medium">
                          {formatObservationType(obs.type)}
                        </span>
                        <span className={`text-sm font-medium ${getSignificanceColor(obs.significance)}`}>
                          {(obs.significance * 100).toFixed(0)}% significance
                        </span>
                        <span className="text-xs text-gray-500">
                          Tick {obs.tick}
                        </span>
                      </div>
                      
                      <p className="text-gray-900 mb-2">{obs.content}</p>
                      
                      {obs.metadata.tags.length > 0 && (
                        <div className="flex flex-wrap gap-1">
                          {obs.metadata.tags.map((tag, idx) => (
                            <span
                              key={idx}
                              className="px-2 py-1 bg-blue-50 text-blue-700 text-xs rounded"
                            >
                              {tag}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                    
                    <div className="ml-4 text-right">
                      <div className="text-xs text-gray-500">
                        Confidence: {(obs.confidence * 100).toFixed(0)}%
                      </div>
                      {obs.reflections.length > 0 && (
                        <div className="text-xs text-indigo-600 mt-1">
                          {obs.reflections.length} reflection{obs.reflections.length !== 1 ? 's' : ''}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}

              {filteredObservations.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  <span className="text-4xl mb-2 block">🦉</span>
                  <p>No observations match the current filter.</p>
                  <p className="text-sm mt-1">Owl is observing and will report significant events.</p>
                </div>
              )}
            </div>
          </div>
        )}

        {selectedTab === 'plans' && (
          <div>
            <div className="grid gap-4">
              {activePlans.map((plan) => (
                <div
                  key={plan.id}
                  className="p-4 border border-gray-200 rounded-lg"
                >
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-medium text-gray-900">{plan.name}</h3>
                    <span className={`px-2 py-1 text-xs rounded font-medium ${
                      plan.status === 'active' ? 'bg-green-100 text-green-800' :
                      plan.status === 'proposed' ? 'bg-blue-100 text-blue-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {plan.status}
                    </span>
                  </div>
                  
                  <p className="text-gray-700 text-sm mb-3">{plan.description}</p>
                  
                  <div className="flex items-center justify-between text-xs text-gray-500">
                    <span>Horizon: {plan.horizon} ticks</span>
                    <span>Confidence: {(plan.confidence * 100).toFixed(0)}%</span>
                  </div>
                </div>
              ))}

              {activePlans.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  <span className="text-4xl mb-2 block">📋</span>
                  <p>No active strategic plans.</p>
                  <p className="text-sm mt-1">Owl will create plans based on observations and patterns.</p>
                </div>
              )}
            </div>
          </div>
        )}

        {selectedTab === 'insights' && (
          <div>
            {/* Urgent Recommendations */}
            {urgentRecommendations.length > 0 && (
              <div className="mb-6">
                <h3 className="text-lg font-medium text-gray-900 mb-3">Urgent Recommendations</h3>
                <div className="space-y-3">
                  {urgentRecommendations.map((rec) => (
                    <div
                      key={rec.id}
                      className="p-4 border-l-4 border-red-400 bg-red-50 rounded-r-lg"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-1">
                            <span className={`px-2 py-1 text-xs rounded font-medium ${getPriorityColor(rec.urgency)}`}>
                              Priority {rec.urgency}/10
                            </span>
                            <span className="text-xs text-gray-600 capitalize">
                              {rec.type.replace('_', ' ')}
                            </span>
                          </div>
                          
                          <p className="text-gray-900 font-medium mb-1">{rec.description}</p>
                          <p className="text-gray-700 text-sm">{rec.rationale}</p>
                        </div>
                        
                        <div className="ml-4 text-right text-xs text-gray-500">
                          Confidence: {(rec.confidence * 100).toFixed(0)}%
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* High Significance Observations Summary */}
            {highSigObservations.length > 0 && (
              <div className="mb-6">
                <h3 className="text-lg font-medium text-gray-900 mb-3">High Significance Events</h3>
                <div className="grid gap-3">
                  {highSigObservations.slice(-5).map((obs) => (
                    <div
                      key={obs.id}
                      className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg"
                    >
                      <div className="flex items-center justify-between text-sm">
                        <span className="font-medium text-yellow-800">{obs.content}</span>
                        <span className="text-yellow-600">
                          {(obs.significance * 100).toFixed(0)}% significance
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Summary Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="p-4 bg-blue-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">{observationCount}</div>
                <div className="text-sm text-blue-800">Total Observations</div>
              </div>
              
              <div className="p-4 bg-green-50 rounded-lg">
                <div className="text-2xl font-bold text-green-600">{highSigObservations.length}</div>
                <div className="text-sm text-green-800">High Significance</div>
              </div>
              
              <div className="p-4 bg-purple-50 rounded-lg">
                <div className="text-2xl font-bold text-purple-600">{activePlans.length}</div>
                <div className="text-sm text-purple-800">Active Plans</div>
              </div>
              
              <div className="p-4 bg-red-50 rounded-lg">
                <div className="text-2xl font-bold text-red-600">{urgentRecommendations.length}</div>
                <div className="text-sm text-red-800">Urgent Actions</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}; 