import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { apiService } from '../services/api';

const Dashboard = ({ user }) => {
  const [currentSession, setCurrentSession] = useState(null);
  const [dailySummary, setDailySummary] = useState(null);
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
    
    // Set up polling for current session
    const interval = setInterval(loadCurrentSession, 5000);
    return () => clearInterval(interval);
  }, [user]);

  const loadDashboardData = async () => {
    try {
      await Promise.all([
        loadCurrentSession(),
        loadDailySummary(),
        loadInsights()
      ]);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadCurrentSession = async () => {
    try {
      const sessionData = await apiService.getActiveSessions(user.user_id);
      setCurrentSession(sessionData.active_sessions && sessionData.active_sessions.length > 0 ? {
        active_sessions: sessionData.active_sessions,
        count: sessionData.count
      } : null);
    } catch (error) {
      console.error('Error loading current session:', error);
    }
  };

  const loadDailySummary = async () => {
    try {
      const summary = await apiService.getDailySummary(user.user_id);
      setDailySummary(summary);
    } catch (error) {
      console.error('Error loading daily summary:', error);
    }
  };

  const loadInsights = async () => {
    try {
      const insightsData = await apiService.getInsights(user.user_id, 7);
      setInsights(insightsData);
    } catch (error) {
      console.error('Error loading insights:', error);
    }
  };

  const formatDuration = (minutes) => {
    if (!minutes) return '0m';
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
  };

  const formatTime = (dateString) => {
    return new Date(dateString).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

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
          <h1 className="text-2xl font-bold text-flow-dark">
            Welcome back, {user.username}! 
          </h1>
          <p className="text-flow-gray mt-1">
            {new Date().toLocaleDateString('en-US', { 
              weekday: 'long', 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric' 
            })}
          </p>
        </div>
        
        <Link 
          to="/track" 
          className="flow-button-primary"
        >
          {currentSession ? 'Continue Session' : 'Start Tracking'}
        </Link>
      </div>

      {/* Active Sessions */}
      {currentSession && (
        <div className="flow-card bg-gradient-to-r from-flow-blue to-flow-purple text-white">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-lg font-semibold">Active Sessions ({currentSession.count})</h3>
              <p className="text-blue-100">Multiple activities running simultaneously</p>
            </div>
            <Link 
              to="/track" 
              className="bg-white bg-opacity-20 hover:bg-opacity-30 text-white px-4 py-2 rounded-lg transition-colors duration-200"
            >
              Manage Sessions
            </Link>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {currentSession.active_sessions.slice(0, 4).map((session) => (
              <div key={session.session_id} className="bg-white bg-opacity-10 backdrop-blur-sm rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <div className="text-sm font-medium">{session.tag}</div>
                  <div className="text-xs text-blue-200">
                    {formatDuration(session.duration_minutes)}
                  </div>
                </div>
                <div className="text-xs text-blue-100 mb-2">
                  {session.task || 'Working...'}
                </div>
                <div className="flex justify-between text-xs text-blue-200">
                  <span>Started: {formatTime(session.start_time)}</span>
                  <span>Energy: {session.energy_level}/5</span>
                </div>
              </div>
            ))}
            
            {currentSession.count > 4 && (
              <div className="bg-white bg-opacity-10 backdrop-blur-sm rounded-lg p-4 flex items-center justify-center">
                <div className="text-center text-blue-100">
                  <div className="text-lg font-semibold">+{currentSession.count - 4}</div>
                  <div className="text-xs">more sessions</div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="flow-card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-flow-blue bg-opacity-10 rounded-lg flex items-center justify-center">
                <span className="text-flow-blue">⏱️</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-flow-gray">Today's Focus Time</p>
              <p className="text-2xl font-bold text-flow-dark">
                {formatDuration(dailySummary?.total_minutes || 0)}
              </p>
            </div>
          </div>
        </div>

        <div className="flow-card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-flow-green bg-opacity-10 rounded-lg flex items-center justify-center">
                <span className="text-flow-green">📊</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-flow-gray">Sessions</p>
              <p className="text-2xl font-bold text-flow-dark">
                {dailySummary?.entries_count || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="flow-card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-flow-purple bg-opacity-10 rounded-lg flex items-center justify-center">
                <span className="text-flow-purple">⚡</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-flow-gray">Avg Energy</p>
              <p className="text-2xl font-bold text-flow-dark">
                {dailySummary?.average_energy ? 
                  `${dailySummary.average_energy.toFixed(1)}/5` : 'N/A'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Today's Activity */}
      {dailySummary?.categories && Object.keys(dailySummary.categories).length > 0 && (
        <div className="flow-card">
          <h3 className="text-lg font-semibold text-flow-dark mb-4">Today's Activity</h3>
          <div className="space-y-3">
            {Object.entries(dailySummary.categories)
              .sort(([,a], [,b]) => b - a)
              .map(([category, minutes]) => (
                <div key={category} className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="w-3 h-3 bg-flow-blue rounded-full mr-3"></div>
                    <span className="text-flow-dark capitalize">{category}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-flow-gray">{formatDuration(minutes)}</span>
                    <div className="w-20 bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-flow-blue h-2 rounded-full" 
                        style={{ 
                          width: `${Math.min(100, (minutes / (dailySummary.total_minutes || 1)) * 100)}%` 
                        }}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}
          </div>
        </div>
      )}

      {/* Insights */}
      {insights?.time_tracking_insights?.active_days > 0 && (
        <div className="flow-card insight-card">
          <h3 className="text-lg font-semibold text-flow-dark mb-4">Recent Insights</h3>
          
          <div className="space-y-4">
            <div className="p-4 bg-flow-light rounded-lg">
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-flow-blue bg-opacity-10 rounded-lg flex items-center justify-center">
                    <span className="text-flow-blue">📈</span>
                  </div>
                </div>
                <div className="ml-3">
                  <h4 className="text-sm font-medium text-flow-dark">Weekly Progress</h4>
                  <p className="text-sm text-flow-gray mt-1">
                    You've been active for {insights.time_tracking_insights.active_days} days 
                    with an average of {Math.round(insights.time_tracking_insights.average_daily_time)} 
                    minutes of focused work per day.
                  </p>
                </div>
              </div>
            </div>

            {insights.ai_insights && insights.ai_insights.length > 0 && (
              <div className="p-4 bg-flow-light rounded-lg">
                <div className="flex items-start">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-flow-purple bg-opacity-10 rounded-lg flex items-center justify-center">
                      <span className="text-flow-purple">🧠</span>
                    </div>
                  </div>
                  <div className="ml-3">
                    <h4 className="text-sm font-medium text-flow-dark">AI Observation</h4>
                    <p className="text-sm text-flow-gray mt-1">
                      {insights.ai_insights[0].description}
                    </p>
                    <p className="text-xs text-flow-gray mt-2">
                      Confidence: {insights.ai_insights[0].confidence}
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="mt-4 pt-4 border-t border-gray-200">
            <Link 
              to="/analytics" 
              className="text-sm text-flow-blue hover:text-blue-600 font-medium"
            >
              View detailed analytics →
            </Link>
          </div>
        </div>
      )}

      {/* Getting Started */}
      {(!dailySummary || dailySummary.entries_count === 0) && (
        <div className="flow-card border-2 border-dashed border-gray-300">
          <div className="text-center">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-flow-blue bg-opacity-10">
              <span className="text-2xl">🚀</span>
            </div>
            <h3 className="mt-2 text-sm font-medium text-flow-dark">Start Your First Session</h3>
            <p className="mt-1 text-sm text-flow-gray">
              Begin tracking your productivity to unlock insights and patterns.
            </p>
            <div className="mt-6">
              <Link to="/track" className="flow-button-primary">
                Start Time Tracking
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;