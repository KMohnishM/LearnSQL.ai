import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism';

const MarkdownTestComponent = () => {
  const testMarkdown = `**Great job on creating a table!** Now, you're ready to add a primary key to one of its columns. Adding a primary key is a crucial step in table design, as it uniquely identifies each row in your table.

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

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Markdown Formatting Test</h1>
      
      <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-6">
        <h2 className="text-lg font-semibold mb-4">Rendered Output:</h2>
        
        <div className="space-y-4">
          {formatMessageContent(testMarkdown).map((part, index) => (
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
                    <button className="flex items-center gap-1 text-xs text-gray-500 hover:text-gray-700 transition-colors">
                      📋 Copy
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
      
      <div className="mt-8 bg-gray-50 border border-gray-200 rounded-lg p-4">
        <h2 className="text-lg font-semibold mb-2">Raw Markdown:</h2>
        <pre className="text-xs text-gray-600 whitespace-pre-wrap overflow-x-auto">
          {testMarkdown}
        </pre>
      </div>
    </div>
  );
};

export default MarkdownTestComponent;