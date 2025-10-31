import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Play, BookOpen, Award, ChevronRight } from 'lucide-react';
import { apiService } from '../services/api';
import { userSession } from '../services/userSession';
import toast from 'react-hot-toast';

const Practice = () => {
  const navigate = useNavigate();
  const [modules, setModules] = useState([]);
  const [userProgress, setUserProgress] = useState([]);
  const [loading, setLoading] = useState(true);
  // Get unique user ID for this browser session
  const [userId] = useState(() => userSession.getUserId());

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [modulesResponse, progressResponse] = await Promise.all([
        apiService.getModules(),
        apiService.getUserProgress(userId)
      ]);
      
      setModules(Array.isArray(modulesResponse.data) ? modulesResponse.data : []);
      setUserProgress(Array.isArray(progressResponse.data) ? progressResponse.data : []);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching practice data:', error);
      toast.error('Failed to load practice data');
      // Set default empty arrays on error
      setModules([]);
      setUserProgress([]);
      setLoading(false);
    }
  };

  const getProgressForModule = (moduleId) => {
    if (!Array.isArray(userProgress)) {
      return {
        questions_attempted: 0,
        questions_correct: 0,
        completion_percentage: 0,
        current_difficulty: 'easy'
      };
    }
    
    return userProgress.find(p => p.module_id === moduleId) || {
      questions_attempted: 0,
      questions_correct: 0,
      completion_percentage: 0,
      current_difficulty: 'easy'
    };
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'easy': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'hard': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getModuleDifficultyColor = (level) => {
    switch (level) {
      case 'beginner': return 'bg-green-100 text-green-800';
      case 'intermediate': return 'bg-yellow-100 text-yellow-800';
      case 'advanced': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const startPractice = (moduleId) => {
    navigate(`/practice/module/${moduleId}`);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-8">
        <div className="mb-6 sm:mb-8">
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">SQL Learning Journey</h1>
          <p className="text-sm sm:text-base text-gray-600">Master SQL through structured practice and adaptive learning</p>
        </div>

        {/* Progress Overview */}
        <div className="grid grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-6 mb-6 sm:mb-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-3 sm:p-4">
            <div className="flex items-center">
              <div className="p-2 rounded-full bg-primary-100 flex-shrink-0">
                <BookOpen className="h-4 w-4 sm:h-5 sm:w-5 text-primary-600" />
              </div>
              <div className="ml-3 min-w-0 flex-1">
                <p className="text-xs sm:text-sm font-medium text-gray-500 truncate">Modules Started</p>
                <p className="text-lg sm:text-xl font-bold text-gray-900">
                  {Array.isArray(userProgress) ? userProgress.filter(p => p.questions_attempted > 0).length : 0} / {Array.isArray(modules) ? modules.length : 0}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-3 sm:p-4">
            <div className="flex items-center">
              <div className="p-2 rounded-full bg-green-100 flex-shrink-0">
                <Award className="h-4 w-4 sm:h-5 sm:w-5 text-green-600" />
              </div>
              <div className="ml-3 min-w-0 flex-1">
                <p className="text-xs sm:text-sm font-medium text-gray-500 truncate">Questions Correct</p>
                <p className="text-lg sm:text-xl font-bold text-gray-900">
                  {Array.isArray(userProgress) ? userProgress.reduce((sum, p) => sum + (p.questions_correct || 0), 0) : 0}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-3 sm:p-4 col-span-2 lg:col-span-1">
            <div className="flex items-center">
              <div className="p-2 rounded-full bg-blue-100 flex-shrink-0">
                <Play className="h-4 w-4 sm:h-5 sm:w-5 text-blue-600" />
              </div>
              <div className="ml-3 min-w-0 flex-1">
                <p className="text-xs sm:text-sm font-medium text-gray-500 truncate">Total Attempts</p>
                <p className="text-lg sm:text-xl font-bold text-gray-900">
                  {Array.isArray(userProgress) ? userProgress.reduce((sum, p) => sum + (p.questions_attempted || 0), 0) : 0}
                </p>
              </div>
            </div>
          </div>
        </div>        {/* Learning Modules */}
        <div className="space-y-4 sm:space-y-6">
          <h2 className="text-xl sm:text-2xl font-bold text-gray-900">Learning Modules</h2>
          
          <div className="grid gap-4 sm:gap-6">
            {modules.map((module) => {
              const progress = getProgressForModule(module.id);
              const isStarted = progress.questions_attempted > 0;
              
              return (
                <div key={module.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 sm:p-6 hover:shadow-md transition-shadow duration-200">
                  {/* Mobile Layout - Stack everything vertically */}
                  <div className="flex flex-col gap-4 sm:hidden">
                    {/* Header Section */}
                    <div className="flex flex-col gap-3">
                      <div className="flex items-start justify-between gap-3">
                        <h3 className="text-lg font-semibold text-gray-900 flex-1">{module.name}</h3>
                        <div className="flex flex-wrap gap-2 justify-end">
                          <span className={`px-2 py-1 text-xs font-medium rounded-full ${getModuleDifficultyColor(module.difficulty_level)}`}>
                            {module.difficulty_level}
                          </span>
                          {isStarted && (
                            <span className={`px-2 py-1 text-xs font-medium rounded-full ${getDifficultyColor(progress.current_difficulty)}`}>
                              Current: {progress.current_difficulty}
                            </span>
                          )}
                        </div>
                      </div>
                      
                      <p className="text-sm text-gray-600 leading-relaxed">{module.description}</p>
                    </div>
                    
                    {/* Progress Section */}
                    {isStarted && (
                      <div className="bg-gray-50 rounded-lg p-3 space-y-3">
                        <div className="flex justify-between items-center text-sm">
                          <span className="text-gray-600 font-medium">Progress</span>
                          <span className="text-primary-600 font-semibold">{progress.completion_percentage.toFixed(1)}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                            style={{ width: `${progress.completion_percentage}%` }}
                          ></div>
                        </div>
                        <div className="flex justify-between text-xs text-gray-500">
                          <span>{progress.questions_attempted} questions attempted</span>
                          <span>{progress.questions_correct} correct</span>
                        </div>
                      </div>
                    )}
                    
                    {/* Action Button - Full width on mobile */}
                    <button
                      onClick={() => startPractice(module.id)}
                      className="w-full btn-primary flex items-center justify-center space-x-2 touch-manipulation"
                    >
                      <Play className="h-4 w-4" />
                      <span>{isStarted ? 'Continue Practice' : 'Start Module'}</span>
                      <ChevronRight className="h-4 w-4" />
                    </button>
                  </div>
                  
                  {/* Desktop Layout - Better positioning */}
                  <div className="hidden sm:flex sm:items-start sm:justify-between sm:gap-6">
                    <div className="flex-1">
                      <div className="flex items-start justify-between gap-3 mb-3">
                        <h3 className="text-xl font-semibold text-gray-900">{module.name}</h3>
                        <div className="flex flex-wrap gap-2">
                          <span className={`px-2 py-1 text-xs font-medium rounded-full ${getModuleDifficultyColor(module.difficulty_level)}`}>
                            {module.difficulty_level}
                          </span>
                          {isStarted && (
                            <span className={`px-2 py-1 text-xs font-medium rounded-full ${getDifficultyColor(progress.current_difficulty)}`}>
                              Current: {progress.current_difficulty}
                            </span>
                          )}
                        </div>
                      </div>
                      
                      <p className="text-base text-gray-600 leading-relaxed mb-4">{module.description}</p>
                    
                      {/* Desktop Progress Section */}
                      {isStarted && (
                        <div className="bg-gray-50 rounded-lg p-4 space-y-3">
                          <div className="flex justify-between items-center text-sm">
                            <span className="text-gray-600 font-medium">Progress</span>
                            <span className="text-primary-600 font-semibold">{progress.completion_percentage.toFixed(1)}%</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                              style={{ width: `${progress.completion_percentage}%` }}
                            ></div>
                          </div>
                          <div className="flex justify-between text-sm text-gray-500">
                            <span>{progress.questions_attempted} questions attempted</span>
                            <span>{progress.questions_correct} correct</span>
                          </div>
                        </div>
                      )}
                    </div>
                    
                    {/* Desktop Action Button - Auto width */}
                    <div className="flex items-end">
                      <button
                        onClick={() => startPractice(module.id)}
                        className="btn-primary flex items-center space-x-2 touch-manipulation whitespace-nowrap"
                      >
                        <Play className="h-4 w-4" />
                        <span>{isStarted ? 'Continue' : 'Start'}</span>
                        <ChevronRight className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Practice;