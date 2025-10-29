import { track } from '@vercel/analytics';

/**
 * Utility functions for tracking user interactions with Vercel Analytics
 */
export const analytics = {
  // Track when user starts a practice module
  trackModuleStart: (moduleId, moduleName) => {
    track('module_started', {
      module_id: moduleId,
      module_name: moduleName
    });
  },

  // Track when user completes a question
  trackQuestionCompleted: (moduleId, questionId, isCorrect, score, difficulty) => {
    track('question_completed', {
      module_id: moduleId,
      question_id: questionId,
      is_correct: isCorrect,
      score: score,
      difficulty: difficulty
    });
  },

  // Track chatbot usage
  trackChatbotMessage: (context, messageType = 'user_message') => {
    track('chatbot_interaction', {
      context_page: context.page || 'unknown',
      context_module: context.module || '',
      message_type: messageType
    });
  },

  // Track when user uses dynamic examples in cheat sheet
  trackDynamicExample: (command, category) => {
    track('dynamic_example_generated', {
      sql_command: command,
      category: category
    });
  },

  // Track when user copies code
  trackCodeCopy: (codeType, location) => {
    track('code_copied', {
      code_type: codeType, // 'sql', 'example', 'solution'
      location: location   // 'cheatsheet', 'practice', 'chatbot'
    });
  },

  // Track analytics page views
  trackAnalyticsView: (userId) => {
    track('analytics_viewed', {
      user_id: userId
    });
  },

  // Track when user toggles chatbot full screen
  trackChatbotFullScreen: (isFullScreen) => {
    track('chatbot_fullscreen_toggle', {
      is_fullscreen: isFullScreen
    });
  },

  // Track user progress milestones
  trackProgressMilestone: (milestone, moduleId, totalProgress) => {
    track('progress_milestone', {
      milestone: milestone, // 'first_question', 'module_50_percent', 'module_completed'
      module_id: moduleId,
      total_progress: totalProgress
    });
  },

  // Track difficulty level changes
  trackDifficultyChange: (moduleId, fromDifficulty, toDifficulty) => {
    track('difficulty_changed', {
      module_id: moduleId,
      from_difficulty: fromDifficulty,
      to_difficulty: toDifficulty
    });
  },

  // Track search usage in cheat sheet
  trackCheatSheetSearch: (searchTerm, resultsCount) => {
    track('cheatsheet_search', {
      search_term: searchTerm,
      results_count: resultsCount
    });
  }
};

export default analytics;