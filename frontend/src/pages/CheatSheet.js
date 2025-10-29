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
    setLoadingExample(true);
    setShowModal(true);
    
    try {
      const response = await apiService.getDynamicExample({
        command: item.command,
        syntax: item.syntax,
        category: item.category
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
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">SQL Cheat Sheet</h1>
        <p className="text-gray-600">Quick reference for SQL syntax and examples</p>
      </div>

      {/* Search and Filter */}
      <div className="flex flex-col sm:flex-row gap-4 mb-8">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
          <input
            type="text"
            placeholder="Search SQL commands, syntax, or descriptions..."
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        
        <div className="relative">
          <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
          <select
            className="appearance-none pl-10 pr-8 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white"
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
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {filteredData.map((item) => (
          <div key={item.id} className="card hover:shadow-lg transition-shadow duration-200">
            <div className="flex justify-between items-start mb-3">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">{item.command}</h3>
                <span className="inline-block px-2 py-1 text-xs font-medium bg-primary-100 text-primary-800 rounded-full">
                  {item.category}
                </span>
              </div>
              <button
                onClick={() => copyToClipboard(item.syntax, item.id)}
                className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                title="Copy syntax"
              >
                {copiedId === item.id ? (
                  <Check className="h-4 w-4 text-green-500" />
                ) : (
                  <Copy className="h-4 w-4" />
                )}
              </button>
            </div>

            {item.description && (
              <p className="text-gray-600 text-sm mb-4">{item.description}</p>
            )}

            <div className="space-y-3">
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-2">Syntax:</h4>
                <SyntaxHighlighter
                  language="sql"
                  style={tomorrow}
                  customStyle={{
                    margin: 0,
                    padding: '0.75rem',
                    fontSize: '0.875rem',
                    borderRadius: '0.5rem',
                  }}
                >
                  {item.syntax}
                </SyntaxHighlighter>
              </div>

              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-2">Example:</h4>
                <SyntaxHighlighter
                  language="sql"
                  style={tomorrow}
                  customStyle={{
                    margin: 0,
                    padding: '0.75rem',
                    fontSize: '0.875rem',
                    borderRadius: '0.5rem',
                  }}
                >
                  {item.example}
                </SyntaxHighlighter>
              </div>

              {/* Dynamic Example Button */}
              <div className="pt-2">
                <button
                  onClick={() => generateDynamicExample(item)}
                  className="w-full flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-primary-600 bg-primary-50 hover:bg-primary-100 rounded-lg transition-colors duration-200"
                >
                    <Sparkles className="h-4 w-4" />
                    Generate Real-Time Scenario
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredData.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500">No cheat sheet entries found matching your criteria.</p>
        </div>
      )}

      {/* Dynamic Example Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
              <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-primary-500" />
             Dynamic Real-Time Scenario
              </h2>
              <button
                onClick={closeModal}
                className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            
            <div className="p-6">
              {loadingExample ? (
                <div className="flex items-center justify-center py-12">
                  <div className="text-center">
                    <Loader className="h-8 w-8 animate-spin text-primary-500 mx-auto mb-4" />
                <p className="text-gray-600">Generating real-time scenario...</p>
                  </div>
                </div>
              ) : dynamicExample ? (
                <div className="space-y-6">
                  {/* Scenario Header */}
                  <div className="bg-gradient-to-r from-primary-50 to-blue-50 rounded-lg p-4">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      🏢 {dynamicExample.scenario}
                    </h3>
                    <p className="text-gray-700">{dynamicExample.business_context}</p>
                  </div>

                  {/* Table Description */}
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
  );
};

export default CheatSheet;