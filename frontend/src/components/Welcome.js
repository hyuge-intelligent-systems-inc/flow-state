import React, { useState } from 'react';
import { apiService } from '../services/api';

const Welcome = ({ onUserLogin }) => {
  const [isCreatingUser, setIsCreatingUser] = useState(false);
  const [username, setUsername] = useState('');
  const [error, setError] = useState('');

  const handleCreateUser = async (e) => {
    e.preventDefault();
    if (!username.trim()) {
      setError('Please enter a username');
      return;
    }

    setIsCreatingUser(true);
    setError('');

    try {
      const userData = await apiService.createUser(username.trim());
      onUserLogin(userData);
    } catch (error) {
      setError('Failed to create user. Please try again.');
      console.error('Error creating user:', error);
    } finally {
      setIsCreatingUser(false);
    }
  };

  const handleCreateDemo = async () => {
    setIsCreatingUser(true);
    setError('');

    try {
      const demoUser = await apiService.createSampleUser();
      onUserLogin(demoUser);
    } catch (error) {
      setError('Failed to create demo user. Please try again.');
      console.error('Error creating demo user:', error);
    } finally {
      setIsCreatingUser(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-flow-blue to-flow-purple flex items-center justify-center px-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-2xl p-8">
        <div className="text-center mb-8">
          <div className="flow-gradient w-16 h-16 rounded-full mx-auto mb-4 flex items-center justify-center">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                    d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-flow-dark mb-2">FlowState</h1>
          <p className="text-flow-gray text-sm">
            Human-Centered Productivity Intelligence
          </p>
        </div>

        <div className="mb-6 p-4 bg-flow-light rounded-lg">
          <h3 className="font-semibold text-flow-dark mb-2">The Philosophy</h3>
          <p className="text-sm text-flow-gray">
            Most productivity apps assume you need to be optimized. 
            FlowState assumes you need to be understood.
          </p>
        </div>

        <form onSubmit={handleCreateUser} className="space-y-4">
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-flow-dark mb-2">
              Choose a username to get started
            </label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
              className="flow-input"
              disabled={isCreatingUser}
            />
          </div>

          {error && (
            <div className="p-3 bg-red-100 border border-red-300 rounded-lg text-red-700 text-sm">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={isCreatingUser}
            className="w-full flow-button-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isCreatingUser ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Creating...
              </span>
            ) : (
              'Start Your Journey'
            )}
          </button>
        </form>

        <div className="mt-6 pt-6 border-t border-gray-200">
          <p className="text-center text-sm text-flow-gray mb-4">
            Want to see FlowState in action?
          </p>
          <button
            onClick={handleCreateDemo}
            disabled={isCreatingUser}
            className="w-full flow-button-secondary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Try Demo with Sample Data
          </button>
        </div>

        <div className="mt-6 text-center">
          <p className="text-xs text-flow-gray">
            ✨ Privacy-first • 🔒 Your data, your control • 🚀 Progressive complexity
          </p>
        </div>
      </div>
    </div>
  );
};

export default Welcome;