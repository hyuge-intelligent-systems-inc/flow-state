import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

const Analytics = ({ user }) => {
  const [insights, setInsights] = useState(null);
  const [patterns, setPatterns] = useState(null);
  const [tagAnalytics, setTagAnalytics] = useState(null);
  const [timeframe, setTimeframe] = useState(30);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalyticsData();
  }, [user, timeframe]);

  const loadAnalyticsData = async () => {
    setLoading(true);
    try {
      const [insightsData, patternsData, tagAnalyticsData] = await Promise.all([
        apiService.getInsights(user.user_id, timeframe),
        apiService.getPatterns(user.user_id),
        apiService.getTagAnalytics(user.user_id, timeframe)
      ]);
      
      setInsights(insightsData);
      setPatterns(patternsData);
      setTagAnalytics(tagAnalyticsData);
    } catch (error) {
      console.error('Error loading analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDuration = (minutes) => {
    if (!minutes) return '0m';
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
  };

  const getConfidenceColor = (confidence) => {
    switch (confidence?.toLowerCase()) {
      case 'high': return 'text-green-600 bg-green-100';
      case 'moderate': return 'text-yellow-600 bg-yellow-100';
      case 'low': return 'text-orange-600 bg-orange-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const PatternCard = ({ name, pattern }) => (
    <div className="flow-card pattern-visualization">
      <div className="flex justify-between items-start mb-3">
        <h4 className="text-lg font-semibold text-flow-dark">{name.replace(/_/g, ' ').toUpperCase()}</h4>
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getConfidenceColor(pattern.confidence)}`}>
          {pattern.confidence} confidence
        </span>
      </div>
      
      <p className="text-flow-gray mb-4">{pattern.description}</p>
      
      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-flow-gray">Sample Size:</span>
          <span className="font-medium">{pattern.sample_size} data points</span>
        </div>
        
        {pattern.user_interpretation_needed && (
          <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg mt-4">
            <p className="text-sm text-blue-800">
              💭 <strong>Your interpretation needed:</strong> This pattern observation is based on your data. 
              What does this mean for your productivity?
            </p>
          </div>
        )}
        
        {pattern.limitations && (
          <div className="mt-3 p-2 bg-gray-50 rounded text-xs text-gray-600">
            <strong>Limitations:</strong> {pattern.limitations}
          </div>
        )}
      </div>
    </div>
  );

  const InsightCard = ({ insight, index }) => (
    <div className="flow-card insight-card">
      <div className="flex items-start space-x-3">
        <div className="flex-shrink-0">
          <div className="w-8 h-8 bg-flow-purple bg-opacity-10 rounded-lg flex items-center justify-center">
            <span className="text-flow-purple">🧠</span>
          </div>
        </div>
        <div className="flex-1">
          <div className="flex justify-between items-start mb-2">
            <h4 className="font-medium text-flow-dark">AI Insight #{index + 1}</h4>
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getConfidenceColor(insight.confidence)}`}>
              {insight.confidence}
            </span>
          </div>
          
          <p className="text-flow-gray mb-3">{insight.description}</p>
          
          {insight.supporting_evidence && insight.supporting_evidence.length > 0 && (
            <div className="text-sm">
              <p className="font-medium text-flow-dark mb-1">Supporting Evidence:</p>
              <ul className="list-disc list-inside text-flow-gray space-y-1">
                {insight.supporting_evidence.slice(0, 2).map((evidence, i) => (
                  <li key={i}>{evidence}</li>
                ))}
              </ul>
            </div>
          )}
          
          {insight.limitations && (
            <div className="mt-3 p-2 bg-gray-50 rounded text-xs text-gray-600">
              <strong>Limitations:</strong> {insight.limitations}
            </div>
          )}
        </div>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-flow-blue"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-flow-dark">Analytics & Insights</h1>
          <p className="text-flow-gray mt-1">
            Understanding your productivity patterns with honest limitations
          </p>
        </div>
        
        <select
          value={timeframe}
          onChange={(e) => setTimeframe(parseInt(e.target.value))}
          className="flow-input w-auto"
        >
          <option value={7}>Last 7 days</option>
          <option value={30}>Last 30 days</option>
          <option value={90}>Last 90 days</option>
        </select>
      </div>

      {/* Summary Stats */}
      {insights?.time_tracking_insights && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="flow-card">
            <div className="text-center">
              <div className="text-3xl font-bold text-flow-blue mb-2">
                {insights.time_tracking_insights.active_days}
              </div>
              <p className="text-flow-gray">Active Days</p>
            </div>
          </div>
          
          <div className="flow-card">
            <div className="text-center">
              <div className="text-3xl font-bold text-flow-green mb-2">
                {formatDuration(insights.time_tracking_insights.total_tracked_time)}
              </div>
              <p className="text-flow-gray">Total Focus Time</p>
            </div>
          </div>
          
          <div className="flow-card">
            <div className="text-center">
              <div className="text-3xl font-bold text-flow-purple mb-2">
                {formatDuration(Math.round(insights.time_tracking_insights.average_daily_time))}
              </div>
              <p className="text-flow-gray">Daily Average</p>
            </div>
          </div>
        </div>
      )}

      {/* Patterns Section */}
      {patterns?.patterns && Object.keys(patterns.patterns).length > 0 ? (
        <div>
          <h2 className="text-xl font-semibold text-flow-dark mb-4">Productivity Patterns</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {Object.entries(patterns.patterns).map(([name, pattern]) => (
              <PatternCard key={name} name={name} pattern={pattern} />
            ))}
          </div>
        </div>
      ) : patterns?.message ? (
        <div className="flow-card border-2 border-dashed border-gray-300">
          <div className="text-center py-8">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-flow-blue bg-opacity-10 mb-4">
              <span className="text-2xl">📊</span>
            </div>
            <h3 className="text-lg font-medium text-flow-dark mb-2">Building Pattern Intelligence</h3>
            <p className="text-flow-gray mb-2">{patterns.message}</p>
            <p className="text-sm text-flow-gray">
              You need {patterns.required_sessions} sessions total. 
              Current: {patterns.current_sessions}
            </p>
          </div>
        </div>
      ) : null}

      {/* AI Insights */}
      {insights?.ai_insights && insights.ai_insights.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold text-flow-dark mb-4">AI Observations</h2>
          <div className="space-y-4">
            {insights.ai_insights.map((insight, index) => (
              <InsightCard key={index} insight={insight} index={index} />
            ))}
          </div>
        </div>
      )}

      {/* Integration Insights */}
      {insights?.integration_insights && insights.integration_insights.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold text-flow-dark mb-4">Data Quality & Insights</h2>
          <div className="space-y-4">
            {insights.integration_insights.map((insight, index) => (
              <div key={index} className="flow-card">
                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-flow-green bg-opacity-10 rounded-lg flex items-center justify-center">
                      <span className="text-flow-green">✅</span>
                    </div>
                  </div>
                  <div>
                    <h4 className="font-medium text-flow-dark mb-1">{insight.type.replace(/_/g, ' ').toUpperCase()}</h4>
                    <p className="text-flow-gray mb-2">{insight.description}</p>
                    <p className="text-sm text-flow-gray">{insight.guidance}</p>
                    {insight.user_action && (
                      <p className="text-sm font-medium text-flow-blue mt-2">
                        💡 {insight.user_action}
                      </p>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Next Steps */}
      {insights?.next_steps && insights.next_steps.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold text-flow-dark mb-4">Suggested Next Steps</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {insights.next_steps.map((step, index) => (
              <div key={index} className="flow-card">
                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-flow-blue bg-opacity-10 rounded-lg flex items-center justify-center">
                      <span className="text-flow-blue">🎯</span>
                    </div>
                  </div>
                  <div>
                    <h4 className="font-medium text-flow-dark mb-1">{step.title}</h4>
                    <p className="text-sm text-flow-gray mb-2">{step.description}</p>
                    <p className="text-xs text-flow-gray">{step.rationale}</p>
                    {step.action && (
                      <p className="text-sm font-medium text-flow-blue mt-2">
                        → {step.action}
                      </p>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Limitations and Transparency */}
      <div className="flow-card bg-yellow-50 border border-yellow-200">
        <div className="flex items-start space-x-3">
          <div className="flex-shrink-0">
            <div className="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
              <span className="text-yellow-600">⚠️</span>
            </div>
          </div>
          <div>
            <h4 className="font-medium text-flow-dark mb-2">Understanding Your Analytics</h4>
            <div className="text-sm text-flow-gray space-y-1">
              <p>• All insights are based on your tracked data and may not capture your full productivity picture</p>
              <p>• Patterns may change with life circumstances, work changes, or personal growth</p>
              <p>• You are the expert on your own productivity - use insights as starting points for reflection</p>
              <p>• Individual context and external factors are not fully captured in the data</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;