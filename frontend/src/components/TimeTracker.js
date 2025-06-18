import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

const TimeTracker = ({ user }) => {
  const [activeSessions, setActiveSessions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState(null);
  const [sessionForm, setSessionForm] = useState({
    task_description: '',
    main_tag: '',
    sub_tag: '',
    estimated_minutes: '',
    energy_level: 3
  });
  const [endSessionForm, setEndSessionForm] = useState({
    session_id: '',
    user_notes: '',
    energy_level: 3,
    focus_quality: 3,
    interruptions: 0,
    satisfaction: 3
  });
  const [userTags, setUserTags] = useState([]);

  const commonTags = [
    { main: 'work', subs: ['client-project', 'meetings', 'planning', 'coding', 'review'] },
    { main: 'learning', subs: ['tutorial', 'reading', 'course', 'practice', 'research'] },
    { main: 'exercise', subs: ['cardio', 'strength', 'yoga', 'walking', 'sports'] },
    { main: 'creative', subs: ['writing', 'design', 'art', 'music', 'brainstorming'] },
    { main: 'admin', subs: ['email', 'paperwork', 'organizing', 'scheduling', 'bills'] },
    { main: 'wellness', subs: ['meditation', 'break', 'therapy', 'self-care', 'reflection'] },
    { main: 'social', subs: ['family', 'friends', 'networking', 'community', 'calls'] },
    { main: 'personal', subs: ['errands', 'chores', 'shopping', 'cooking', 'cleaning'] }
  ];

  useEffect(() => {
    loadActiveSessions();
    loadUserTags();
    initializeSpeechRecognition();
    
    // Poll for session updates
    const interval = setInterval(loadActiveSessions, 10000);
    return () => clearInterval(interval);
  }, [user]);

  const initializeSpeechRecognition = () => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognitionInstance = new SpeechRecognition();
      
      recognitionInstance.continuous = false; // Change to false for better command recognition
      recognitionInstance.interimResults = false; // Change to false to get final results only
      recognitionInstance.lang = 'en-US';
      recognitionInstance.maxAlternatives = 1;
      
      recognitionInstance.onresult = (event) => {
        const transcript = event.results[0][0].transcript.toLowerCase().trim();
        console.log('Voice command received:', transcript);
        processVoiceCommand(transcript);
      };
      
      recognitionInstance.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
        
        // Provide user feedback based on error type
        if (event.error === 'no-speech') {
          alert('No speech detected. Please try again.');
        } else if (event.error === 'not-allowed') {
          alert('Microphone access denied. Please allow microphone access to use voice commands.');
        }
      };
      
      recognitionInstance.onend = () => {
        setIsListening(false);
      };
      
      recognitionInstance.onstart = () => {
        console.log('Speech recognition started');
      };
      
      setRecognition(recognitionInstance);
    }
  };

  const processVoiceCommand = (command) => {
    console.log('Processing voice command:', command);
    
    // Check for start command first
    if (command.includes('start') || command.includes('begin') || command === 'go') {
      if (sessionForm.main_tag.trim()) {
        console.log('Starting session via voice command');
        handleStartSession();
        return;
      } else {
        alert('Please set a main tag first before starting a session');
        return;
      }
    }
    
    // Parse tag commands - look for patterns like "work client project" or "learning react tutorial"
    const words = command.split(' ').filter(word => word.length > 0);
    
    if (words.length >= 1) {
      const mainTag = words[0];
      const subTagWords = words.slice(1);
      const subTag = subTagWords.length > 0 ? subTagWords.join('-') : '';
      
      console.log('Parsed tags:', { mainTag, subTag });
      
      // Validate main tag against known tags or common tags
      const isValidMainTag = 
        userTags.some(tag => tag.toLowerCase().includes(mainTag.toLowerCase())) || 
        commonTags.some(tag => tag.main.toLowerCase().includes(mainTag.toLowerCase())) ||
        ['work', 'learning', 'exercise', 'creative', 'admin', 'wellness', 'social', 'personal'].includes(mainTag.toLowerCase());
      
      if (isValidMainTag || words.length >= 2) { // Accept if valid or if there are multiple words
        setSessionForm(prev => ({
          ...prev,
          main_tag: mainTag.toLowerCase(),
          sub_tag: subTag.toLowerCase()
        }));
        
        // Provide feedback to user
        const tagDisplay = subTag ? `#${mainTag}/${subTag}` : `#${mainTag}`;
        console.log('Tags set via voice:', tagDisplay);
        
        // Auto-start after a brief delay if the form is ready
        setTimeout(() => {
          if (sessionForm.main_tag || mainTag) {
            console.log('Tags set. Say "start" to begin the session.');
          }
        }, 500);
      } else {
        console.log('Unrecognized voice command:', command);
      }
    }
  };

  const toggleVoiceRecognition = () => {
    if (!recognition) {
      alert('Speech recognition is not supported in your browser. Please use Chrome, Edge, or Safari.');
      return;
    }
    
    if (isListening) {
      recognition.stop();
      setIsListening(false);
    } else {
      try {
        recognition.start();
        setIsListening(true);
      } catch (error) {
        console.error('Failed to start speech recognition:', error);
        alert('Failed to start voice recognition. Please check your microphone permissions.');
      }
    }
  };

  const loadActiveSessions = async () => {
    try {
      const data = await apiService.getActiveSessions(user.user_id);
      setActiveSessions(data.active_sessions || []);
    } catch (error) {
      console.error('Error loading active sessions:', error);
    }
  };

  const loadUserTags = async () => {
    try {
      const data = await apiService.getUserTags(user.user_id);
      setUserTags(data.user_tags || []);
    } catch (error) {
      console.error('Error loading user tags:', error);
    }
  };

  const handleStartSession = async (e = null) => {
    if (e) e.preventDefault();
    if (!sessionForm.main_tag.trim()) {
      alert('Please enter a main tag (e.g., work, learning, exercise)');
      return;
    }

    setIsLoading(true);

    try {
      const sessionData = {
        task_description: sessionForm.task_description,
        main_tag: sessionForm.main_tag.toLowerCase().trim(),
        sub_tag: sessionForm.sub_tag ? sessionForm.sub_tag.toLowerCase().trim() : null,
        estimated_minutes: sessionForm.estimated_minutes ? parseInt(sessionForm.estimated_minutes) : null,
        energy_level: sessionForm.energy_level
      };

      await apiService.startSession(user.user_id, sessionData);
      await loadActiveSessions();
      await loadUserTags();
      
      // Reset form
      setSessionForm({
        task_description: '',
        main_tag: '',
        sub_tag: '',
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
    if (!endSessionForm.session_id) {
      alert('Please select a session to end');
      return;
    }

    setIsLoading(true);

    try {
      await apiService.endSession(user.user_id, endSessionForm);
      await loadActiveSessions();
      
      // Reset end session form
      setEndSessionForm({
        session_id: '',
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

  const quickSelectTag = (main, sub = '') => {
    setSessionForm(prev => ({
      ...prev,
      main_tag: main,
      sub_tag: sub
    }));
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-flow-dark">Multi-Session Time Tracker</h1>
        <p className="text-flow-gray mt-2">
          Track multiple activities simultaneously with your own tags
        </p>
      </div>

      {/* Active Sessions Display */}
      {activeSessions.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-flow-dark">
            Active Sessions ({activeSessions.length})
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {activeSessions.map((session) => (
              <div key={session.session_id} className="flow-card bg-gradient-to-r from-flow-blue to-flow-purple text-white">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <div className="text-lg font-semibold">{session.tag}</div>
                    <div className="text-sm text-blue-100">{session.task || 'Working...'}</div>
                  </div>
                  <button
                    onClick={() => setEndSessionForm(prev => ({ ...prev, session_id: session.session_id }))}
                    className="text-xs bg-white bg-opacity-20 px-2 py-1 rounded hover:bg-opacity-30 transition-colors"
                  >
                    Select to End
                  </button>
                </div>
                
                <div className="flex justify-between items-end">
                  <div>
                    <div className="text-2xl font-bold session-timer session-active">
                      {formatDuration(session.duration_minutes)}
                    </div>
                    <div className="text-xs text-blue-100">
                      Started {formatTime(session.start_time)}
                    </div>
                  </div>
                  <div className="text-right text-xs text-blue-100">
                    Energy: {session.energy_level}/5
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Voice Control */}
      <div className="flow-card bg-purple-50 border border-purple-200">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-purple-900">Voice Control</h3>
            <p className="text-sm text-purple-700 mt-1">
              Say your tag and sub-tag, then say "start" to begin tracking
            </p>
            <p className="text-xs text-purple-600 mt-1">
              Example: "work client project" then "start"
            </p>
          </div>
          <button
            onClick={toggleVoiceRecognition}
            className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
              isListening 
                ? 'bg-red-500 text-white hover:bg-red-600' 
                : 'bg-purple-500 text-white hover:bg-purple-600'
            }`}
          >
            {isListening ? 'Stop Listening' : 'Start Voice Control'}
          </button>
        </div>
        {isListening && (
          <div className="mt-3 p-3 bg-purple-100 rounded-lg">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
              <span className="text-sm text-purple-800">Listening for voice commands...</span>
            </div>
          </div>
        )}
      </div>

      {/* Start New Session */}
      <div className="flow-card">
        <h2 className="text-xl font-semibold text-flow-dark mb-4">Start New Session</h2>
        
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
              placeholder="e.g., Building new feature, Learning React hooks, Morning workout..."
              className="flow-input"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-flow-dark mb-2">
                Main Tag * (e.g., work, learning, exercise)
              </label>
              <input
                type="text"
                value={sessionForm.main_tag}
                onChange={(e) => setSessionForm(prev => ({
                  ...prev, 
                  main_tag: e.target.value
                }))}
                placeholder="work"
                className="flow-input mb-2"
                list="main-tags"
                required
              />
              <datalist id="main-tags">
                {userTags.map(tag => (
                  <option key={tag} value={tag} />
                ))}
                {commonTags.map(tag => (
                  <option key={tag.main} value={tag.main} />
                ))}
              </datalist>
              
              <label className="block text-sm font-medium text-flow-dark mb-2 mt-4">
                Sub Tag (Optional additional detail)
              </label>
              <input
                type="text"
                value={sessionForm.sub_tag}
                onChange={(e) => setSessionForm(prev => ({
                  ...prev, 
                  sub_tag: e.target.value
                }))}
                placeholder="client-project"
                className="flow-input"
                list="sub-tags"
              />
              <datalist id="sub-tags">
                {commonTags.find(t => t.main === sessionForm.main_tag)?.subs.map(sub => (
                  <option key={sub} value={sub} />
                ))}
              </datalist>
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

          {/* Quick Tag Selection */}
          <div>
            <label className="block text-sm font-medium text-flow-dark mb-2">
              Quick Tag Selection
            </label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
              {commonTags.slice(0, 8).map((tagGroup) => (
                <button
                  key={tagGroup.main}
                  type="button"
                  onClick={() => quickSelectTag(tagGroup.main)}
                  className={`p-2 rounded-lg border-2 transition-all duration-200 text-sm ${
                    sessionForm.main_tag === tagGroup.main
                      ? 'border-flow-blue bg-flow-blue bg-opacity-10 text-flow-blue'
                      : 'border-gray-200 hover:border-gray-300 text-flow-gray hover:text-flow-dark'
                  }`}
                >
                  #{tagGroup.main}
                </button>
              ))}
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
                'Start New Session'
              )}
            </button>
          </div>
        </form>
      </div>

      {/* End Session */}
      {activeSessions.length > 0 && (
        <div className="flow-card">
          <h2 className="text-xl font-semibold text-flow-dark mb-4">End Session</h2>
          
          <form onSubmit={handleEndSession} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-flow-dark mb-2">
                Select Session to End
              </label>
              <select
                value={endSessionForm.session_id}
                onChange={(e) => setEndSessionForm(prev => ({
                  ...prev, 
                  session_id: e.target.value
                }))}
                className="flow-input"
                required
              >
                <option value="">Choose a session...</option>
                {activeSessions.map((session) => (
                  <option key={session.session_id} value={session.session_id}>
                    {session.tag} - {session.task || 'No description'} ({formatDuration(session.duration_minutes)})
                  </option>
                ))}
              </select>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-flow-dark mb-2">
                  Focus Quality (1-5)
                </label>
                <select
                  value={endSessionForm.focus_quality}
                  onChange={(e) => setEndSessionForm(prev => ({
                    ...prev, 
                    focus_quality: parseInt(e.target.value)
                  }))}
                  className="flow-input"
                >
                  <option value={1}>1 - Very Poor</option>
                  <option value={2}>2 - Poor</option>
                  <option value={3}>3 - Average</option>
                  <option value={4}>4 - Good</option>
                  <option value={5}>5 - Excellent</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-flow-dark mb-2">
                  Energy Level (1-5)
                </label>
                <select
                  value={endSessionForm.energy_level}
                  onChange={(e) => setEndSessionForm(prev => ({
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

              <div>
                <label className="block text-sm font-medium text-flow-dark mb-2">
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
                  className="flow-input"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-flow-dark mb-2">
                  Satisfaction (1-5)
                </label>
                <select
                  value={endSessionForm.satisfaction}
                  onChange={(e) => setEndSessionForm(prev => ({
                    ...prev, 
                    satisfaction: parseInt(e.target.value)
                  }))}
                  className="flow-input"
                >
                  <option value={1}>1 - Very Unsatisfied</option>
                  <option value={2}>2 - Unsatisfied</option>
                  <option value={3}>3 - Neutral</option>
                  <option value={4}>4 - Satisfied</option>
                  <option value={5}>5 - Very Satisfied</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-flow-dark mb-2">
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
                className="flow-input resize-none"
              />
            </div>

            <button
              type="submit"
              disabled={isLoading || !endSessionForm.session_id}
              className="w-full flow-button-primary disabled:opacity-50"
            >
              {isLoading ? 'Ending Session...' : 'End Selected Session'}
            </button>
          </form>
        </div>
      )}

      <div className="flow-card bg-blue-50 border border-blue-200">
        <div className="flex items-start space-x-3">
          <div className="flex-shrink-0">
            <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
              <span className="text-blue-600">i</span>
            </div>
          </div>
          <div>
            <h4 className="font-medium text-blue-900 mb-2">Enhanced Multi-Session Tracking</h4>
            <div className="text-sm text-blue-800 space-y-1">
              <p><strong>Multiple Sessions:</strong> Track different activities simultaneously</p>
              <p><strong>Your Tags:</strong> Create hashtag-like categories that make sense to you</p>
              <p><strong>Flexible Structure:</strong> Main tag + optional sub-tag (e.g., #work/client-project)</p>
              <p><strong>Voice Control:</strong> Use voice commands to set tags and start sessions</p>
              <p><strong>Real Work Patterns:</strong> Reflects how people actually multitask</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TimeTracker;