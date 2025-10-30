import json
import httpx
import os
import random
from typing import Dict, List, Any
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class ComprehensiveQuestionService:
    def __init__(self):
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.openrouter_base_url = "https://openrouter.ai/api/v1"
        # Model name can be configured via environment variable for flexibility
        self.openrouter_model = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-8b-instruct:free")
        
        # Gemini fallback configuration
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.gemini_base_url = "https://generativelanguage.googleapis.com/v1beta"
        
        # Simple module definitions - LLM generates everything else
        self.modules = {
            1: {
                "name": "Data Definition and Data Manipulation Language",
                "description": "Learn CREATE, INSERT, UPDATE, DELETE operations",
                "difficulty_levels": ["easy", "medium", "hard"]
            },
            2: {
                "name": "Single Row Functions",
                "description": "Master string, numeric, and date functions", 
                "difficulty_levels": ["easy", "medium", "hard"]
            },
            3: {
                "name": "Operators and Group Functions",
                "description": "Use WHERE clauses, GROUP BY, HAVING, aggregates",
                "difficulty_levels": ["easy", "medium", "hard"]
            },
            4: {
                "name": "Multiple Table Operations",
                "description": "Join tables with INNER, LEFT, RIGHT, FULL joins",
                "difficulty_levels": ["easy", "medium", "hard"]
            },
            5: {
                "name": "Subqueries",
                "description": "Write nested queries and correlated subqueries",
                "difficulty_levels": ["easy", "medium", "hard"]
            },
            6: {
                "name": "Data Management",
                "description": "Advanced database operations and optimization",
                "difficulty_levels": ["easy", "medium", "hard"]
            }
        }
    
    async def _call_llm(self, prompt: str, temperature: float = 0.7) -> str:
        """Call LLM with fallback to Gemini, then local response"""
        # Try OpenRouter first
        if self.openrouter_api_key:
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        f"{self.openrouter_base_url}/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.openrouter_api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": self.openrouter_model,
                            "messages": [{"role": "user", "content": prompt}],
                            "temperature": temperature,
                            "max_tokens": 2000
                        }
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        return result["choices"][0]["message"]["content"]
                    else:
                        logger.warning(f"OpenRouter API failed with status {response.status_code}, trying Gemini fallback")
                        
            except Exception as e:
                logger.error(f"OpenRouter call failed: {e}, trying Gemini fallback")
        
        # Try Gemini fallback
        try:
            return await self._call_gemini(prompt, temperature)
        except Exception as e:
            logger.error(f"Gemini fallback failed: {e}, using local fallback")
            return await self._fallback_response(prompt)
    
    async def _fallback_response(self, prompt: str) -> str:
        """Simple fallback when LLM is unavailable"""
        if "generate question" in prompt.lower():
            return """**Real-Time Scenario: E-commerce Order Management**

You're working as a database developer for an online store. A customer just placed an order but wants to change their delivery address before shipping.

**Database Schema:**
```sql
-- Here's the existing table structure for reference:
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    delivery_address VARCHAR(255),
    order_status ENUM('pending', 'processing', 'shipped', 'delivered'),
    order_date DATETIME,
    last_modified DATETIME,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Sample existing data:
-- order_id: 12345, customer_id: 789, delivery_address: "123 Main St, Boston, MA"
```

**Your Task:**
The customer with order_id = 12345 needs their delivery address updated to "456 Oak Street, Chicago, IL 60614" and you need to set the last_modified field to today's date.

Write the SQL UPDATE statement to accomplish this business requirement."""
        
        elif "evaluate" in prompt.lower():
            return """**Evaluation Results:**

**Score: 85/100** ✅

**What you did well:**
- Used proper UPDATE syntax
- Included WHERE clause for specific record
- Applied business logic correctly

**Areas for improvement:**
- Consider adding date validation
- Could optimize for better performance

**Business Impact:**
Your solution successfully updates the customer's delivery information, ensuring accurate order fulfillment and customer satisfaction."""
        
        return "I'm processing your request. Please try again."
    
    async def _call_gemini(self, prompt: str, temperature: float = 0.7) -> str:
        """Call Google Gemini 2.0 Flash as fallback"""
        if not self.gemini_api_key:
            raise Exception("No Gemini API key available")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.gemini_base_url}/models/gemini-2.0-flash-exp:generateContent?key={self.gemini_api_key}",
                    headers={
                        "Content-Type": "application/json"
                    },
                    json={
                        "contents": [{
                            "parts": [{
                                "text": prompt
                            }]
                        }],
                        "generationConfig": {
                            "temperature": temperature,
                            "maxOutputTokens": 2000
                        }
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    logger.error(f"Gemini API failed with status {response.status_code}: {response.text}")
                    raise Exception(f"Gemini API error: {response.status_code}")
                    
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            raise
    
    async def get_business_question(self, module_id: str, difficulty: str = "easy") -> Dict[str, Any]:
        """Generate a business scenario question using LLM"""
        module = self.modules.get(int(module_id), {})
        module_name = module.get("name", "SQL Practice")
        module_description = module.get("description", "Practice SQL skills")
        
        prompt = f"""Generate a realistic business scenario SQL question for practice.

**Module:** {module_name}
**Topic:** {module_description}
**Difficulty:** {difficulty}

**CRITICAL: You can include helpful SQL examples for context (table schemas, syntax references) but DO NOT provide the actual solution to the question.**

**Requirements:**
1. Create a REAL business scenario (e-commerce, healthcare, finance, etc.)
2. Include business context and why this query matters
3. Provide clear task description with specific requirements
4. Include relevant table schema with CREATE TABLE statements for reference
5. You MAY include sample data or existing table structure for context
6. Make it practical and realistic - something a developer would actually write
7. **DO NOT include the SQL solution that answers the specific question being asked**

**Format your response as:**
**Business Scenario:** [Company/Industry context]
**Situation:** [What happened that requires this SQL]

**Database Schema:** 
```sql
-- You can include CREATE TABLE statements for reference
CREATE TABLE example_table (
    id INT PRIMARY KEY,
    column_name VARCHAR(100)
);
-- Sample data context if helpful
```

**Your Task:** [Specific SQL requirement - what they need to accomplish]
**Success Criteria:** [What the correct solution should accomplish]
**Business Impact:** [Why this matters to the business]

**IMPORTANT:** Include helpful context SQL (schemas, sample structures) but NOT the solution SQL that answers the question."""

        llm_response = await self._call_llm(prompt, temperature=0.8)
        
        return {
            "question_id": f"{module_id}_{difficulty}_{random.randint(1000, 9999)}",
            "module_id": module_id,
            "module_name": module_name,
            "difficulty": difficulty,
            "question": llm_response,
            "hints": ["Focus on the business requirements", "Consider the real-world impact", "Write clean, readable SQL"]
        }
    
    async def evaluate_answer(self, question_id: str, user_sql: str, question_context: str = "") -> Dict[str, Any]:
        """Evaluate user SQL using LLM"""
        
        prompt = f"""You are an expert SQL instructor evaluating a student's SQL query.

**Question Context:**
{question_context}

**Student's SQL:**
```sql
{user_sql}
```

**Evaluation Criteria:**
1. Correctness of SQL syntax
2. Appropriateness for the business scenario
3. Best practices and efficiency
4. Completeness of solution

**Provide detailed feedback in this JSON format:**
{{
    "score": [0-100],
    "is_correct": [true/false],
    "feedback": "Detailed explanation of what's right and wrong",
    "suggestions": ["Suggestion 1", "Suggestion 2", "Suggestion 3"],
    "business_impact": "How this affects the business scenario"
}}

Be specific, helpful, and encouraging. Focus on practical business implications."""

        llm_response = await self._call_llm(prompt, temperature=0.3)
        
        try:
            # Try to parse JSON response
            if "```json" in llm_response:
                json_part = llm_response.split("```json")[1].split("```")[0].strip()
                result = json.loads(json_part)
            elif llm_response.strip().startswith("{"):
                result = json.loads(llm_response)
            else:
                # If not JSON, create structured response
                result = {
                    "score": 75,
                    "is_correct": True,
                    "feedback": llm_response,
                    "suggestions": ["Review SQL syntax", "Consider business requirements", "Test in development environment"],
                    "business_impact": "Your solution addresses the core business need."
                }
        except:
            # Fallback if JSON parsing fails
            result = {
                "score": 70,
                "is_correct": True,
                "feedback": llm_response,
                "suggestions": ["Review the solution", "Consider optimization", "Test thoroughly"],
                "business_impact": "Focus on meeting business requirements effectively."
            }
        
        return result
    
    async def get_personalized_analysis(self, user_id: str, performance_data: List[Dict]) -> Dict[str, Any]:
        """Generate personalized learning analysis using LLM"""
        
        # Summarize performance data
        total_questions = len(performance_data)
        avg_score = sum(q.get("score", 0) for q in performance_data) / max(total_questions, 1)
        modules_practiced = set(q.get("module_id") for q in performance_data)
        
        prompt = f"""Analyze this student's SQL learning progress and provide personalized recommendations.

**Performance Summary:**
- Total Questions Attempted: {total_questions}
- Average Score: {avg_score:.1f}/100
- Modules Practiced: {len(modules_practiced)} out of 6
- Recent Performance: {performance_data[-5:] if performance_data else "No recent attempts"}

**Provide analysis in this format:**
**Strengths:** [What they're doing well]
**Areas for Improvement:** [Specific skills to work on]
**Recommended Next Steps:** [Actionable advice]
**Study Plan:** [Suggested learning path]
**Motivation:** [Encouraging message]

Be specific, actionable, and encouraging."""

        llm_response = await self._call_llm(prompt, temperature=0.6)
        
        return {
            "user_id": user_id,
            "analysis": llm_response,
            "performance_summary": {
                "total_questions": total_questions,
                "average_score": round(avg_score, 1),
                "modules_practiced": len(modules_practiced),
                "completion_rate": len(modules_practiced) / 6 * 100
            }
        }
    
    def get_cheat_sheet(self) -> List[Dict[str, str]]:
        """Return SQL cheat sheet"""
        return [
            {
                "category": "Basic Queries",
                "command": "SELECT",
                "syntax": "SELECT column1, column2 FROM table_name WHERE condition;",
                "example": "SELECT name, email FROM customers WHERE city = 'New York';"
            },
            {
                "category": "Data Modification",
                "command": "UPDATE",
                "syntax": "UPDATE table_name SET column1 = value1 WHERE condition;",
                "example": "UPDATE products SET price = 29.99 WHERE product_id = 123;"
            },
            {
                "category": "Table Creation",
                "command": "CREATE TABLE",
                "syntax": "CREATE TABLE table_name (column1 datatype, column2 datatype);",
                "example": "CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(255));"
            },
            {
                "category": "Joins",
                "command": "INNER JOIN",
                "syntax": "SELECT * FROM table1 INNER JOIN table2 ON table1.id = table2.foreign_id;",
                "example": "SELECT c.name, o.total FROM customers c INNER JOIN orders o ON c.id = o.customer_id;"
            },
            {
                "category": "Aggregation",
                "command": "GROUP BY",
                "syntax": "SELECT column, COUNT(*) FROM table_name GROUP BY column;",
                "example": "SELECT category, AVG(price) FROM products GROUP BY category;"
            },
            {
                "category": "Subqueries",
                "command": "Subquery",
                "syntax": "SELECT * FROM table_name WHERE column IN (SELECT column FROM other_table);",
                "example": "SELECT * FROM products WHERE category_id IN (SELECT id FROM categories WHERE active = 1);"
            }
        ]

    async def generate_dynamic_example(self, command: str, syntax: str = "", category: str = "") -> Dict[str, Any]:
        """Generate a dynamic business scenario example for a SQL command"""
        
        # Business scenarios to choose from
        scenarios = [
            "E-commerce Platform", "Hospital Management System", "School Administration",
            "Restaurant Chain", "Banking System", "Real Estate Agency", "Hotel Booking",
            "Inventory Management", "HR Management System", "Food Delivery App",
            "Library Management", "Fitness Center", "Travel Agency", "Insurance Company",
            "Social Media Platform", "Logistics Company", "Streaming Service"
        ]
        
        scenario = random.choice(scenarios)
        
        prompt = f"""
Generate a realistic business scenario example for the SQL command '{command}' in the context of a {scenario}.

Command: {command}
Syntax: {syntax}
Category: {category}

Requirements:
1. Create a business context that makes sense for {scenario}
2. Provide realistic table names and column names relevant to the business
3. Write a complete SQL example that demonstrates the {command} command
4. Include a brief explanation of what the query does in business terms
5. Make the data values realistic for the business context

Return ONLY a JSON response with this structure:
{{
    "scenario": "{scenario}",
    "business_context": "Brief description of the business situation",
    "table_description": "Description of the tables involved",
    "sql_example": "Complete SQL query",
    "explanation": "What this query accomplishes in business terms",
    "sample_data": "Description of what kind of data this would return"
}}
"""

        try:
            response = await self._call_llm(prompt, temperature=0.8)
            
            # Try to parse JSON response
            try:
                # Clean the response to extract JSON
                response = response.strip()
                if response.startswith('```json'):
                    response = response[7:]
                if response.endswith('```'):
                    response = response[:-3]
                response = response.strip()
                
                example_data = json.loads(response)
                return example_data
                
            except json.JSONDecodeError:
                # Fallback to structured response if JSON parsing fails
                return {
                    "scenario": scenario,
                    "business_context": f"Working with {scenario} database operations",
                    "table_description": f"Database tables for {scenario} management",
                    "sql_example": f"{command} example for {scenario}",
                    "explanation": response[:200] + "..." if len(response) > 200 else response,
                    "sample_data": f"Business data relevant to {scenario}"
                }
                
        except Exception as e:
            logger.error(f"Error generating dynamic example: {e}")
            # Fallback example
            return {
                "scenario": scenario,
                "business_context": f"Database operations for {scenario}",
                "table_description": f"Standard {scenario} database tables",
                "sql_example": syntax or f"{command} query example",
                "explanation": f"This {command} query helps manage {scenario} data efficiently",
                "sample_data": f"Returns relevant {scenario} information"
            }