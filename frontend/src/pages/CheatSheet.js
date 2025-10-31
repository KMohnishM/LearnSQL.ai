import React, { useState, useEffect } from 'react';
import { Search, Filter, Copy, Check, Sparkles, X, Loader } from 'lucide-react';
import { apiService } from '../services/api';
import { analytics } from '../services/analytics';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism';
import toast from 'react-hot-toast';

const CheatSheet = () => {
  const [cheatSheetData, setCheatSheetData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [loading, setLoading] = useState(true);
  const [copiedId, setCopiedId] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [dynamicExample, setDynamicExample] = useState(null);
  const [loadingExample, setLoadingExample] = useState(false);

  useEffect(() => {
    fetchCheatSheet();
  }, []);

  useEffect(() => {
    filterData();
  }, [searchTerm, selectedCategory, cheatSheetData]);

  const fetchCheatSheet = async () => {
    try {
      const response = await apiService.getCheatSheet();
      setCheatSheetData(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching cheat sheet:', error);
      toast.error('Failed to load cheat sheet');
      setLoading(false);
    }
  };

  const filterData = () => {
    let filtered = cheatSheetData;

    if (selectedCategory !== 'All') {
      filtered = filtered.filter(item => item.category === selectedCategory);
    }

    if (searchTerm) {
      filtered = filtered.filter(item =>
        item.command.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.category?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.syntax.toLowerCase().includes(searchTerm.toLowerCase())
      );
      
      // Track search events (only when user has typed something)
      if (searchTerm.trim().length > 2) {
        analytics.trackCheatSheetSearch(searchTerm, filtered.length);
      }
    }
    
    setFilteredData(filtered);
  };

  const copyToClipboard = async (text, id) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedId(id);
      toast.success('Copied to clipboard!');
      
      // Track code copy event
      analytics.trackCodeCopy('sql', 'cheatsheet');
      
      setTimeout(() => setCopiedId(null), 2000);
    } catch (error) {
      toast.error('Failed to copy');
    }
  };

  const generateDynamicExample = async (item) => {
    // Validate that we have a command before making the API call
    if (!item.command || !item.command.trim()) {
      toast.error('No command available for this cheat sheet item');
      return;
    }

    setLoadingExample(true);
    setShowModal(true);
    
    try {
      const response = await apiService.getDynamicExample({
        command: item.command,
        syntax: item.syntax || "",
        category: item.category || ""
      });
      
      setDynamicExample(response.data);
      
      // Track dynamic example generation
      analytics.trackDynamicExample(item.command, item.category);
    } catch (error) {
      console.error('Error generating dynamic example:', error);
        toast.error('Failed to generate real-time example');
        setDynamicExample({
          scenario: "Real-Time Scenario",
          business_context: "Unable to generate real-time example at this time.",
          sql_example: item.example,
          explanation: "Please try again later or refer to the static example provided."
        });
    } finally {
      setLoadingExample(false);
    }
  };

  const closeModal = () => {
    setShowModal(false);
    setDynamicExample(null);
  };

  const categories = ['All', ...new Set(cheatSheetData.map(item => item.category))];

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
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">SQL Cheat Sheet</h1>
          <p className="text-sm sm:text-base text-gray-600">Quick reference for SQL syntax and examples</p>
        </div>

        {/* Search and Filter */}
        <div className="flex flex-col gap-3 mb-6 sm:mb-8">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <input
              type="text"
              placeholder="Search SQL commands, syntax..."
              className="w-full pl-10 pr-4 py-3 sm:py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent text-base bg-white shadow-sm"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <div className="relative">
            <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <select
              className="appearance-none w-full pl-10 pr-8 py-3 sm:py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white text-base shadow-sm"
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
            >
              {categories.map((category, index) => (
                <option key={`category-${index}`} value={category}>{category}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Cheat Sheet Grid */}
        <div className="space-y-4 sm:grid sm:grid-cols-2 lg:grid-cols-3 sm:gap-6 sm:space-y-0">
          {filteredData.map((item) => (
            <div key={item.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow duration-200">
              {/* Header with command name and copy button */}
              <div className="flex justify-between items-start mb-3">
                <div className="flex-1 min-w-0">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{item.command}</h3>
                  <span className="inline-block px-2 py-1 text-xs font-medium bg-primary-100 text-primary-800 rounded-full">
                    {item.category}
                  </span>
                </div>
                <button
                  onClick={() => copyToClipboard(item.syntax, item.id)}
                  className="p-3 text-gray-400 hover:text-gray-600 transition-colors touch-manipulation ml-2 flex-shrink-0 min-w-[44px] min-h-[44px] flex items-center justify-center rounded-lg hover:bg-gray-50"
                  title="Copy syntax"
                >
                  {copiedId === item.id ? (
                    <Check className="h-5 w-5 text-green-500" />
                  ) : (
                    <Copy className="h-5 w-5" />
                  )}
                </button>
              </div>

              {/* Description */}
              {item.description && (
                <p className="text-gray-600 text-sm mb-4 leading-relaxed">{item.description}</p>
              )}

              {/* Code sections */}
              <div className="space-y-4">
                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-2">Syntax:</h4>
                  <div className="relative">
                    <SyntaxHighlighter
                      language="sql"
                      style={tomorrow}
                      customStyle={{
                        margin: 0,
                        padding: '12px',
                        fontSize: '13px',
                        borderRadius: '8px',
                        lineHeight: '1.4',
                      }}
                    >
                      {item.syntax}
                    </SyntaxHighlighter>
                  </div>
                </div>

                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-2">Example:</h4>
                  <div className="relative">
                    <SyntaxHighlighter
                      language="sql"
                      style={tomorrow}
                      customStyle={{
                        margin: 0,
                        padding: '12px',
                        fontSize: '13px',
                        borderRadius: '8px',
                        lineHeight: '1.4',
                      }}
                    >
                      {item.example}
                    </SyntaxHighlighter>
                  </div>
                </div>

                {/* Dynamic Example Button */}
                <div className="pt-2">
                  <button
                    onClick={() => generateDynamicExample(item)}
                    disabled={loadingExample}
                    className="w-full flex items-center justify-center gap-2 px-4 py-3 text-sm font-medium text-primary-600 bg-primary-50 hover:bg-primary-100 active:bg-primary-200 rounded-lg transition-colors duration-200 touch-manipulation disabled:opacity-50 disabled:cursor-not-allowed min-h-[44px]"
                  >
                      {loadingExample ? (
                        <>
                          <div className="h-4 w-4 animate-spin rounded-full border-2 border-primary-600 border-t-transparent" />
                          <span>Generating...</span>
                        </>
                      ) : (
                        <>
                          <Sparkles className="h-4 w-4" />
                          <span>Generate Example</span>
                        </>
                      )}
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredData.length === 0 && (
          <div className="text-center py-12 px-4">
            <div className="max-w-sm mx-auto">
              <Search className="h-12 w-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500 text-base">No cheat sheet entries found matching your search.</p>
              <p className="text-gray-400 text-sm mt-2">Try adjusting your search terms or filter.</p>
            </div>
          </div>
        )}        {/* Dynamic Example Modal */}
        {showModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-end sm:items-center justify-center p-0 sm:p-4 z-50">
            <div className="bg-white rounded-t-2xl sm:rounded-xl w-full sm:max-w-4xl max-h-[95vh] sm:max-h-[90vh] overflow-hidden flex flex-col">
              <div className="sticky top-0 bg-white border-b border-gray-200 px-4 sm:px-6 py-4 flex justify-between items-center">
                <h2 className="text-lg sm:text-xl font-bold text-gray-900 flex items-center gap-2">
                  <Sparkles className="h-5 w-5 text-primary-500" />
                  <span>Dynamic Scenario</span>
                </h2>
                <button
                  onClick={closeModal}
                  className="p-3 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100 touch-manipulation min-w-[44px] min-h-[44px] flex items-center justify-center"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
              
              <div className="flex-1 overflow-y-auto p-4 sm:p-6 scrollbar-thin">
                {loadingExample ? (
                  <div className="flex items-center justify-center py-12">
                    <div className="text-center">
                      <Loader className="h-8 w-8 animate-spin text-primary-500 mx-auto mb-4" />
                      <p className="text-base text-gray-600">Generating scenario...</p>
                    </div>
                  </div>
              ) : dynamicExample ? (
                  <div className="space-y-4 sm:space-y-6">
                    {/* Scenario Header */}
                    <div className="bg-gradient-to-r from-primary-50 to-blue-50 rounded-lg p-3 sm:p-4">
                      <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-2">
                        🏢 {dynamicExample.scenario}
                      </h3>
                      <p className="text-sm sm:text-base text-gray-700">{dynamicExample.business_context}</p>
                    </div>                  {/* Table Description */}
                  {dynamicExample.table_description && (
                    <div>
                      <h4 className="text-md font-semibold text-gray-900 mb-2">Database Context:</h4>
                      <p className="text-gray-700 bg-gray-50 rounded-lg p-3">
                        {dynamicExample.table_description}
                      </p>
                    </div>
                  )}

                  {/* SQL Example */}
                  <div>
                    <h4 className="text-md font-semibold text-gray-900 mb-2">SQL Query:</h4>
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
                      {dynamicExample.sql_example}
                    </SyntaxHighlighter>
                  </div>

                  {/* Explanation */}
                  <div>
                    <h4 className="text-md font-semibold text-gray-900 mb-2">Business Impact:</h4>
                    <p className="text-gray-700 bg-blue-50 rounded-lg p-3">
                      {dynamicExample.explanation}
                    </p>
                  </div>

                  {/* Sample Data */}
                  {dynamicExample.sample_data && (
                    <div>
                      <h4 className="text-md font-semibold text-gray-900 mb-2">Expected Results:</h4>
                      <p className="text-gray-700 bg-green-50 rounded-lg p-3">
                        {dynamicExample.sample_data}
                      </p>
                    </div>
                  )}

                  {/* Copy Button */}
                  <div className="flex justify-end pt-4 border-t border-gray-200">
                    <button
                      onClick={() => copyToClipboard(dynamicExample.sql_example, 'modal')}
                      className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
                    >
                      {copiedId === 'modal' ? (
                        <>
                          <Check className="h-4 w-4" />
                          Copied!
                        </>
                      ) : (
                        <>
                          <Copy className="h-4 w-4" />
                          Copy SQL
                        </>
                      )}
                    </button>
                  </div>
                </div>
              ) : null}
            </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CheatSheet;