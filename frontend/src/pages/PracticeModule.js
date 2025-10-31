import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Send, Lightbulb, CheckCircle, XCircle, RotateCcw, Copy, Check } from 'lucide-react';
import { apiService } from '../services/api';
import { analytics } from '../services/analytics';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism';
import ReactMarkdown from 'react-markdown';
import { useChatbotContext } from '../context/ChatbotContext';
import toast from 'react-hot-toast';

const PracticeModule = () => {
  const { moduleId } = useParams();
  const navigate = useNavigate();
  // Generate unique user ID per session
  const [userId] = useState(() => {
    let storedUserId = localStorage.getItem('sql_learning_user_id');
    if (!storedUserId) {
      storedUserId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem('sql_learning_user_id', storedUserId);
    }
    return storedUserId;
  });
  const { updateContext } = useChatbotContext();
  
  const [module, setModule] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [userAnswer, setUserAnswer] = useState('');
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [showHints, setShowHints] = useState(false);
  const [questionCount, setQuestionCount] = useState(1);
  const [copiedCode, setCopiedCode] = useState(null);
  const [loadingNextQuestion, setLoadingNextQuestion] = useState(false);

  useEffect(() => {
    fetchModuleAndQuestion();
  }, [moduleId]);

  const fetchModuleAndQuestion = async () => {
    try {
      const [moduleResponse, businessQuestionResponse] = await Promise.all([
        apiService.getModule(moduleId),
        apiService.getBusinessQuestion(moduleId, 'easy') // Start with easy difficulty
      ]);
      
      setModule(moduleResponse.data);
      setCurrentQuestion(businessQuestionResponse.data);
      
      // Track module start
      analytics.trackModuleStart(moduleId, moduleResponse.data.name);
      
      // Update chatbot context with current question
      updateContext({
        currentPage: 'practice',
        currentModule: moduleResponse.data.name,
        currentQuestion: businessQuestionResponse.data.question,
        userProgress: { 
          questionCount, 
          difficulty: businessQuestionResponse.data.difficulty,
          module: moduleResponse.data.name
        }
      });
      
      setLoading(false);
    } catch (error) {
      console.error('Error fetching module data:', error);
      toast.error('Failed to load practice module');
      setLoading(false);
    }
  };

  const submitAnswer = async () => {
    if (!userAnswer.trim()) {
      toast.error('Please enter your SQL query');
      return;
    }

    setSubmitting(true);
    try {
      const response = await apiService.evaluateBusinessAnswer({
        question_id: currentQuestion.question_id,
        user_sql: userAnswer,
        expected_sql: currentQuestion.expected_sql
      });
      
      setFeedback(response.data);
      
      // Track question completion
      analytics.trackQuestionCompleted(
        moduleId,
        currentQuestion.question_id,
        response.data.is_correct,
        response.data.score,
        currentQuestion.difficulty
      );
      
      setSubmitting(false);
    } catch (error) {
      console.error('Error submitting answer:', error);
      toast.error('Failed to submit answer');
      setSubmitting(false);
    }
  };

  const nextQuestion = async () => {
    setLoadingNextQuestion(true);
    try {
      // Cycle through difficulties based on performance
      let nextDifficulty = 'easy';
      if (feedback && feedback.score >= 0.8) {
        nextDifficulty = currentQuestion.difficulty === 'easy' ? 'medium' : 'medium';
      }
      
      const response = await apiService.getBusinessQuestion(moduleId, nextDifficulty);
      const newQuestionCount = questionCount + 1;
      
      setCurrentQuestion(response.data);
      setUserAnswer('');
      setFeedback(null);
      setShowHints(false);
      setQuestionCount(newQuestionCount);
      
      // Update chatbot context with new question
      updateContext({
        currentPage: 'practice',
        currentModule: module?.name,
        currentQuestion: response.data.question,
        userProgress: { 
          questionCount: newQuestionCount, 
          difficulty: response.data.difficulty,
          module: module?.name
        }
      });
    } catch (error) {
      console.error('Error loading next question:', error);
      toast.error('Failed to load next question');
    } finally {
      setLoadingNextQuestion(false);
    }
  };

  const copyCodeToClipboard = async (code, id) => {
    try {
      await navigator.clipboard.writeText(code);
      setCopiedCode(id);
      toast.success('SQL code copied!');
      
      // Track code copy event
      analytics.trackCodeCopy('sql', 'practice');
      
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

  const resetAnswer = () => {
    setUserAnswer('');
    setFeedback(null);
    setShowHints(false);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!module || !currentQuestion) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8 text-center">
        <p className="text-gray-500">No questions available for this module.</p>
        <button
          onClick={() => navigate('/practice')}
          className="mt-4 btn-primary"
        >
          Back to Practice
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-8">
        {/* Header */}
        <div className="flex items-center space-x-3 sm:space-x-4 mb-6 sm:mb-8">
          <button
            onClick={() => navigate('/practice')}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors touch-manipulation"
          >
            <ArrowLeft className="h-5 w-5" />
          </button>
          <div className="flex-1 min-w-0">
            <h1 className="text-xl sm:text-2xl font-bold text-gray-900 truncate">{module.name}</h1>
            <p className="text-sm sm:text-base text-gray-600">Question {questionCount}</p>
          </div>
        </div>

        {/* Question */}
        <div className="card mb-4 sm:mb-6">
          <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-2 sm:gap-4 mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Question</h2>
            <span className={`px-2 py-1 text-xs font-medium rounded-full self-start ${
              currentQuestion.difficulty === 'easy' ? 'bg-green-100 text-green-800' :
              currentQuestion.difficulty === 'medium' ? 'bg-yellow-100 text-yellow-800' :
              'bg-red-100 text-red-800'
            }`}>
              {currentQuestion.difficulty}
            </span>
          </div>
        
        <div className="space-y-3">
          {formatMessageContent(currentQuestion.question).map((part, index) => (
            <div key={index}>
              {part.type === 'markdown' ? (
                <div className="text-gray-700 leading-relaxed prose max-w-none">
                  <ReactMarkdown
                    components={{
                      h1: ({node, ...props}) => <h1 className="text-xl font-bold text-gray-900 mb-3 mt-4 first:mt-0" {...props} />,
                      h2: ({node, ...props}) => <h2 className="text-lg font-bold text-gray-900 mb-2 mt-3 first:mt-0" {...props} />,
                      h3: ({node, ...props}) => <h3 className="text-base font-bold text-gray-900 mb-2 mt-2 first:mt-0" {...props} />,
                      strong: ({node, ...props}) => <strong className="font-semibold text-gray-900" {...props} />,
                      em: ({node, ...props}) => <em className="italic text-gray-800" {...props} />,
                      p: ({node, ...props}) => <p className="mb-3 last:mb-0" {...props} />,
                      ul: ({node, ...props}) => <ul className="list-disc pl-6 mb-3 space-y-1" {...props} />,
                      ol: ({node, ...props}) => <ol className="list-decimal pl-6 mb-3 space-y-1" {...props} />,
                      li: ({node, ...props}) => <li className="text-base" {...props} />,
                      code: ({node, ...props}) => <code className="bg-gray-100 text-gray-800 px-2 py-1 rounded text-sm font-mono" {...props} />,
                      blockquote: ({node, ...props}) => <blockquote className="border-l-4 border-gray-300 pl-4 italic text-gray-700 mb-3" {...props} />
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
                      onClick={() => copyCodeToClipboard(part.content, `question-${index}`)}
                      className="flex items-center gap-1 text-xs text-gray-500 hover:text-gray-700 transition-colors touch-manipulation"
                    >
                      {copiedCode === `question-${index}` ? (
                        <>
                          <Check className="h-3 w-3" />
                          <span className="hidden sm:inline">Copied!</span>
                        </>
                      ) : (
                        <>
                          <Copy className="h-3 w-3" />
                          <span className="hidden sm:inline">Copy</span>
                        </>
                      )}
                    </button>
                  </div>
                  <SyntaxHighlighter
                    language="sql"
                    style={tomorrow}
                    customStyle={{
                      margin: 0,
                      borderRadius: '6px',
                      fontSize: '0.875rem',
                      padding: '0.75rem',
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
        
        {/* Hints */}
        {currentQuestion.hints && currentQuestion.hints.length > 0 && (
          <div className="mt-4">
            <button
              onClick={() => setShowHints(!showHints)}
              className="flex items-center space-x-2 text-primary-600 hover:text-primary-700 transition-colors"
            >
              <Lightbulb className="h-4 w-4" />
              <span>{showHints ? 'Hide' : 'Show'} Hints</span>
            </button>
            
            {showHints && (
              <div className="mt-2 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                <div className="space-y-2">
                  {currentQuestion.hints.map((hint, index) => (
                    <div key={index} className="flex items-start space-x-2">
                      <span className="text-yellow-600 mt-0.5">💡</span>
                      <div className="flex-1 space-y-2">
                        {formatMessageContent(hint).map((part, partIndex) => (
                          <div key={partIndex}>
                            {part.type === 'markdown' ? (
                              <div className="text-sm text-yellow-800">
                                <ReactMarkdown
                                  components={{
                                    h1: ({node, ...props}) => <h1 className="text-base font-bold text-yellow-900 mb-1 mt-2 first:mt-0" {...props} />,
                                    h2: ({node, ...props}) => <h2 className="text-sm font-bold text-yellow-900 mb-1 mt-2 first:mt-0" {...props} />,
                                    h3: ({node, ...props}) => <h3 className="text-sm font-semibold text-yellow-900 mb-1 mt-1 first:mt-0" {...props} />,
                                    strong: ({node, ...props}) => <strong className="font-semibold text-yellow-900" {...props} />,
                                    em: ({node, ...props}) => <em className="italic text-yellow-800" {...props} />,
                                    p: ({node, ...props}) => <p className="mb-1 last:mb-0" {...props} />,
                                    ul: ({node, ...props}) => <ul className="list-disc pl-4 mb-1 space-y-1" {...props} />,
                                    ol: ({node, ...props}) => <ol className="list-decimal pl-4 mb-1 space-y-1" {...props} />,
                                    li: ({node, ...props}) => <li className="text-sm" {...props} />,
                                    code: ({node, ...props}) => <code className="bg-yellow-100 text-yellow-900 px-1 py-0.5 rounded text-xs font-mono" {...props} />,
                                    blockquote: ({node, ...props}) => <blockquote className="border-l-4 border-yellow-300 pl-2 italic text-yellow-700 mb-1" {...props} />
                                  }}
                                >
                                  {part.content}
                                </ReactMarkdown>
                              </div>
                            ) : (
                              <div className="relative">
                                <div className="flex items-center justify-between mb-1">
                                  <span className="text-xs font-medium text-yellow-600 uppercase tracking-wide">
                                    SQL Hint
                                  </span>
                                  <button
                                    onClick={() => copyCodeToClipboard(part.content, `hint-${index}-${partIndex}`)}
                                    className="flex items-center gap-1 text-xs text-yellow-600 hover:text-yellow-800 transition-colors"
                                  >
                                    {copiedCode === `hint-${index}-${partIndex}` ? (
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
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

        {/* Answer Input */}
        <div className="card mb-4 sm:mb-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-base sm:text-lg font-semibold text-gray-900">Your SQL Query</h3>
            <button
              onClick={resetAnswer}
              className="p-2 text-gray-400 hover:text-gray-600 transition-colors touch-manipulation"
              title="Reset answer"
            >
              <RotateCcw className="h-4 w-4" />
            </button>
          </div>
          
          <textarea
            value={userAnswer}
            onChange={(e) => setUserAnswer(e.target.value)}
            placeholder="Enter your SQL query here..."
            className="textarea-field font-mono text-sm resize-none"
            rows={6}
            disabled={feedback !== null}
          />
          
          <div className="mt-4 flex flex-col sm:flex-row justify-end gap-3 sm:gap-3 sm:space-x-0">
            {feedback === null ? (
              <button
                onClick={submitAnswer}
                disabled={submitting || !userAnswer.trim()}
                className="btn-primary flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed w-full sm:w-auto touch-manipulation"
              >
                {submitting ? (
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                ) : (
                  <Send className="h-4 w-4" />
                )}
                <span>{submitting ? 'Submitting...' : 'Submit Answer'}</span>
              </button>
            ) : (
              <button
                onClick={nextQuestion}
                disabled={loadingNextQuestion}
                className="btn-primary flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed w-full sm:w-auto touch-manipulation"
              >
                {loadingNextQuestion ? (
                  <>
                    <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                    <span>Loading...</span>
                  </>
                ) : (
                  <span>Next Question</span>
                )}
              </button>
            )}
          </div>
        </div>

        {/* Feedback */}
        {feedback && (
          <div className="card">
          <div className="flex items-center space-x-3 mb-4">
            {feedback.is_correct ? (
              <CheckCircle className="h-6 w-6 text-green-500" />
            ) : (
              <XCircle className="h-6 w-6 text-red-500" />
            )}
            <h3 className="text-lg font-semibold text-gray-900">
              {feedback.is_correct ? 'Correct!' : 'Not Quite Right'}
            </h3>
            <span className="text-sm text-gray-500">
              Score: {(feedback.score * 100).toFixed(0)}%
            </span>
          </div>
          
          <div className="space-y-3">
            {formatMessageContent(feedback.feedback).map((part, index) => (
              <div key={index}>
                {part.type === 'markdown' ? (
                  <div className="prose max-w-none">
                    <ReactMarkdown
                      components={{
                        h1: ({node, ...props}) => <h1 className="text-lg font-bold text-gray-900 mb-2 mt-3 first:mt-0" {...props} />,
                        h2: ({node, ...props}) => <h2 className="text-base font-bold text-gray-900 mb-2 mt-3 first:mt-0" {...props} />,
                        h3: ({node, ...props}) => <h3 className="text-sm font-bold text-gray-900 mb-1 mt-2 first:mt-0" {...props} />,
                        strong: ({node, ...props}) => <strong className="font-semibold text-gray-900" {...props} />,
                        em: ({node, ...props}) => <em className="italic text-gray-800" {...props} />,
                        p: ({node, ...props}) => <p className="mb-2 last:mb-0 text-gray-700 leading-relaxed" {...props} />,
                        ul: ({node, ...props}) => <ul className="list-disc pl-4 mb-2 space-y-1" {...props} />,
                        ol: ({node, ...props}) => <ol className="list-decimal pl-4 mb-2 space-y-1" {...props} />,
                        li: ({node, ...props}) => <li className="text-sm" {...props} />,
                        code: ({node, ...props}) => <code className="bg-gray-100 text-gray-800 px-1 py-0.5 rounded text-xs font-mono" {...props} />,
                        blockquote: ({node, ...props}) => <blockquote className="border-l-4 border-gray-300 pl-3 italic text-gray-700 mb-2" {...props} />
                      }}
                    >
                      {part.content}
                    </ReactMarkdown>
                  </div>
                ) : (
                  <div className="relative">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                        SQL Code
                      </span>
                      <button
                        onClick={() => copyCodeToClipboard(part.content, `feedback-${index}`)}
                        className="flex items-center gap-1 text-xs text-gray-500 hover:text-gray-700 transition-colors"
                      >
                        {copiedCode === `feedback-${index}` ? (
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
                        borderRadius: '6px',
                        fontSize: '0.875rem',
                        padding: '0.75rem',
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
          
          {feedback.correct_sql && feedback.correct_sql !== userAnswer && (
            <div className="mt-4">
              <h4 className="text-sm font-medium text-gray-700 mb-2">Suggested Solution:</h4>
              <SyntaxHighlighter
                language="sql"
                style={tomorrow}
                customStyle={{
                  margin: 0,
                  padding: '1rem',
                  fontSize: '0.875rem',
                  borderRadius: '0.5rem',
                }}
              >
                {feedback.correct_sql}
              </SyntaxHighlighter>
            </div>
          )}
          
          {feedback.next_difficulty && (
            <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
              <p className="text-sm text-blue-800">
                Next difficulty level: <span className="font-medium">{feedback.next_difficulty}</span>
              </p>
            </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default PracticeModule;