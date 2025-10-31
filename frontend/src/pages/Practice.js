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
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 mb-6 sm:mb-8">
          <div className="card">
            <div className="flex items-center">
              <div className="p-2 sm:p-3 rounded-full bg-primary-100">
                <BookOpen className="h-5 w-5 sm:h-6 sm:w-6 text-primary-600" />
              </div>
              <div className="ml-3 sm:ml-4">
                <p className="text-xs sm:text-sm font-medium text-gray-500">Modules Started</p>
                <p className="text-xl sm:text-2xl font-bold text-gray-900">
                  {Array.isArray(userProgress) ? userProgress.length : 0} / {Array.isArray(modules) ? modules.length : 0}
                </p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="p-2 sm:p-3 rounded-full bg-green-100">
                <Award className="h-5 w-5 sm:h-6 sm:w-6 text-green-600" />
              </div>
              <div className="ml-3 sm:ml-4">
                <p className="text-xs sm:text-sm font-medium text-gray-500">Questions Correct</p>
                <p className="text-xl sm:text-2xl font-bold text-gray-900">
                  {Array.isArray(userProgress) ? userProgress.reduce((sum, p) => sum + (p.questions_correct || 0), 0) : 0}
                </p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="p-2 sm:p-3 rounded-full bg-blue-100">
                <Play className="h-5 w-5 sm:h-6 sm:w-6 text-blue-600" />
              </div>
              <div className="ml-3 sm:ml-4">
                <p className="text-xs sm:text-sm font-medium text-gray-500">Total Attempts</p>
                <p className="text-xl sm:text-2xl font-bold text-gray-900">
                  {Array.isArray(userProgress) ? userProgress.reduce((sum, p) => sum + (p.questions_attempted || 0), 0) : 0}
                </p>
              </div>
            </div>
          </div>
      </div>

        {/* Learning Modules */}
        <div className="space-y-4 sm:space-y-6">
          <h2 className="text-xl sm:text-2xl font-bold text-gray-900">Learning Modules</h2>
          
          <div className="grid gap-4 sm:gap-6">
            {modules.map((module) => {
              const progress = getProgressForModule(module.id);
              const isStarted = progress.questions_attempted > 0;
              
              return (
                <div key={module.id} className="card hover:shadow-lg transition-shadow duration-200">
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 sm:gap-6">
                    <div className="flex-1 min-w-0">
                      <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:space-x-3 mb-3">
                        <h3 className="text-lg sm:text-xl font-semibold text-gray-900 truncate">{module.name}</h3>
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
                      
                      <p className="text-sm sm:text-base text-gray-600 mb-4">{module.description}</p>
                    
                    {isStarted && (
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm text-gray-500">
                          <span>Progress</span>
                          <span>{progress.completion_percentage.toFixed(1)}%</span>
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
                    
                    <button
                      onClick={() => startPractice(module.id)}
                      className="w-full sm:w-auto sm:ml-6 btn-primary flex items-center justify-center space-x-2 touch-manipulation"
                    >
                      <Play className="h-4 w-4" />
                      <span>{isStarted ? 'Continue' : 'Start'}</span>
                      <ChevronRight className="h-4 w-4" />
                    </button>
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