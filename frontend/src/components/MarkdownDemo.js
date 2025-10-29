import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Copy, Check } from 'lucide-react';

const MarkdownDemo = () => {
  const [copiedCode, setCopiedCode] = useState(null);

  // This is the exact content that was showing formatting issues
  const problemResponse = `**Great job on creating a table!** Now, you're ready to add a primary key to one of its columns. Adding a primary key is a crucial step in table design, as it uniquely identifies each row in your table.

To make a column as a primary key, you'll use the \`ALTER TABLE\` statement in SQL. Here's a step-by-step guide:

### Syntax
\`\`\`sql
ALTER TABLE table_name
ADD CONSTRAINT primary_key_name PRIMARY KEY (column_name);
\`\`\`

* \`table_name\` is the name of your table.
* \`primary_key_name\` is the name you want to give to your primary key constraint.
* \`column_name\` is the name of the column you want to make as the primary key.

### Example
Let's say you have a table called \`employees\` and you want to make the \`employee_id\` column as the primary key. Your SQL statement would look like this:

\`\`\`sql
ALTER TABLE employees
ADD CONSTRAINT pk_employee_id PRIMARY KEY (employee_id);
\`\`\`

### Best Practices
* Choose a column that is unique for each row. Typically, this is an auto-incrementing ID column.
* Primary keys are used in indexing, which can improve query performance.
* You can have only one primary key per table.

Now that you've learned how to add a primary key, I recommend practicing with a sample table to solidify your understanding. You can try creating a table with a primary key in our **Practice Module**. If you need help with table creation or have any questions, feel free to ask!`;

  const formatMessageContent = (content) => {
    const parts = content.split(/```sql\n([\s\S]*?)\n```/g);
    const formattedParts = [];
    
    for (let i = 0; i < parts.length; i++) {
      if (i % 2 === 0) {
        if (parts[i].trim()) {
          formattedParts.push({
            type: 'markdown',
            content: parts[i].trim()
          });
        }
      } else {
        formattedParts.push({
          type: 'sql',
          content: parts[i].trim()
        });
      }
    }
    
    return formattedParts;
  };

  const copyCodeToClipboard = async (code, id) => {
    try {
      await navigator.clipboard.writeText(code);
      setCopiedCode(id);
      setTimeout(() => setCopiedCode(null), 2000);
    } catch (error) {
      console.error('Failed to copy code');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">✅ Markdown Formatting Fixed!</h1>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Before (Raw Text) */}
            <div>
              <h2 className="text-xl font-semibold text-red-600 mb-4">❌ Before (Raw Markdown)</h2>
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 h-96 overflow-y-auto">
                <pre className="text-sm text-gray-700 whitespace-pre-wrap">
                  {problemResponse}
                </pre>
              </div>
              <p className="text-sm text-red-600 mt-2">Issues: **, ###, ` showing as raw text instead of formatting</p>
            </div>

            {/* After (Rendered) */}
            <div>
              <h2 className="text-xl font-semibold text-green-600 mb-4">✅ After (Properly Rendered)</h2>
              <div className="bg-green-50 border border-green-200 rounded-lg p-4 h-96 overflow-y-auto">
                <div className="space-y-3">
                  {formatMessageContent(problemResponse).map((part, index) => (
                    <div key={index}>
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
                              onClick={() => copyCodeToClipboard(part.content, `demo-${index}`)}
                              className="flex items-center gap-1 text-xs text-gray-500 hover:text-gray-700 transition-colors"
                            >
                              {copiedCode === `demo-${index}` ? (
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
                </div>
              </div>
              <p className="text-sm text-green-600 mt-2">Fixed: All markdown elements render properly with beautiful formatting!</p>
            </div>
          </div>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-blue-800 mb-4">🎉 What's Fixed:</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h3 className="font-semibold text-blue-700 mb-2">Markdown Elements:</h3>
              <ul className="text-sm text-blue-600 space-y-1">
                <li>✅ **Bold text** renders properly</li>
                <li>✅ ### Headers are formatted correctly</li>
                <li>✅ `Inline code` has proper styling</li>
                <li>✅ Bullet points display as lists</li>
                <li>✅ *Italic text* works perfectly</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-blue-700 mb-2">Code Features:</h3>
              <ul className="text-sm text-blue-600 space-y-1">
                <li>✅ SQL syntax highlighting</li>
                <li>✅ Copy-to-clipboard functionality</li>
                <li>✅ Proper code block separation</li>
                <li>✅ Dark theme for code blocks</li>
                <li>✅ Responsive layout</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MarkdownDemo;