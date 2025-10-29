import React, { useEffect, useCallback } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { Analytics } from '@vercel/analytics/react';
import { SpeedInsights } from '@vercel/speed-insights/react';
import Navbar from './components/Navbar';
import FloatingChatbot from './components/FloatingChatbot';
import { ChatbotProvider, useChatbotContext } from './context/ChatbotContext';
import CheatSheet from './pages/CheatSheet';
import Practice from './pages/Practice';
import PracticeModule from './pages/PracticeModule';
import Analysis from './pages/Analysis';
import MarkdownTestComponent from './components/MarkdownTestComponent';
import MarkdownDemo from './components/MarkdownDemo';

// Context-aware wrapper component
function AppContent() {
  const location = useLocation();
  const { chatbotContext, updateContext } = useChatbotContext();

  useEffect(() => {
    // Update chatbot context based on current route
    const pathname = location.pathname;
    let currentPage = 'dashboard';
    let currentModule = '';
    
    if (pathname === '/') {
      currentPage = 'cheatsheet';
    } else if (pathname === '/practice') {
      currentPage = 'practice';
    } else if (pathname.startsWith('/practice/module/')) {
      currentPage = 'practice';
      const moduleId = pathname.split('/').pop();
      currentModule = `Module ${moduleId}`;
    } else if (pathname === '/analysis') {
      currentPage = 'analysis';
    }
    
    updateContext({ currentPage, currentModule });
  }, [location.pathname, updateContext]);

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<CheatSheet />} />
          <Route path="/practice" element={<Practice />} />
          <Route path="/practice/module/:moduleId" element={<PracticeModule />} />
          <Route path="/analysis" element={<Analysis />} />
          <Route path="/test-markdown" element={<MarkdownTestComponent />} />
          <Route path="/demo" element={<MarkdownDemo />} />
        </Routes>
      </main>
      <FloatingChatbot />
    </div>
  );
}

function App() {
  return (
    <Router>
      <ChatbotProvider>
        <AppContent />
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 3000,
            style: {
              background: '#363636',
              color: '#fff',
            },
            success: {
              iconTheme: {
                primary: '#10B981',
                secondary: '#fff',
              },
            },
            error: {
              iconTheme: {
                primary: '#EF4444',
                secondary: '#fff',
              },
            },
          }}
        />
        <Analytics />
        <SpeedInsights />
      </ChatbotProvider>
    </Router>
  );
}

export default App;