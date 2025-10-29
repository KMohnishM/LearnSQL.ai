import json
import os
from typing import Dict, List, Any
from dotenv import load_dotenv
import httpx
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class ChatbotService:
    def __init__(self):
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.openrouter_base_url = "https://openrouter.ai/api/v1"
        
        # Context memory for the session
        self.conversation_memory = []
        
    async def _call_llm(self, prompt: str, temperature: float = 0.7) -> str:
        """Call LLM with fallback"""
        if not self.openrouter_api_key:
            logger.warning("No OpenRouter API key found, using fallback response")
            return await self._fallback_response(prompt)
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.openrouter_base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.openrouter_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "meta-llama/llama-3.3-8b-instruct:free",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": temperature,
                        "max_tokens": 1000
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"].strip()
                else:
                    logger.error(f"LLM API error: {response.status_code} - {response.text}")
                    return await self._fallback_response(prompt)
                    
        except Exception as e:
            logger.error(f"Error calling LLM: {e}")
            return await self._fallback_response(prompt)
    
    async def _fallback_response(self, prompt: str) -> str:
        """Provide helpful, well-formatted fallback responses"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ["primary key", "constraint", "alter table"]):
            return """**Great job on creating a table!** Now you're ready to add a primary key column. That's a crucial step in table design!

To make a column as primary key, you'll use the **ALTER TABLE** statement with the **ADD CONSTRAINT** clause:

### Syntax
```sql
ALTER TABLE table_name
ADD CONSTRAINT pk_column_name PRIMARY KEY (column_name);
```

### Example
If your table is named `employees` and you want to make the `employee_id` column the primary key:

```sql
ALTER TABLE employees
ADD CONSTRAINT pk_employee_id PRIMARY KEY (employee_id);
```

### Best Practices
* Choose a column that is **unique** for each row
* The column must **not contain NULL values or duplicates**
* Primary keys improve **query performance** through indexing
* You can have only **one primary key per table**

Need help with table creation or have questions? Feel free to ask!"""
        
        elif any(word in prompt_lower for word in ["select", "query", "data"]):
            return """For **SELECT** queries, here's the basic syntax:

### Basic Structure
```sql
SELECT column1, column2 
FROM table_name 
WHERE condition;
```

### Common Patterns
* `SELECT *` - selects all columns
* `SELECT DISTINCT column` - removes duplicates  
* `WHERE column = 'value'` - filters rows
* `ORDER BY column` - sorts results

### Example
```sql
SELECT name, email 
FROM employees 
WHERE department = 'Sales'
ORDER BY name;
```

Need help with **specific clauses** or **joins**?"""
        
        elif any(word in prompt_lower for word in ["create", "table", "database"]):
            return """To **create a table**, use the CREATE TABLE statement:

### Basic Syntax
```sql
CREATE TABLE table_name (
    column1 datatype,
    column2 datatype,
    PRIMARY KEY (column1)
);
```

### Example
```sql
CREATE TABLE employees (
    employee_id INT,
    name VARCHAR(100),
    email VARCHAR(255),
    hire_date DATE,
    PRIMARY KEY (employee_id)
);
```

### Common Data Types
* `INT` - whole numbers
* `VARCHAR(n)` - text up to n characters
* `DATE` - date values
* `DECIMAL(p,s)` - numbers with decimals

What **specific table structure** do you need help with?"""
        
        elif any(word in prompt_lower for word in ["join", "inner", "left", "right"]):
            return """**JOINs** connect tables based on related columns:

```sql
SELECT columns
FROM table1 
INNER JOIN table2 ON table1.id = table2.foreign_id;
```

**JOIN Types:**
- **INNER JOIN** - only matching records
- **LEFT JOIN** - all records from left table
- **RIGHT JOIN** - all records from right table

Which type of **JOIN** are you trying to use?"""
        
        elif any(word in prompt_lower for word in ["update", "modify", "change"]):
            return """**UPDATE** syntax to modify existing data:

```sql
UPDATE table_name 
SET column1 = value1 
WHERE condition;
```

**⚠️ Important:** Always include a **WHERE clause** to avoid updating all rows!

**Example:**
```sql
UPDATE employees 
SET salary = 55000 
WHERE employee_id = 123;
```"""
        
        elif any(word in prompt_lower for word in ["delete", "remove"]):
            return """**DELETE** syntax to remove data:

```sql
DELETE FROM table_name 
WHERE condition;
```

**⚠️ Warning:** Be careful with the **WHERE clause** to avoid deleting all data!

**Example:**
```sql
DELETE FROM employees 
WHERE employee_id = 123;
```"""
        
        elif any(word in prompt_lower for word in ["practice", "learn", "study"]):
            return """Great question! Here's how to **level up your SQL skills**:

📚 **Start with the basics:**
- Practice SELECT queries
- Learn table creation
- Master WHERE clauses

🎯 **Try our practice modules:**  
- Basic Queries → Single Row Functions → JOINs → Subqueries

💡 **Pro tip:** Use the cheat sheet for quick syntax reference!"""
        
        else:
            return """👋 I'm here to help with **SQL questions**! 

**I can help you with:**
- SELECT, INSERT, UPDATE, DELETE queries
- Table creation and modification  
- JOINs and relationships
- Subqueries and advanced topics
- Debugging SQL syntax errors

What **specific SQL concept** would you like to learn about?"""

    async def chat_response(self, user_message: str, page_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate contextual chat response"""
        
        # Build context-aware prompt
        context_info = ""
        if page_context:
            current_page = page_context.get("page", "")
            current_module = page_context.get("module", "")
            current_question = page_context.get("question", "")
            user_progress = page_context.get("progress", {})
            
            context_info = f"""
CURRENT CONTEXT:
- User is on: {current_page} page
- Current module: {current_module}
- Current question: {current_question[:200]}... (if applicable)
- User progress: {user_progress}

"""
        
        # Add conversation memory
        conversation_context = ""
        if self.conversation_memory:
            recent_conversation = self.conversation_memory[-3:]  # Last 3 exchanges
            conversation_context = "RECENT CONVERSATION:\n"
            for exchange in recent_conversation:
                conversation_context += f"User: {exchange['user']}\nBot: {exchange['bot']}\n\n"
        
        # Enhanced context handling for practice questions
        context_specific_info = ""
        if page_context and page_context.get("page") == "practice":
            current_question = page_context.get("question", "")
            current_module = page_context.get("module", "")
            user_progress = page_context.get("progress", {})
            
            context_specific_info = f"""
PRACTICE CONTEXT:
- User is working on: {current_module}
- Current practice question: {current_question}
- Progress: Question {user_progress.get('questionCount', 1)}, Difficulty: {user_progress.get('difficulty', 'easy')}

IMPORTANT: The user is asking about the specific practice question above. Your response should be directly related to helping them solve this particular business scenario and SQL query. Provide hints, explanations, or guidance that relates to their current question.
"""

        system_prompt = f"""You are an expert SQL learning assistant chatbot integrated into a SQL learning platform. You help users with SQL questions, provide guidance, and offer contextual help based on what they're currently working on.

{context_info}
{context_specific_info}
{conversation_context}

FORMATTING RULES:
- Use markdown formatting for better readability
- Wrap SQL code in ```sql code blocks for syntax highlighting
- Use **bold** for important concepts
- Use bullet points for lists
- Keep explanations clear and structured

CAPABILITIES:
- Answer SQL syntax questions with properly formatted code examples
- Explain SQL concepts clearly with step-by-step breakdowns
- Provide business-relevant examples and best practices
- Help debug SQL queries with formatted corrections
- Suggest learning paths and relevant modules
- Give context-aware help based on current page/module
- Provide specific help for practice questions and business scenarios

PERSONALITY:
- Friendly and encouraging tone
- Clear, well-structured explanations
- Provide practical, formatted examples
- Ask clarifying questions when needed
- Guide users to relevant practice modules

RESPONSE FORMAT:
- Start with a brief, friendly acknowledgment of their current context
- Provide main explanation with proper formatting related to their specific question
- Include formatted SQL examples that relate to their current scenario
- End with helpful suggestions or next steps

USER QUESTION: {user_message}

Provide a helpful, well-formatted contextual response. Use SQL code blocks for any SQL syntax. If the user is working on a specific practice question, provide guidance that directly relates to that question and business scenario."""

        try:
            response = await self._call_llm(system_prompt, temperature=0.7)
            
            # Store in conversation memory
            self.conversation_memory.append({
                "user": user_message,
                "bot": response,
                "context": page_context
            })
            
            # Keep only last 10 exchanges
            if len(self.conversation_memory) > 10:
                self.conversation_memory = self.conversation_memory[-10:]
            
            return {
                "response": response,
                "context_aware": bool(page_context),
                "suggested_actions": self._generate_suggested_actions(user_message, page_context)
            }
            
        except Exception as e:
            logger.error(f"Error generating chat response: {e}")
            return {
                "response": await self._fallback_response(user_message),
                "context_aware": False,
                "suggested_actions": ["Visit the cheat sheet for quick reference", "Try the practice modules"]
            }
    
    def _generate_suggested_actions(self, user_message: str, page_context: Dict[str, Any] = None) -> List[str]:
        """Generate helpful action suggestions"""
        suggestions = []
        message_lower = user_message.lower()
        
        if "practice" in message_lower or "learn" in message_lower:
            suggestions.append("🎯 Try the Practice Modules")
            suggestions.append("📚 Check the Cheat Sheet")
        
        elif any(word in message_lower for word in ["join", "multiple", "table"]):
            suggestions.append("🔗 Practice Multiple Table Operations module")
            suggestions.append("📖 Review JOIN examples in cheat sheet")
        
        elif any(word in message_lower for word in ["function", "string", "date"]):
            suggestions.append("⚡ Try Single Row Functions module")
            suggestions.append("🔍 Search cheat sheet for functions")
        
        elif "subquery" in message_lower or "nested" in message_lower:
            suggestions.append("🎯 Practice Subqueries module")
            suggestions.append("💡 Generate dynamic examples for subqueries")
        
        else:
            suggestions.append("📚 Browse the Cheat Sheet")
            suggestions.append("🎯 Start with Practice Modules")
        
        return suggestions[:3]  # Limit to 3 suggestions
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.conversation_memory = []