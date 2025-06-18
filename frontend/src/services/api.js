import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || window.location.origin;

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => {
        return response.data;
      },
      (error) => {
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(error.response?.data || error);
      }
    );
  }

  // Health check
  async healthCheck() {
    return this.client.get('/api/health');
  }

  // User management
  async createUser(username, preferences = {}) {
    return this.client.post('/api/users', { username, preferences });
  }

  async getUser(userId) {
    return this.client.get(`/api/users/${userId}`);
  }

  async updateUserPreferences(userId, preferences) {
    return this.client.put(`/api/users/${userId}/preferences`, preferences);
  }

  // Session management
  async startSession(userId, sessionData) {
    return this.client.post(`/api/users/${userId}/sessions/start`, sessionData);
  }

  async endSession(userId, sessionData) {
    return this.client.post(`/api/users/${userId}/sessions/end`, sessionData);
  }

  async getActiveSessions(userId) {
    return this.client.get(`/api/users/${userId}/sessions/active`);
  }

  async getCurrentSession(userId) {
    return this.client.get(`/api/users/${userId}/sessions/current`);
  }

  async getSession(userId, sessionId) {
    return this.client.get(`/api/users/${userId}/sessions/${sessionId}`);
  }

  async pauseSession(userId, sessionId) {
    return this.client.post(`/api/users/${userId}/sessions/${sessionId}/pause`);
  }

  async resumeSession(userId, sessionId) {
    return this.client.post(`/api/users/${userId}/sessions/${sessionId}/resume`);
  }

  async cancelSession(userId, sessionId) {
    return this.client.delete(`/api/users/${userId}/sessions/${sessionId}`);
  }

  // Tag management
  async getUserTags(userId) {
    return this.client.get(`/api/users/${userId}/tags`);
  }

  async getTagAnalytics(userId, timeframeDays = 30) {
    return this.client.get(`/api/users/${userId}/tags/analytics?timeframe_days=${timeframeDays}`);
  }

  async getEstimationAccuracy(userId) {
    return this.client.get(`/api/users/${userId}/estimation-accuracy`);
  }

  // Analytics and insights
  async getDailySummary(userId, date = null) {
    const params = date ? `?date=${date}` : '';
    return this.client.get(`/api/users/${userId}/summary/daily${params}`);
  }

  async getInsights(userId, timeframeDays = 30) {
    return this.client.get(`/api/users/${userId}/insights?timeframe_days=${timeframeDays}`);
  }

  async getPatterns(userId) {
    return this.client.get(`/api/users/${userId}/patterns`);
  }

  // Self-discovery
  async startSelfDiscovery(userId, category, supportLevel = 'guided') {
    return this.client.post(`/api/users/${userId}/self-discovery/start`, {
      category,
      support_level: supportLevel
    });
  }

  // Data export and privacy
  async exportUserData(userId) {
    return this.client.get(`/api/users/${userId}/export`);
  }

  async deleteUser(userId, confirmation) {
    return this.client.delete(`/api/users/${userId}?confirmation=${confirmation}`);
  }

  // Demo helpers
  async createSampleUser() {
    return this.client.get('/api/demo/sample-user');
  }

  async resetDemoUser(userId) {
    return this.client.get(`/api/demo/reset/${userId}`);
  }
}

export const apiService = new ApiService();