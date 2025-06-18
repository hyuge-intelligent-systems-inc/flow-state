import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

const TimeTracker = ({ user }) => {
  const [currentSession, setCurrentSession] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionForm, setSessionForm] = useState({
    task_description: '',
    category: 'work',
    estimated_minutes: '',
    energy_level: 3
  });
  const [endSessionForm, setEndSessionForm] = useState({
    user_notes: '',
    energy_level: 3,
    focus_quality: 3,
    interruptions: 0,
    satisfaction: 3
  });

  const categories = [
    { value: 'work', label: 'Work', icon: '💼' },
    { value: 'learning', label: 'Learning', icon: '📚' },
    { value: 'planning', label: 'Planning', icon: '📋' },
    { value: 'admin', label: 'Admin', icon: '📄' },
    { value: 'meeting', label: 'Meeting', icon: '👥' },
    { value: 'creative', label: 'Creative', icon: '🎨' },
    { value: 'break', label: 'Break', icon: '☕' },
    { value: 'personal', label: 'Personal', icon: '🏠' }
  ];

  useEffect(() => {
    loadCurrentSession();
    
    // Poll for session updates
    const interval = setInterval(loadCurrentSession, 10000);
    return () => clearInterval(interval);
  }, [user]);

  const loadCurrentSession = async () => {
    try {
      const sessionData = await apiService.getCurrentSession(user.user_id);
      setCurrentSession(sessionData.active_session ? sessionData.session : null);
    } catch (error) {
      console.error('Error loading current session:', error);
    }
  };

  const handleStartSession = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const sessionData = {
        task_description: sessionForm.task_description,
        category: sessionForm.category,
        estimated_minutes: sessionForm.estimated_minutes ? parseInt(sessionForm.estimated_minutes) : null,
        energy_level: sessionForm.energy_level
      };

      await apiService.startSession(user.user_id, sessionData);
      await loadCurrentSession();
      
      // Reset form
      setSessionForm({
        task_description: '',
        category: 'work',
        estimated_minutes: '',
        energy_level: 3
      });
    } catch (error) {
      console.error('Error starting session:', error);
      alert('Failed to start session. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleEndSession = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      await apiService.endSession(user.user_id, endSessionForm);
      await loadCurrentSession();
      
      // Reset end session form
      setEndSessionForm({
        user_notes: '',
        energy_level: 3,
        focus_quality: 3,
        interruptions: 0,
        satisfaction: 3
      });
    } catch (error) {
      console.error('Error ending session:', error);
      alert('Failed to end session. Please try again.');
    } finally {
      setIsLoading(false);
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

  const getSelectedCategory = (value) => {
    return categories.find(cat => cat.value === value) || categories[0];
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-flow-dark">Time Tracker</h1>
        <p className="text-flow-gray mt-2">
          Track your focused work sessions with honest self-assessment
        </p>
      </div>

      {/* Current Session Display */}
      {currentSession ? (
        <div className="flow-card bg-gradient-to-r from-flow-blue to-flow-purple text-white">
          <div className="text-center">
            <div className="text-6xl font-bold session-timer session-active mb-4">
              {formatDuration(currentSession.duration_minutes)}
            </div>
            
            <h3 className="text-xl font-semibold mb-2">
              {currentSession.task || 'Active Session'}
            </h3>
            
            <div className="flex justify-center items-center space-x-4 text-blue-100 mb-6">
              <span>{getSelectedCategory(currentSession.category).icon} {getSelectedCategory(currentSession.category).label}</span>
              <span>•</span>
              <span>Started at {formatTime(currentSession.start_time)}</span>
              <span>•</span>
              <span>{currentSession.confidence} confidence</span>
            </div>

            {/* End Session Form */}
            <form onSubmit={handleEndSession} className="bg-white bg-opacity-20 backdrop-blur-sm rounded-lg p-6 text-left">
              <h4 className="text-lg font-semibold mb-4 text-center">End Session</h4>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <label className="block text-sm font-medium mb-2">
                    Focus Quality (1-5)
                  </label>
                  <select
                    value={endSessionForm.focus_quality}
                    onChange={(e) => setEndSessionForm(prev => ({
                      ...prev, 
                      focus_quality: parseInt(e.target.value)
                    }))}
                    className="w-full px-3 py-2 rounded-lg text-flow-dark border-0 focus:ring-2 focus:ring-white"
                  >
                    <option value={1}>1 - Very Poor</option>
                    <option value={2}>2 - Poor</option>
                    <option value={3}>3 - Average</option>
                    <option value={4}>4 - Good</option>
                    <option value={5}>5 - Excellent</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">
                    Energy Level (1-5)
                  </label>
                  <select
                    value={endSessionForm.energy_level}
                    onChange={(e) => setEndSessionForm(prev => ({
                      ...prev, 
                      energy_level: parseInt(e.target.value)
                    }))}
                    className="w-full px-3 py-2 rounded-lg text-flow-dark border-0 focus:ring-2 focus:ring-white"
                  >
                    <option value={1}>1 - Very Low</option>
                    <option value={2}>2 - Low</option>
                    <option value={3}>3 - Moderate</option>
                    <option value={4}>4 - High</option>
                    <option value={5}>5 - Very High</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">
                    Interruptions
                  </label>
                  <input
                    type="number"
                    min="0"
                    value={endSessionForm.interruptions}
                    onChange={(e) => setEndSessionForm(prev => ({
                      ...prev, 
                      interruptions: parseInt(e.target.value) || 0
                    }))}
                    className="w-full px-3 py-2 rounded-lg text-flow-dark border-0 focus:ring-2 focus:ring-white"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">
                    Satisfaction (1-5)
                  </label>
                  <select
                    value={endSessionForm.satisfaction}
                    onChange={(e) => setEndSessionForm(prev => ({
                      ...prev, 
                      satisfaction: parseInt(e.target.value)
                    }))}
                    className="w-full px-3 py-2 rounded-lg text-flow-dark border-0 focus:ring-2 focus:ring-white"
                  >
                    <option value={1}>1 - Very Unsatisfied</option>
                    <option value={2}>2 - Unsatisfied</option>
                    <option value={3}>3 - Neutral</option>
                    <option value={4}>4 - Satisfied</option>
                    <option value={5}>5 - Very Satisfied</option>
                  </select>
                </div>
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium mb-2">
                  Session Notes (Optional)
                </label>
                <textarea
                  value={endSessionForm.user_notes}
                  onChange={(e) => setEndSessionForm(prev => ({
                    ...prev, 
                    user_notes: e.target.value
                  }))}
                  placeholder="How did this session go? What did you accomplish?"
                  rows={3}
                  className="w-full px-3 py-2 rounded-lg text-flow-dark border-0 focus:ring-2 focus:ring-white resize-none"
                />
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-white text-flow-blue font-semibold py-3 px-4 rounded-lg hover:bg-gray-100 transition-colors duration-200 disabled:opacity-50"
              >
                {isLoading ? 'Ending Session...' : 'End Session'}
              </button>
            </form>
          </div>
        </div>
      ) : (
        /* Start New Session */
        <div className="flow-card">
          <form onSubmit={handleStartSession} className="space-y-6">
            <div>
              <label htmlFor="task" className="block text-sm font-medium text-flow-dark mb-2">
                What are you working on? (Optional)
              </label>
              <input
                id="task"
                type="text"
                value={sessionForm.task_description}
                onChange={(e) => setSessionForm(prev => ({
                  ...prev, 
                  task_description: e.target.value
                }))}
                placeholder="e.g., Writing project proposal, Learning React, Team meeting prep..."
                className="flow-input"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-flow-dark mb-2">
                  Category
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {categories.map((category) => (
                    <button
                      key={category.value}
                      type="button"
                      onClick={() => setSessionForm(prev => ({
                        ...prev, 
                        category: category.value
                      }))}
                      className={`p-3 rounded-lg border-2 transition-all duration-200 ${
                        sessionForm.category === category.value
                          ? 'border-flow-blue bg-flow-blue bg-opacity-10 text-flow-blue'
                          : 'border-gray-200 hover:border-gray-300 text-flow-gray hover:text-flow-dark'
                      }`}
                    >
                      <div className="text-lg mb-1">{category.icon}</div>
                      <div className="text-xs font-medium">{category.label}</div>
                    </button>
                  ))}
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-flow-dark mb-2">
                    Estimated Duration (Optional)
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="480"
                    value={sessionForm.estimated_minutes}
                    onChange={(e) => setSessionForm(prev => ({
                      ...prev, 
                      estimated_minutes: e.target.value
                    }))}
                    placeholder="Minutes"
                    className="flow-input"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-flow-dark mb-2">
                    Current Energy Level (1-5)
                  </label>
                  <select
                    value={sessionForm.energy_level}
                    onChange={(e) => setSessionForm(prev => ({
                      ...prev, 
                      energy_level: parseInt(e.target.value)
                    }))}
                    className="flow-input"
                  >
                    <option value={1}>1 - Very Low</option>
                    <option value={2}>2 - Low</option>
                    <option value={3}>3 - Moderate</option>
                    <option value={4}>4 - High</option>
                    <option value={5}>5 - Very High</option>
                  </select>
                </div>
              </div>
            </div>

            <div className="pt-4 border-t border-gray-200">
              <button
                type="submit"
                disabled={isLoading}
                className="w-full flow-button-primary text-lg py-4 disabled:opacity-50"
              >
                {isLoading ? (
                  <span className="flex items-center justify-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Starting Session...
                  </span>
                ) : (
                  '🚀 Start Focus Session'
                )}
              </button>
            </div>
          </form>

          <div className="mt-6 p-4 bg-flow-light rounded-lg">
            <h4 className="text-sm font-semibold text-flow-dark mb-2">💡 FlowState Philosophy</h4>
            <p className="text-xs text-flow-gray">
              FlowState believes in honest self-assessment over perfect metrics. 
              Track what feels authentic to your work style and circumstances.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default TimeTracker;