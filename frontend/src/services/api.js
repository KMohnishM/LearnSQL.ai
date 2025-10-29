import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Cheat sheet endpoints
  getCheatSheet: () => api.get('/cheatsheet'),
  getCheatSheetByCategory: (category) => api.get(`/cheatsheet/category/${category}`),
  searchCheatSheet: (searchTerm) => api.get(`/cheatsheet/search/${searchTerm}`),
  getDynamicExample: (data) => api.post('/cheat-sheet/example', data),

  // Practice endpoints
  getModules: () => api.get('/modules'),
  getModule: (moduleId) => api.get(`/modules/${moduleId}`),
  getModuleQuestions: (moduleId, difficulty = 'medium') => 
    api.get(`/modules/${moduleId}/questions?difficulty=${difficulty}`),
  getNextQuestion: (moduleId, userId) => 
    api.get(`/modules/${moduleId}/next-question/${userId}`),
  submitAnswer: (data) => api.post('/practice/submit', data),  
  getUserProgress: (userId) => api.get(`/practice/progress/${userId}`),
  
  // Business scenario endpoints
  getBusinessQuestion: (moduleId, difficulty = 'easy') => 
    api.get(`/modules/${moduleId}/business-question?difficulty=${difficulty}`),
  evaluateBusinessAnswer: (data) => api.post('/practice/evaluate-business-answer', data),
  getBusinessProgress: (userId, moduleId) => api.get(`/progress/${userId}/module/${moduleId}`),

  // Analysis endpoints
  getUserAnalytics: (userId) => api.get(`/analysis/${userId}`),
  getDetailedAnalytics: (userId) => api.get(`/analysis/${userId}/detailed`),
  getLearningPathSuggestions: (userId) => api.get(`/analysis/${userId}/learning-path`),

  // Chatbot endpoints
  sendChatMessage: (data) => api.post('/chatbot/message', data),
  clearChatHistory: () => api.post('/chatbot/clear'),
  chatbotHealth: () => api.get('/chatbot/health'),

  // Health check
  healthCheck: () => api.get('/health'),
};

export default apiService;