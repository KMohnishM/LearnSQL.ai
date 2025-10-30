/**
 * User session management utility
 * Handles unique user identification for progress tracking
 */

export const userSession = {
  /**
   * Get or generate unique user ID for this browser session
   * Persists across page reloads but unique per browser/device
   */
  getUserId: () => {
    let storedUserId = localStorage.getItem('sql_learning_user_id');
    if (!storedUserId) {
      // Generate unique ID: timestamp + random string
      storedUserId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem('sql_learning_user_id', storedUserId);
      
      // Also store session start time for analytics
      localStorage.setItem('sql_learning_session_start', new Date().toISOString());
    }
    return storedUserId;
  },

  /**
   * Clear current user session (for testing or reset)
   */
  clearSession: () => {
    localStorage.removeItem('sql_learning_user_id');
    localStorage.removeItem('sql_learning_session_start');
  },

  /**
   * Get session info for analytics
   */
  getSessionInfo: () => {
    return {
      userId: userSession.getUserId(),
      sessionStart: localStorage.getItem('sql_learning_session_start'),
      browserInfo: {
        userAgent: navigator.userAgent,
        language: navigator.language,
        timestamp: new Date().toISOString()
      }
    };
  },

  /**
   * Generate new user ID (forces new session)
   */
  generateNewSession: () => {
    userSession.clearSession();
    return userSession.getUserId();
  }
};

export default userSession;