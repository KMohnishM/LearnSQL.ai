import React, { useState, useEffect } from 'react';
import { TrendingUp, Award, Target, Clock, BarChart3, PieChart, Copy, Check } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart as RechartsPieChart, Cell } from 'recharts';
import { apiService } from '../services/api';
import { analytics as analyticsService } from '../services/analytics';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism';
import ReactMarkdown from 'react-markdown';
import toast from 'react-hot-toast';

const Analysis = () => {
  const [userId] = useState('user_123');
  const [analytics, setAnalytics] = useState(null);
  const [detailedAnalytics, setDetailedAnalytics] = useState(null);
  const [suggestions, setSuggestions] = useState(null);
  const [loading, setLoading] = useState(true);
  const [copiedCode, setCopiedCode] = useState(null);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const [analyticsResponse, detailedResponse, suggestionsResponse] = await Promise.all([
        apiService.getUserAnalytics(userId),
        apiService.getDetailedAnalytics(userId),
        apiService.getLearningPathSuggestions(userId)
      ]);
      
      setAnalytics(analyticsResponse.data);
      setDetailedAnalytics(detailedResponse.data);
      setSuggestions(suggestionsResponse.data);
      
      // Track analytics page view
      analyticsService.trackAnalyticsView(userId);
      
      setLoading(false);
    } catch (error) {
      console.error('Error fetching analytics:', error);
      toast.error('Failed to load analytics');
      setLoading(false);
    }
  };

  const difficultyColors = {
    easy: '#10B981',
    medium: '#F59E0B', 
    hard: '#EF4444'
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric' 
    });
  };

  const copyCodeToClipboard = async (code, id) => {
    try {
      await navigator.clipboard.writeText(code);
      setCopiedCode(id);
      toast.success('SQL code copied!');
      setTimeout(() => setCopiedCode(null), 2000);
    } catch (error) {
      toast.error('Failed to copy code');
    }
  };

  const formatMessageContent = (content) => {
    // Split content by SQL code blocks
    const parts = content.split(/```sql\n([\s\S]*?)\n```/g);
    const formattedParts = [];
    
    for (let i = 0; i < parts.length; i++) {
      if (i % 2 === 0) {
        // Regular text (markdown)
        if (parts[i].trim()) {
          formattedParts.push({
            type: 'markdown',
            content: parts[i].trim()
          });
        }
      } else {
        // SQL code
        formattedParts.push({
          type: 'sql',
          content: parts[i].trim()
        });
      }
    }
    
    return formattedParts;
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!analytics || analytics.total_questions_attempted === 0) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center py-12">
          <BarChart3 className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">No Data Yet</h2>
          <p className="text-gray-600 mb-6">Start practicing to see your progress and analytics!</p>
          <button
            onClick={() => window.location.href = '/practice'}
            className="btn-primary"
          >
            Start Learning
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Learning Analytics</h1>
        <p className="text-gray-600">Track your progress and identify areas for improvement</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-primary-100">
              <Target className="h-6 w-6 text-primary-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Overall Accuracy</p>
              <p className="text-2xl font-bold text-gray-900">
                {analytics.overall_accuracy.toFixed(1)}%
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-green-100">
              <Award className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Questions Correct</p>
              <p className="text-2xl font-bold text-gray-900">
                {analytics.total_correct}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-blue-100">
              <TrendingUp className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Total Attempts</p>
              <p className="text-2xl font-bold text-gray-900">
                {analytics.total_questions_attempted}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-purple-100">
              <Clock className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Modules Started</p>
              <p className="text-2xl font-bold text-gray-900">
                {analytics.modules_progress.length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Performance Over Time */}
      {detailedAnalytics && detailedAnalytics.performance_over_time.length > 0 && (
        <div className="card mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Performance Over Time</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={detailedAnalytics.performance_over_time.reverse()}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="date" 
                  tickFormatter={formatDate}
                />
                <YAxis domain={[0, 1]} tickFormatter={(value) => `${(value * 100).toFixed(0)}%`} />
                <Tooltip 
                  labelFormatter={(value) => `Date: ${formatDate(value)}`}
                  formatter={(value) => [`${(value * 100).toFixed(1)}%`, 'Average Score']}
                />
                <Line 
                  type="monotone" 
                  dataKey="avg_score" 
                  stroke="#3B82F6" 
                  strokeWidth={2}
                  dot={{ fill: '#3B82F6', strokeWidth: 2, r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Module Progress */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Module Progress</h2>
          <div className="space-y-4">
            {analytics.modules_progress.map((module) => (
              <div key={module.module_id} className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-700">{module.module_name}</span>
                  <span className="text-sm text-gray-500">
                    {module.completion_percentage.toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${module.completion_percentage}%` }}
                  ></div>
                </div>
                <div className="flex justify-between text-xs text-gray-500">
                  <span>{module.questions_attempted} attempts</span>
                  <span className={`px-2 py-1 rounded-full ${
                    module.current_difficulty === 'easy' ? 'bg-green-100 text-green-800' :
                    module.current_difficulty === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {module.current_difficulty}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Difficulty Distribution */}
        {detailedAnalytics && detailedAnalytics.difficulty_distribution.length > 0 && (
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Performance by Difficulty</h2>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <RechartsPieChart>
                  <Pie
                    data={detailedAnalytics.difficulty_distribution}
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    dataKey="attempts"
                    nameKey="difficulty_level"
                  >
                    {detailedAnalytics.difficulty_distribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={difficultyColors[entry.difficulty_level]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value, name) => [value, `${name} attempts`]} />
                </RechartsPieChart>
              </ResponsiveContainer>
            </div>
            <div className="flex justify-center space-x-4 mt-4">
              {detailedAnalytics.difficulty_distribution.map((item) => (
                <div key={item.difficulty_level} className="flex items-center space-x-2">
                  <div
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: difficultyColors[item.difficulty_level] }}
                  ></div>
                  <span className="text-sm text-gray-600 capitalize">
                    {item.difficulty_level} ({(item.avg_score * 100).toFixed(0)}% avg)
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Strengths and Areas for Improvement */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Strengths</h2>
          <div className="space-y-3">
            {analytics.strengths.map((strength, index) => (
              <div key={index} className="flex items-start space-x-3">
                <Award className="h-5 w-5 text-green-500 mt-0.5" />
                <p className="text-gray-700">{strength}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Areas for Improvement</h2>
          <div className="space-y-3">
            {analytics.areas_for_improvement.map((area, index) => (
              <div key={index} className="flex items-start space-x-3">
                <Target className="h-5 w-5 text-orange-500 mt-0.5" />
                <p className="text-gray-700">{area}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Learning Path Suggestions */}
      {suggestions && suggestions.suggestions.length > 0 && (
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Personalized Learning Recommendations</h2>
          <div className="space-y-4">
            {suggestions.suggestions.map((suggestion, index) => (
              <div
                key={index}
                className={`p-4 rounded-lg border-l-4 ${
                  suggestion.priority === 'high' ? 'border-red-400 bg-red-50' :
                  suggestion.priority === 'medium' ? 'border-yellow-400 bg-yellow-50' :
                  'border-blue-400 bg-blue-50'
                }`}
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1 mr-4">
                    <h3 className="font-medium text-gray-900">{suggestion.module_name}</h3>
                    <div className="mt-1 space-y-2">
                      {formatMessageContent(suggestion.reason).map((part, partIndex) => (
                        <div key={partIndex}>
                          {part.type === 'markdown' ? (
                            <div className="text-gray-600">
                              <ReactMarkdown
                                components={{
                                  h1: ({node, ...props}) => <h1 className="text-base font-bold text-gray-900 mb-1 mt-2 first:mt-0" {...props} />,
                                  h2: ({node, ...props}) => <h2 className="text-sm font-bold text-gray-900 mb-1 mt-2 first:mt-0" {...props} />,
                                  h3: ({node, ...props}) => <h3 className="text-sm font-semibold text-gray-900 mb-1 mt-1 first:mt-0" {...props} />,
                                  strong: ({node, ...props}) => <strong className="font-semibold text-gray-900" {...props} />,
                                  em: ({node, ...props}) => <em className="italic text-gray-700" {...props} />,
                                  p: ({node, ...props}) => <p className="mb-1 last:mb-0" {...props} />,
                                  ul: ({node, ...props}) => <ul className="list-disc pl-4 mb-1 space-y-1" {...props} />,
                                  ol: ({node, ...props}) => <ol className="list-decimal pl-4 mb-1 space-y-1" {...props} />,
                                  li: ({node, ...props}) => <li className="text-sm" {...props} />,
                                  code: ({node, ...props}) => <code className="bg-gray-100 text-gray-800 px-1 py-0.5 rounded text-xs font-mono" {...props} />,
                                  blockquote: ({node, ...props}) => <blockquote className="border-l-4 border-gray-300 pl-2 italic text-gray-600 mb-1" {...props} />
                                }}
                              >
                                {part.content}
                              </ReactMarkdown>
                            </div>
                          ) : (
                            <div className="relative">
                              <div className="flex items-center justify-between mb-2">
                                <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                                  SQL Example
                                </span>
                                <button
                                  onClick={() => copyCodeToClipboard(part.content, `suggestion-${index}-${partIndex}`)}
                                  className="flex items-center gap-1 text-xs text-gray-500 hover:text-gray-700 transition-colors"
                                >
                                  {copiedCode === `suggestion-${index}-${partIndex}` ? (
                                    <>
                                      <Check className="h-3 w-3" />
                                      Copied!
                                    </>
                                  ) : (
                                    <>
                                      <Copy className="h-3 w-3" />
                                      Copy
                                    </>
                                  )}
                                </button>
                              </div>
                              <SyntaxHighlighter
                                language="sql"
                                style={tomorrow}
                                customStyle={{
                                  margin: 0,
                                  borderRadius: '4px',
                                  fontSize: '0.75rem',
                                  padding: '0.5rem',
                                  background: '#1a1a1a',
                                }}
                              >
                                {part.content}
                              </SyntaxHighlighter>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                  <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                    suggestion.priority === 'high' ? 'bg-red-100 text-red-800' :
                    suggestion.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-blue-100 text-blue-800'
                  }`}>
                    {suggestion.priority} priority
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recent Attempts */}
      {analytics.recent_attempts.length > 0 && (
        <div className="card mt-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Recent Attempts</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Module
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Result
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Score
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {analytics.recent_attempts.slice(0, 10).map((attempt, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {new Date(attempt.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {attempt.module_name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        attempt.is_correct ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}>
                        {attempt.is_correct ? 'Correct' : 'Incorrect'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {attempt.score ? `${(attempt.score * 100).toFixed(0)}%` : 'N/A'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default Analysis;