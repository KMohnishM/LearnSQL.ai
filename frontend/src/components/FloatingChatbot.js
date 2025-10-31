import React, { useState, useEffect, useRef } from 'react';
import { MessageCircle, X, Send, Loader, Sparkles, BookOpen, Target, Copy, Check, Maximize2, Minimize2 } from 'lucide-react';
import { apiService } from '../services/api';
import { analytics } from '../services/analytics';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism';
import ReactMarkdown from 'react-markdown';
import { useChatbotContext } from '../context/ChatbotContext';
import toast from 'react-hot-toast';

const FloatingChatbot = () => {
  const { chatbotContext } = useChatbotContext();
  const { currentPage, currentModule, currentQuestion, userProgress } = chatbotContext;
  const [isOpen, setIsOpen] = useState(false);
  const [isFullScreen, setIsFullScreen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [copiedCode, setCopiedCode] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Add welcome message when chatbot opens for the first time
    if (isOpen && messages.length === 0) {
      const welcomeMessage = getWelcomeMessage();
      setMessages([{
        id: Date.now(),
        type: 'bot',
        content: welcomeMessage.content,
        suggestions: welcomeMessage.suggestions,
        timestamp: new Date()
      }]);
    }
  }, [isOpen]);

  useEffect(() => {
    // Handle escape key to exit full-screen mode
    const handleEscape = (e) => {
      if (e.key === 'Escape' && isFullScreen) {
        setIsFullScreen(false);
      }
    };

    if (isFullScreen) {
      document.addEventListener('keydown', handleEscape);
      return () => document.removeEventListener('keydown', handleEscape);
    }
  }, [isFullScreen]);

  const getWelcomeMessage = () => {
    const context = getPageContext();
    let content = "👋 Hi! I'm your SQL learning assistant. I can help you with:";
    let suggestions = ["📚 SQL syntax questions", "🎯 Practice guidance", "💡 Concept explanations"];

    if (currentPage === 'practice' && currentModule) {
      content = `👋 Hi! I see you're working on ${currentModule}. How can I help you with this module?`;
      suggestions = ["❓ Explain this concept", "💡 Give me a hint", "🔍 Show me examples"];
    } else if (currentPage === 'cheatsheet') {
      content = "👋 Hi! I see you're browsing the cheat sheet. Need help understanding any SQL commands?";
      suggestions = ["🔍 Explain a command", "💼 Show business examples", "📖 Related concepts"];
    }

    return { content, suggestions };
  };

  const getPageContext = () => {
    return {
      page: currentPage || 'dashboard',
      module: currentModule || '',
      question: currentQuestion || '',
      progress: userProgress || {}
    };
  };

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const context = getPageContext();
      
      // Track chatbot interaction
      analytics.trackChatbotMessage(context, 'user_message');
      
      const response = await apiService.sendChatMessage({
        message: inputMessage,
        context: context
      });

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.data.response,
        suggestions: response.data.suggested_actions || [],
        contextAware: response.data.context_aware,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: "Sorry, I'm having trouble responding right now. Try asking about SQL syntax, practice modules, or check the cheat sheet for quick reference!",
        suggestions: ["📚 Visit Cheat Sheet", "🎯 Try Practice Modules"],
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
      toast.error('Failed to send message');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setInputMessage(suggestion.replace(/[📚🎯💡🔍❓💼📖⚡]/g, '').trim());
  };

  const clearChat = async () => {
    try {
      await apiService.clearChatHistory();
      setMessages([]);
      const welcomeMessage = getWelcomeMessage();
      setMessages([{
        id: Date.now(),
        type: 'bot',
        content: welcomeMessage.content,
        suggestions: welcomeMessage.suggestions,
        timestamp: new Date()
      }]);
      toast.success('Chat history cleared');
    } catch (error) {
      console.error('Error clearing chat:', error);
      toast.error('Failed to clear chat');
    }
  };

  const toggleFullScreen = () => {
    const newFullScreenState = !isFullScreen;
    setIsFullScreen(newFullScreenState);
    
    // Track full-screen toggle
    analytics.trackChatbotFullScreen(newFullScreenState);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
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

  if (!isOpen) {
    return (
      <div className="fixed bottom-4 right-4 sm:bottom-6 sm:right-6 z-50">
        <button
          onClick={() => setIsOpen(true)}
          className="bg-primary-600 hover:bg-primary-700 active:bg-primary-800 text-white rounded-full p-3 sm:p-4 shadow-lg transition-all duration-200 hover:scale-105 touch-manipulation"
          title="SQL Learning Assistant"
        >
          <MessageCircle className="h-5 w-5 sm:h-6 sm:w-6" />
        </button>
      </div>
    );
  }

  return (
    <>
      {/* Full-screen backdrop */}
      {isFullScreen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-40" />
      )}
      
      <div className={`fixed z-50 ${
        isFullScreen 
          ? 'inset-2 sm:inset-4' 
          : 'bottom-4 right-4 left-4 sm:bottom-6 sm:right-6 sm:left-auto'
      }`}>
        <div className={`bg-white shadow-2xl border border-gray-200 flex flex-col overflow-hidden ${
          isFullScreen 
            ? 'w-full h-full rounded-lg' 
            : 'rounded-xl w-full sm:w-96 h-[85vh] max-h-[600px] sm:h-[32rem]'
        }`}>
        {/* Header */}
        <div className="bg-gradient-to-r from-primary-600 to-blue-600 text-white p-3 sm:p-4 flex justify-between items-center">
          <div className="flex items-center gap-2 sm:gap-3 min-w-0 flex-1">
            <div className="relative flex-shrink-0">
              <Sparkles className="h-4 w-4 sm:h-5 sm:w-5" />
              {isLoading && (
                <div className="absolute -top-1 -right-1 w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              )}
            </div>
            <div className="min-w-0 flex-1">
              <h3 className="font-semibold text-sm sm:text-base truncate">SQL Assistant</h3>
              <p className="text-xs opacity-90 flex items-center gap-1 truncate">
                {isLoading ? (
                  <>
                    <div className="w-1 h-1 bg-white rounded-full animate-pulse"></div>
                    Typing...
                  </>
                ) : currentPage === 'practice' && currentModule ? (
                  `Helping with ${currentModule}`
                ) : (
                  'Ready to help!'
                )}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-1 sm:gap-2 flex-shrink-0">
            <button
              onClick={clearChat}
              className="p-1.5 sm:p-1 hover:bg-white hover:bg-opacity-20 rounded touch-manipulation"
              title="Clear chat"
            >
              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
            <button
              onClick={toggleFullScreen}
              className="p-1.5 sm:p-1 hover:bg-white hover:bg-opacity-20 rounded touch-manipulation"
              title={isFullScreen ? "Minimize" : "Maximize"}
            >
              {isFullScreen ? (
                <Minimize2 className="h-4 w-4" />
              ) : (
                <Maximize2 className="h-4 w-4" />
              )}
            </button>
            <button
              onClick={() => setIsOpen(false)}
              className="p-1.5 sm:p-1 hover:bg-white hover:bg-opacity-20 rounded touch-manipulation"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* Messages */}
        <div className={`flex-1 overflow-y-auto space-y-3 sm:space-y-4 scrollbar-thin ${
          isFullScreen ? 'p-4 sm:p-6' : 'p-3 sm:p-4'
        }`}>
          {messages.map((message) => (
            <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`${
                isFullScreen ? 'max-w-[70%]' : 'max-w-[90%] sm:max-w-[85%]'
              } ${
                message.type === 'user' 
                  ? 'bg-primary-600 text-white rounded-lg p-2.5 sm:p-3' 
                  : 'bg-white border border-gray-200 rounded-lg shadow-sm'
              }`}>
                {message.type === 'user' ? (
                  <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                ) : (
                  <div className="p-2.5 sm:p-3">
                    {formatMessageContent(message.content).map((part, index) => (
                      <div key={index} className="mb-3 last:mb-0">
                        {part.type === 'markdown' ? (
                          <div className="text-sm text-gray-800 leading-relaxed prose prose-sm max-w-none">
                            <ReactMarkdown
                              components={{
                                h1: ({node, ...props}) => <h1 className="text-lg font-bold text-gray-900 mb-2 mt-4 first:mt-0" {...props} />,
                                h2: ({node, ...props}) => <h2 className="text-base font-bold text-gray-900 mb-2 mt-3 first:mt-0" {...props} />,
                                h3: ({node, ...props}) => <h3 className="text-sm font-bold text-gray-900 mb-1 mt-2 first:mt-0" {...props} />,
                                strong: ({node, ...props}) => <strong className="font-semibold text-gray-900" {...props} />,
                                em: ({node, ...props}) => <em className="italic text-gray-800" {...props} />,
                                p: ({node, ...props}) => <p className="mb-2 last:mb-0" {...props} />,
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
                                onClick={() => copyCodeToClipboard(part.content, `${message.id}-${index}`)}
                                className="flex items-center gap-1 text-xs text-gray-500 hover:text-gray-700 transition-colors"
                              >
                                {copiedCode === `${message.id}-${index}` ? (
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
                                fontSize: '0.8rem',
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
                    
                    {/* Context indicator */}
                    {message.contextAware && (
                      <div className="mt-3 pt-3 border-t border-gray-100 flex items-center gap-1 text-xs text-gray-500">
                        <Target className="h-3 w-3" />
                        Context-aware response
                      </div>
                    )}
                    
                    {/* Suggestions */}
                    {message.suggestions && message.suggestions.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-gray-100 space-y-2">
                        <p className="text-xs font-medium text-gray-600 uppercase tracking-wide">
                          Quick Actions
                        </p>
                        <div className="space-y-1">
                          {message.suggestions.map((suggestion, index) => (
                            <button
                              key={index}
                              onClick={() => handleSuggestionClick(suggestion)}
                              className="block w-full text-left text-xs bg-gray-50 hover:bg-gray-100 text-gray-700 rounded px-3 py-2 transition-colors"
                            >
                              {suggestion}
                            </button>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}
          
            {isLoading && (
            <div className="flex justify-start">
              <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-4 flex items-center gap-3">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                  <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                </div>
                <span className="text-sm text-gray-600">Analyzing your question...</span>
              </div>
            </div>
          )}          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className={`border-t border-gray-200 bg-gray-50 safe-area-padding ${
          isFullScreen ? 'p-4 sm:p-6' : 'p-3 sm:p-4'
        }`}>
          <div className="flex gap-2 mb-2">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me about SQL syntax, JOINs, queries..."
              className="flex-1 resize-none border border-gray-300 rounded-lg px-3 py-2.5 sm:py-2 text-base sm:text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white shadow-sm min-h-[44px] sm:min-h-[32px]"
              rows={1}
              disabled={isLoading}
            />
            <button
              onClick={sendMessage}
              disabled={!inputMessage.trim() || isLoading}
              className={`rounded-lg px-3 py-2 min-w-[44px] min-h-[44px] sm:min-w-[32px] sm:min-h-[32px] transition-all duration-200 touch-manipulation ${
                !inputMessage.trim() || isLoading
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-primary-600 hover:bg-primary-700 active:bg-primary-800 text-white shadow-sm hover:shadow-md'
              }`}
            >
              {isLoading ? (
                <Loader className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
            </button>
          </div>
          
          {/* Quick suggestions */}
          <div className="flex flex-wrap gap-1 mb-2">
            {['SELECT syntax', 'CREATE TABLE', 'JOINs', 'Primary keys'].map((suggestion) => (
              <button
                key={suggestion}
                onClick={() => setInputMessage(suggestion)}
                className="text-xs bg-white hover:bg-gray-100 active:bg-gray-200 text-gray-600 border border-gray-200 rounded-full px-2 py-1.5 sm:py-1 transition-colors touch-manipulation min-h-[32px] sm:min-h-[auto]"
                disabled={isLoading}
              >
                {suggestion}
              </button>
            ))}
          </div>
          
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
            <p className="text-xs text-gray-500 flex items-center gap-1">
              <Target className="h-3 w-3" />
              Context-aware SQL help
            </p>
            <div className="hidden sm:flex items-center gap-1 text-xs text-gray-400">
              <span>Press</span>
              <kbd className="px-1 py-0.5 bg-gray-200 rounded text-xs">Enter</kbd>
              <span>to send</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    </>
  );
};

export default FloatingChatbot;