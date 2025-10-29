# Vercel Analytics Integration

This document outlines the analytics tracking implementation for the SQL Learning Platform using Vercel Analytics and Speed Insights.

## 📊 Analytics Overview

The application now includes comprehensive analytics tracking to understand user behavior, learning patterns, and platform performance.

### Packages Installed
- `@vercel/analytics` - Page views and custom event tracking
- `@vercel/speed-insights` - Core Web Vitals and performance monitoring

## 🔧 Implementation

### 1. Core Analytics Setup
Located in `src/App.jsx`:
```jsx
import { Analytics } from '@vercel/analytics/react';
import { SpeedInsights } from '@vercel/speed-insights/react';

// Added to the main App component
<Analytics />
<SpeedInsights />
```

### 2. Custom Event Tracking Service
File: `src/services/analytics.js`

Provides utility functions for tracking specific user interactions:

#### Key Functions:
- `trackModuleStart()` - When user begins a practice module
- `trackQuestionCompleted()` - Question submission with correctness and score
- `trackChatbotMessage()` - Chatbot interactions with context
- `trackDynamicExample()` - AI-generated example requests
- `trackCodeCopy()` - Code copying events
- `trackAnalyticsView()` - Analytics page visits
- `trackChatbotFullScreen()` - Full-screen chatbot usage
- `trackProgressMilestone()` - Learning achievements
- `trackDifficultyChange()` - Difficulty level adjustments
- `trackCheatSheetSearch()` - Search functionality usage

## 📈 Events Being Tracked

### Practice Module Events
- **Module Started**: `module_started`
  - `module_id`: Module identifier
  - `module_name`: Human-readable module name

- **Question Completed**: `question_completed`
  - `module_id`: Current module
  - `question_id`: Unique question identifier
  - `is_correct`: Boolean result
  - `score`: Numerical score (0-1)
  - `difficulty`: Question difficulty level

- **Code Copied**: `code_copied`
  - `code_type`: Type of code (sql, example, solution)
  - `location`: Where it was copied from (practice, cheatsheet, chatbot)

### Chatbot Events
- **Chatbot Interaction**: `chatbot_interaction`
  - `context_page`: Current page user is on
  - `context_module`: Current learning module
  - `message_type`: Type of interaction

- **Full-Screen Toggle**: `chatbot_fullscreen_toggle`
  - `is_fullscreen`: Boolean state

### Cheat Sheet Events
- **Dynamic Example Generated**: `dynamic_example_generated`
  - `sql_command`: SQL command for example
  - `category`: Command category

- **Search Usage**: `cheatsheet_search`
  - `search_term`: What user searched for
  - `results_count`: Number of results found

### Analytics Events
- **Analytics Page View**: `analytics_viewed`
  - `user_id`: User identifier

### Progress Events
- **Progress Milestone**: `progress_milestone`
  - `milestone`: Achievement type
  - `module_id`: Related module
  - `total_progress`: Overall completion percentage

- **Difficulty Change**: `difficulty_changed`
  - `module_id`: Module where change occurred
  - `from_difficulty`: Previous level
  - `to_difficulty`: New level

## 🚀 Deployment Considerations

### For Vercel Deployment
Analytics will automatically work when deployed to Vercel. No additional configuration needed.

### For Other Platforms
You may need to set up environment variables or configure the analytics provider differently depending on your hosting platform.

## 📊 Data Analysis

With these events, you can analyze:

1. **Learning Patterns**
   - Which modules are most challenging
   - Time spent on different difficulty levels
   - Common mistake patterns

2. **Feature Usage**
   - Chatbot engagement rates
   - Cheat sheet search patterns
   - Code copying behavior

3. **User Journey**
   - Module completion rates
   - Drop-off points
   - Help-seeking behavior

4. **Performance Metrics**
   - Page load times
   - Core Web Vitals
   - User engagement duration

## 🔍 Viewing Analytics

1. **Vercel Dashboard**: Visit your Vercel project dashboard
2. **Analytics Tab**: Click on the Analytics tab
3. **Custom Events**: View custom events in the Events section
4. **Speed Insights**: Monitor performance metrics

## 🛠️ Customization

To add new tracking events:

1. Add a new function to `src/services/analytics.js`
2. Import and call the function in the relevant component
3. Follow the existing pattern for event naming and properties

Example:
```javascript
// In analytics.js
trackNewFeature: (featureName, userAction) => {
  track('feature_used', {
    feature_name: featureName,
    user_action: userAction
  });
}

// In component
import { analytics } from '../services/analytics';
analytics.trackNewFeature('advanced_search', 'filter_applied');
```

## 🔒 Privacy

All analytics data is processed according to Vercel's privacy policy. No personally identifiable information is tracked beyond user session data for learning progress.

---

**Analytics tracking is now active across the entire SQL Learning Platform! 📊**