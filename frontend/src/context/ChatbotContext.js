import React, { createContext, useContext, useState, useCallback } from 'react';

const ChatbotContext = createContext();

export const useChatbotContext = () => {
  const context = useContext(ChatbotContext);
  if (!context) {
    throw new Error('useChatbotContext must be used within a ChatbotProvider');
  }
  return context;
};

export const ChatbotProvider = ({ children }) => {
  const [chatbotContext, setChatbotContext] = useState({
    currentPage: '',
    currentModule: '',
    currentQuestion: '',
    userProgress: {}
  });

  const updateContext = useCallback((updates) => {
    setChatbotContext(prev => ({ ...prev, ...updates }));
  }, []);

  return (
    <ChatbotContext.Provider value={{ chatbotContext, updateContext }}>
      {children}
    </ChatbotContext.Provider>
  );
};