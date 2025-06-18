import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

const Profile = ({ user }) => {
  const [profileData, setProfileData] = useState(null);
  const [preferences, setPreferences] = useState({
    accessibility_prefs: {},
    productivity_prefs: {},
    privacy_settings: {}
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    loadProfileData();
  }, [user]);

  const loadProfileData = async () => {
    try {
      const userData = await apiService.getUser(user.user_id);
      setProfileData(userData);
    } catch (error) {
      console.error('Error loading profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSavePreferences = async () => {
    setSaving(true);
    try {
      await apiService.updateUserPreferences(user.user_id, preferences);
      alert('Preferences updated successfully!');
      await loadProfileData();
    } catch (error) {
      console.error('Error saving preferences:', error);
      alert('Failed to save preferences. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  const handleExportData = async () => {
    try {
      const exportData = await apiService.exportUserData(user.user_id);
      
      // Create and download file
      const dataStr = JSON.stringify(exportData, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `flowstate-data-${user.username}-${new Date().toISOString().split('T')[0]}.json`;
      link.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error exporting data:', error);
      alert('Failed to export data. Please try again.');
    }
  };

  const handleResetDemo = async () => {
    if (!user.is_demo) {
      alert('This feature is only available for demo users.');
      return;
    }

    if (window.confirm('Are you sure you want to reset all demo data? This cannot be undone.')) {
      try {
        await apiService.resetDemoUser(user.user_id);
        alert('Demo data has been reset!');
        window.location.reload();
      } catch (error) {
        console.error('Error resetting demo:', error);
        alert('Failed to reset demo data. Please try again.');
      }
    }
  };

  const tabs = [
    { id: 'overview', name: 'Overview', icon: '👤' },
    { id: 'preferences', name: 'Preferences', icon: '⚙️' },
    { id: 'privacy', name: 'Privacy & Data', icon: '🔒' }
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-flow-blue"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-flow-dark">Profile & Settings</h1>
        <p className="text-flow-gray mt-1">
          Manage your FlowState experience with full control over your data
        </p>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-2 px-1 border-b-2 font-medium text-sm transition-colors duration-200 ${
                activeTab === tab.id
                  ? 'border-flow-blue text-flow-blue'
                  : 'border-transparent text-flow-gray hover:text-flow-dark hover:border-gray-300'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.name}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          {/* User Info */}
          <div className="flow-card">
            <h3 className="text-lg font-semibold text-flow-dark mb-4">User Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-flow-gray mb-1">Username</label>
                <p className="text-flow-dark font-medium">{profileData?.username}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-flow-gray mb-1">User ID</label>
                <p className="text-flow-dark font-mono text-sm">{profileData?.user_id}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-flow-gray mb-1">Member Since</label>
                <p className="text-flow-dark">
                  {new Date(profileData?.created_at).toLocaleDateString()}
                </p>
              </div>
              <div>
                <label className="block text-sm font-medium text-flow-gray mb-1">Account Type</label>
                <p className="text-flow-dark">
                  {user.is_demo ? (
                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                      Demo Account
                    </span>
                  ) : (
                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      Standard Account
                    </span>
                  )}
                </p>
              </div>
            </div>
          </div>

          {/* Usage Stats */}
          <div className="flow-card">
            <h3 className="text-lg font-semibold text-flow-dark mb-4">Usage Statistics</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="text-2xl font-bold text-flow-blue mb-1">
                  {profileData?.profile?.days_active || 0}
                </div>
                <p className="text-sm text-flow-gray">Active Days</p>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-flow-green mb-1">
                  {profileData?.profile?.total_sessions || 0}
                </div>
                <p className="text-sm text-flow-gray">Total Sessions</p>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-flow-purple mb-1">
                  {profileData?.profile?.ui_complexity_level || 1}
                </div>
                <p className="text-sm text-flow-gray">UI Complexity Level</p>
              </div>
            </div>
          </div>

          {/* Productivity Mode */}
          <div className="flow-card">
            <h3 className="text-lg font-semibold text-flow-dark mb-4">Current Productivity Mode</h3>
            <div className="flex items-center space-x-4">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 bg-flow-blue bg-opacity-10 rounded-lg flex items-center justify-center">
                  <span className="text-2xl">
                    {profileData?.profile?.productivity_mode === 'survival' && '🛡️'}
                    {profileData?.profile?.productivity_mode === 'maintenance' && '⚖️'}
                    {profileData?.profile?.productivity_mode === 'growth' && '🌱'}
                    {profileData?.profile?.productivity_mode === 'mastery' && '🎯'}
                  </span>
                </div>
              </div>
              <div>
                <h4 className="font-medium text-flow-dark capitalize">
                  {profileData?.profile?.productivity_mode || 'Not Set'} Mode
                </h4>
                <p className="text-sm text-flow-gray">
                  {profileData?.profile?.productivity_mode === 'survival' && 'Focus on essential tasks only with minimal cognitive load'}
                  {profileData?.profile?.productivity_mode === 'maintenance' && 'Keeping up with regular responsibilities sustainably'}
                  {profileData?.profile?.productivity_mode === 'growth' && 'Actively improving and optimizing productivity'}
                  {profileData?.profile?.productivity_mode === 'mastery' && 'Advanced productivity practices and teaching others'}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'preferences' && (
        <div className="space-y-6">
          <div className="flow-card">
            <h3 className="text-lg font-semibold text-flow-dark mb-4">Accessibility Preferences</h3>
            <div className="space-y-4">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={preferences.accessibility_prefs.high_contrast || false}
                  onChange={(e) => setPreferences(prev => ({
                    ...prev,
                    accessibility_prefs: {
                      ...prev.accessibility_prefs,
                      high_contrast: e.target.checked
                    }
                  }))}
                  className="rounded border-gray-300 text-flow-blue focus:ring-flow-blue focus:ring-offset-0 mr-3"
                />
                <span className="text-flow-dark">High contrast mode</span>
              </label>
              
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={preferences.accessibility_prefs.reduced_motion || false}
                  onChange={(e) => setPreferences(prev => ({
                    ...prev,
                    accessibility_prefs: {
                      ...prev.accessibility_prefs,
                      reduced_motion: e.target.checked
                    }
                  }))}
                  className="rounded border-gray-300 text-flow-blue focus:ring-flow-blue focus:ring-offset-0 mr-3"
                />
                <span className="text-flow-dark">Reduced motion animations</span>
              </label>

              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={preferences.accessibility_prefs.simplified_interface || false}
                  onChange={(e) => setPreferences(prev => ({
                    ...prev,
                    accessibility_prefs: {
                      ...prev.accessibility_prefs,
                      simplified_interface: e.target.checked
                    }
                  }))}
                  className="rounded border-gray-300 text-flow-blue focus:ring-flow-blue focus:ring-offset-0 mr-3"
                />
                <span className="text-flow-dark">Simplified interface</span>
              </label>
            </div>
          </div>

          <div className="flow-card">
            <h3 className="text-lg font-semibold text-flow-dark mb-4">Productivity Preferences</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-flow-gray mb-2">
                  Preferred Session Length (minutes)
                </label>
                <input
                  type="number"
                  min="5"
                  max="240"
                  value={preferences.productivity_prefs.preferred_session_length || 25}
                  onChange={(e) => setPreferences(prev => ({
                    ...prev,
                    productivity_prefs: {
                      ...prev.productivity_prefs,
                      preferred_session_length: parseInt(e.target.value)
                    }
                  }))}
                  className="flow-input"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-flow-gray mb-2">
                  Energy Peak Time
                </label>
                <select
                  value={preferences.productivity_prefs.energy_peak_time || 'morning'}
                  onChange={(e) => setPreferences(prev => ({
                    ...prev,
                    productivity_prefs: {
                      ...prev.productivity_prefs,
                      energy_peak_time: e.target.value
                    }
                  }))}
                  className="flow-input"
                >
                  <option value="morning">Morning</option>
                  <option value="afternoon">Afternoon</option>
                  <option value="evening">Evening</option>
                </select>
              </div>
            </div>

            <div className="mt-4 space-y-4">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={preferences.productivity_prefs.likes_time_blocking || false}
                  onChange={(e) => setPreferences(prev => ({
                    ...prev,
                    productivity_prefs: {
                      ...prev.productivity_prefs,
                      likes_time_blocking: e.target.checked
                    }
                  }))}
                  className="rounded border-gray-300 text-flow-blue focus:ring-flow-blue focus:ring-offset-0 mr-3"
                />
                <span className="text-flow-dark">I like time blocking</span>
              </label>

              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={preferences.productivity_prefs.needs_autonomy_high || false}
                  onChange={(e) => setPreferences(prev => ({
                    ...prev,
                    productivity_prefs: {
                      ...prev.productivity_prefs,
                      needs_autonomy_high: e.target.checked
                    }
                  }))}
                  className="rounded border-gray-300 text-flow-blue focus:ring-flow-blue focus:ring-offset-0 mr-3"
                />
                <span className="text-flow-dark">High autonomy needs</span>
              </label>
            </div>
          </div>

          <div className="flex justify-end">
            <button
              onClick={handleSavePreferences}
              disabled={saving}
              className="flow-button-primary disabled:opacity-50"
            >
              {saving ? 'Saving...' : 'Save Preferences'}
            </button>
          </div>
        </div>
      )}

      {activeTab === 'privacy' && (
        <div className="space-y-6">
          <div className="flow-card">
            <h3 className="text-lg font-semibold text-flow-dark mb-4">Data Ownership & Control</h3>
            <div className="space-y-4">
              <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                <h4 className="font-medium text-green-800 mb-2">✅ Your Data Rights</h4>
                <ul className="text-sm text-green-700 space-y-1">
                  <li>• You own all your productivity data</li>
                  <li>• Full export available at any time</li>
                  <li>• Complete data deletion available</li>
                  <li>• No data sharing without explicit consent</li>
                  <li>• Privacy-first design by default</li>
                </ul>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <button
                  onClick={handleExportData}
                  className="flow-button-secondary text-left p-4"
                >
                  <div className="flex items-center">
                    <span className="text-2xl mr-3">📁</span>
                    <div>
                      <div className="font-medium">Export All Data</div>
                      <div className="text-sm text-flow-gray">Download your complete FlowState data</div>
                    </div>
                  </div>
                </button>

                {user.is_demo && (
                  <button
                    onClick={handleResetDemo}
                    className="flow-button-secondary text-left p-4 border-yellow-300 hover:bg-yellow-50"
                  >
                    <div className="flex items-center">
                      <span className="text-2xl mr-3">🔄</span>
                      <div>
                        <div className="font-medium">Reset Demo Data</div>
                        <div className="text-sm text-flow-gray">Clear all demo data and start fresh</div>
                      </div>
                    </div>
                  </button>
                )}
              </div>
            </div>
          </div>

          <div className="flow-card">
            <h3 className="text-lg font-semibold text-flow-dark mb-4">Privacy Settings</h3>
            <div className="space-y-4">
              <label className="flex items-center justify-between">
                <div>
                  <span className="text-flow-dark font-medium">Local Data Processing</span>
                  <p className="text-sm text-flow-gray">Keep all data processing on your device</p>
                </div>
                <input
                  type="checkbox"
                  checked={preferences.privacy_settings.local_processing_only !== false}
                  onChange={(e) => setPreferences(prev => ({
                    ...prev,
                    privacy_settings: {
                      ...prev.privacy_settings,
                      local_processing_only: e.target.checked
                    }
                  }))}
                  className="rounded border-gray-300 text-flow-blue focus:ring-flow-blue focus:ring-offset-0"
                />
              </label>

              <label className="flex items-center justify-between">
                <div>
                  <span className="text-flow-dark font-medium">Anonymous Error Reports</span>
                  <p className="text-sm text-flow-gray">Help improve FlowState with anonymous crash reports</p>
                </div>
                <input
                  type="checkbox"
                  checked={preferences.privacy_settings.anonymous_error_reports || false}
                  onChange={(e) => setPreferences(prev => ({
                    ...prev,
                    privacy_settings: {
                      ...prev.privacy_settings,
                      anonymous_error_reports: e.target.checked
                    }
                  }))}
                  className="rounded border-gray-300 text-flow-blue focus:ring-flow-blue focus:ring-offset-0"
                />
              </label>
            </div>
          </div>

          <div className="flow-card bg-blue-50 border border-blue-200">
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                  <span className="text-blue-600">🔒</span>
                </div>
              </div>
              <div>
                <h4 className="font-medium text-blue-900 mb-2">FlowState Privacy Commitment</h4>
                <div className="text-sm text-blue-800 space-y-1">
                  <p>• No surveillance capitalism - your data is never monetized</p>
                  <p>• Transparent algorithms - you can see why every suggestion is made</p>
                  <p>• User-controlled complexity - you decide what features to use</p>
                  <p>• Professional ethics adherence in all psychological features</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Profile;