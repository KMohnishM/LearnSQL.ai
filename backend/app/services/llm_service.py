import os
import httpx
import json
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        
    async def evaluate_sql_answer(self, question: str, user_sql: str, expected_sql: str = None) -> Dict[str, Any]:
        """
        Evaluate user's SQL answer using LLM
        Returns: {
            "is_correct": bool,
            "feedback": str,
            "correct_sql": str,
            "score": float (0-1)
        }
        """
        
        prompt = f"""
You are an expert SQL tutor. Evaluate the student's SQL query and provide helpful feedback.

Question: {question}

Student's SQL: {user_sql}

{"Expected SQL: " + expected_sql if expected_sql else ""}

Please evaluate the student's answer and respond with a JSON object containing:
1. "is_correct": boolean - whether the query is correct
2. "feedback": string - detailed explanation of what's right/wrong and how to improve
3. "correct_sql": string - a corrected version of the SQL if needed
4. "score": float - score between 0 and 1 based on correctness and approach

Focus on:
- Syntax correctness
- Logic correctness
- Best practices
- Performance considerations (if relevant)
- Alternative approaches

Be encouraging and educational in your feedback.
"""

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "meta-llama/llama-3.3-8b-instruct:free",
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are an expert SQL tutor. Always respond with valid JSON."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.3
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    
                    # Try to parse JSON from the response
                    try:
                        evaluation = json.loads(content)
                        return evaluation
                    except json.JSONDecodeError:
                        # Fallback if JSON parsing fails
                        return {
                            "is_correct": False,
                            "feedback": "Sorry, I couldn't evaluate your answer right now. Please try again.",
                            "correct_sql": user_sql,
                            "score": 0.0
                        }
                else:
                    return {
                        "is_correct": False,
                        "feedback": "Error connecting to evaluation service. Please try again.",
                        "correct_sql": user_sql,
                        "score": 0.0
                    }
                    
        except Exception as e:
            print(f"LLM Service Error: {e}")
            return {
                "is_correct": False,
                "feedback": "Error evaluating your answer. Please try again.",
                "correct_sql": user_sql,
                "score": 0.0
            }
    
    async def generate_question(self, module_name: str, difficulty: str) -> Dict[str, str]:
        """
        Generate a realistic, scenario-based SQL question for a specific module and difficulty
        """
        
        scenarios = {
            "Data Definition and Data Manipulation Language": {
                "context": "e-commerce platform database",
                "tables": "customers, orders, products, order_items",
                "business_scenarios": [
                    "Setting up a new product catalog system",
                    "Managing customer registration and profile updates", 
                    "Handling order processing and inventory management",
                    "Creating tables for a loyalty points system"
                ]
            },
            "Constraints": {
                "context": "hospital management system",
                "tables": "patients, doctors, appointments, medical_records",
                "business_scenarios": [
                    "Ensuring patient safety with proper data validation",
                    "Managing doctor scheduling conflicts",
                    "Maintaining referential integrity between patient records",
                    "Enforcing business rules for appointment booking"
                ]
            },
            "Single Row Functions": {
                "context": "employee payroll system",
                "tables": "employees, departments, salaries, time_logs",
                "business_scenarios": [
                    "Calculating monthly payroll with bonuses and deductions",
                    "Generating employee reports with formatted names and dates",
                    "Processing overtime calculations",
                    "Creating employee ID cards with formatted information"
                ]
            },
            "Operators and Group Functions": {
                "context": "sales analytics dashboard",
                "tables": "sales, customers, products, regions, sales_reps",
                "business_scenarios": [
                    "Analyzing quarterly sales performance by region",
                    "Identifying top-performing products and sales reps",
                    "Calculating average order values and customer lifetime value",
                    "Generating executive summary reports for board meetings"
                ]
            },
            "Sub Query, Views and Joins": {
                "context": "online learning platform",
                "tables": "students, courses, enrollments, instructors, assignments, grades",
                "business_scenarios": [
                    "Finding students who haven't completed required courses",
                    "Identifying courses with low completion rates",
                    "Creating instructor performance dashboards",
                    "Generating student transcript reports"
                ]
            },
            "High Level Language Extensions": {
                "context": "banking transaction system",
                "tables": "accounts, transactions, customers, branches",
                "business_scenarios": [
                    "Automating monthly interest calculations",
                    "Processing batch transfers with error handling",
                    "Implementing fraud detection triggers",
                    "Creating stored procedures for account management"
                ]
            }
        }
        
        scenario_info = scenarios.get(module_name, scenarios["Data Definition and Data Manipulation Language"])
        
        prompt = f"""
Create a realistic SQL practice question for: "{module_name}" at {difficulty} difficulty.

CONTEXT: You're working with a {scenario_info['context']} that has tables: {scenario_info['tables']}

BUSINESS SCENARIOS to choose from:
{chr(10).join(f"- {scenario}" for scenario in scenario_info['business_scenarios'])}

REQUIREMENTS:
1. Create a specific business scenario (not just "write a query")
2. Provide realistic table structures and sample data context
3. Make it practically useful for someone working in this domain
4. Include business rules and constraints that matter

DIFFICULTY LEVELS:
- Easy: Simple, single-table operations with clear requirements
- Medium: Multi-table operations, some business logic, moderate complexity
- Hard: Complex business rules, multiple tables, performance considerations

Return JSON with:
{{
  "question_text": "Detailed business scenario with specific requirements and table context",
  "expected_sql": "Working SQL solution that solves the business problem",
  "hints": ["Business-focused hint", "Technical hint", "Best practice hint"],
  "table_context": "Brief description of relevant table structures"
}}

Example of GOOD question:
"Your e-commerce company needs to identify customers who placed orders over $500 in the last 30 days but haven't made a purchase since. The marketing team wants to send them a 'we miss you' email campaign. Write a query using the customers (id, email, name, registration_date) and orders (id, customer_id, order_date, total_amount) tables."

Example of BAD question: 
"Write a SQL query for joins"
"""

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "meta-llama/llama-3.3-8b-instruct:free",
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are an expert SQL instructor. Always respond with valid JSON."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.7
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    
                    try:
                        question_data = json.loads(content)
                        return question_data
                    except json.JSONDecodeError:
                        # Fallback question
                        return {
                            "question_text": f"Write a SQL query for {module_name} ({difficulty} level)",
                            "expected_sql": "SELECT * FROM table_name;",
                            "hints": ["Start with SELECT", "Consider the table structure", "Check your syntax"]
                        }
                else:
                    return {
                        "question_text": f"Write a SQL query for {module_name} ({difficulty} level)",
                        "expected_sql": "SELECT * FROM table_name;",
                        "hints": ["Start with SELECT", "Consider the table structure", "Check your syntax"]
                    }
                    
        except Exception as e:
            print(f"Question Generation Error: {e}")
            return {
                "question_text": f"Write a SQL query for {module_name} ({difficulty} level)",
                "expected_sql": "SELECT * FROM table_name;",
                "hints": ["Start with SELECT", "Consider the table structure", "Check your syntax"]
            }

    async def validate_sql_syntax(self, sql: str) -> Dict[str, Any]:
        """
        Validate SQL syntax using LLM
        Returns: {
            "is_valid": bool,
            "error": str,
            "suggestions": list
        }
        """
        
        prompt = f"""
Please validate this SQL query for syntax errors:

SQL: {sql}

Respond with a JSON object containing:
1. "is_valid": boolean - whether the SQL syntax is correct
2. "error": string - description of any syntax errors found (empty if valid)
3. "suggestions": array of strings - suggestions for fixing any issues

Focus only on syntax validation, not logic or performance.
"""

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "meta-llama/llama-3.3-8b-instruct:free",
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a SQL syntax validator. Always respond with valid JSON."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.1
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    
                    try:
                        validation = json.loads(content)
                        return validation
                    except json.JSONDecodeError:
                        return {
                            "is_valid": True,
                            "error": "",
                            "suggestions": []
                        }
                else:
                    return {
                        "is_valid": True,
                        "error": "",
                        "suggestions": []
                    }
                    
        except Exception as e:
            print(f"SQL Validation Error: {e}")
            return {
                "is_valid": True,
                "error": "",
                "suggestions": []
            }

    async def _make_llm_request(self, prompt: str) -> Dict[str, Any]:
        """
        Generic method to make LLM requests
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "meta-llama/llama-3.3-8b-instruct:free",
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are an expert SQL tutor. Always respond with valid JSON."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.5
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    
                    try:
                        return json.loads(content)
                    except json.JSONDecodeError:
                        return {"error": "Failed to parse response"}
                else:
                    return {"error": f"API request failed: {response.status_code}"}
                    
        except Exception as e:
            print(f"LLM Request Error: {e}")
            return {"error": str(e)}