import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';

// Import components
import Layout from './components/Layout';
import Dashboard from './components/Dashboard';
import TimeTracker from './components/TimeTracker';
import Analytics from './components/Analytics';
import Profile from './components/Profile';
import Welcome from './components/Welcome';

// API service
import { apiService } from './services/api';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    initializeApp();
  }, []);

  const initializeApp = async () => {
    // Check if we have a user in localStorage
    const storedUserId = localStorage.getItem('flowstate_user_id');
    
    if (storedUserId) {
      try {
        const userData = await apiService.getUser(storedUserId);
        setUser(userData);
      } catch (error) {
        console.error('Error loading user:', error);
        localStorage.removeItem('flowstate_user_id');
      }
    }
    
    setLoading(false);
  };

  const handleUserLogin = (userData) => {
    setUser(userData);
    localStorage.setItem('flowstate_user_id', userData.user_id);
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('flowstate_user_id');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-flow-light flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-flow-blue mx-auto mb-4"></div>
          <p className="text-flow-gray">Loading FlowState...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return <Welcome onUserLogin={handleUserLogin} />;
  }

  return (
    <Router>
      <Layout user={user} onLogout={handleLogout}>
        <Routes>
          <Route path="/" element={<Dashboard user={user} />} />
          <Route path="/dashboard" element={<Dashboard user={user} />} />
          <Route path="/track" element={<TimeTracker user={user} />} />
          <Route path="/analytics" element={<Analytics user={user} />} />
          <Route path="/profile" element={<Profile user={user} />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;