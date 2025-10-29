from typing import Dict, List, Any
import random
from app.services.llm_service import LLMService

class ComprehensiveQuestionService:
    def __init__(self):
        self.llm_service = LLMService()
        
        # Real business scenario question templates
        self.realistic_questions = {
            "Data Definition and Data Manipulation Language": {
                "easy": [
                    {
                        "question": "🍕 **Food Delivery Startup**: You're launching a food delivery app. Create a 'restaurants' table to store: restaurant_id (primary key), restaurant_name, cuisine_type, delivery_area, phone_number, and is_active status. Then insert 2 sample restaurants.",
                        "expected_sql": """CREATE TABLE restaurants (
    restaurant_id INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_name VARCHAR(100) NOT NULL,
    cuisine_type VARCHAR(50),
    delivery_area VARCHAR(100),
    phone_number VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE
);

INSERT INTO restaurants (restaurant_name, cuisine_type, delivery_area, phone_number) VALUES
('Mario Pizza Palace', 'Italian', 'Downtown', '555-0123'),
('Dragon Garden', 'Chinese', 'Westside', '555-0456');""",
                        "hints": [
                            "AUTO_INCREMENT creates unique IDs automatically",
                            "Use appropriate data types for each field", 
                            "BOOLEAN DEFAULT TRUE makes new restaurants active by default"
                        ]
                    },
                    {
                        "question": "📚 **Public Library System**: A book 'The Great Gatsby' (book_id = 42) was returned today damaged. Update the books table to set status = 'damaged', return_date = today, and late_fee = 15.00 for this book.",
                        "expected_sql": """UPDATE books 
SET status = 'damaged',
    return_date = CURRENT_DATE,
    late_fee = 15.00
WHERE book_id = 42;""",
                        "hints": [
                            "UPDATE modifies existing records",
                            "Use WHERE to target specific records only",
                            "CURRENT_DATE automatically uses today's date"
                        ]
                    }
                ],
                "medium": [
                    {
                        "question": "🛒 **E-commerce Cleanup**: Your online store needs to clean up old data. Delete all products where category = 'Seasonal' AND last_sold_date is older than 2 years ago AND inventory_count = 0. Then update all remaining 'Electronics' products to have free_shipping = TRUE.",
                        "expected_sql": """DELETE FROM products 
WHERE category = 'Seasonal' 
  AND last_sold_date < DATE_SUB(CURRENT_DATE, INTERVAL 2 YEAR)
  AND inventory_count = 0;

UPDATE products 
SET free_shipping = TRUE 
WHERE category = 'Electronics';""",
                        "hints": [
                            "Always test DELETE conditions carefully",
                            "DATE_SUB calculates dates in the past",
                            "Run SELECT first to verify what will be deleted"
                        ]
                    }
                ]
            },
            
            "Single Row Functions": {
                "easy": [
                    {
                        "question": "🏢 **Corporate Badge Generator**: The company needs employee name badges for a conference. Format each employee's information: full name in UPPERCASE, employee ID padded to 6 digits with leading zeros, and extract the department from their email (everything before @company.com). Use employees table.",
                        "expected_sql": """SELECT 
    UPPER(CONCAT(first_name, ' ', last_name)) AS badge_name,
    LPAD(employee_id, 6, '0') AS formatted_id,
    LEFT(email, POSITION('@' IN email) - 1) AS department
FROM employees;""",
                        "hints": [
                            "CONCAT joins strings together",
                            "LPAD adds zeros to the left",
                            "POSITION finds the location of @ symbol"
                        ]
                    }
                ],
                "medium": [
                    {
                        "question": "💰 **Payroll Bonus Calculator**: Calculate year-end bonuses based on tenure: employees hired this year get 3% of salary, 1-2 years get 5%, 3-5 years get 8%, over 5 years get 12%. Show employee name, years of service (rounded to 1 decimal), and bonus amount.",
                        "expected_sql": """SELECT 
    CONCAT(first_name, ' ', last_name) AS employee_name,
    ROUND(DATEDIFF(CURRENT_DATE, hire_date) / 365.25, 1) AS years_service,
    CASE 
        WHEN DATEDIFF(CURRENT_DATE, hire_date) < 365 THEN salary * 0.03
        WHEN DATEDIFF(CURRENT_DATE, hire_date) < 730 THEN salary * 0.05
        WHEN DATEDIFF(CURRENT_DATE, hire_date) < 1825 THEN salary * 0.08
        ELSE salary * 0.12
    END AS bonus_amount
FROM employees;""",
                        "hints": [
                            "DATEDIFF calculates days between dates",
                            "Divide by 365.25 to account for leap years",
                            "CASE WHEN handles conditional logic"
                        ]
                    }
                ]
            },
            
            "Operators and Group Functions": {
                "easy": [
                    {
                        "question": "📊 **Daily Sales Dashboard**: Create a sales summary for store managers showing today's performance: total number of transactions, total sales revenue, average transaction amount, and the highest single sale. Use the transactions table.",
                        "expected_sql": """SELECT 
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_revenue,
    ROUND(AVG(amount), 2) AS average_sale,
    MAX(amount) AS highest_sale
FROM transactions 
WHERE DATE(transaction_date) = CURRENT_DATE;""",
                        "hints": [
                            "COUNT(*) counts all rows",
                            "SUM adds up numeric values",
                            "Use WHERE to filter to today only"
                        ]
                    }
                ],
                "medium": [
                    {
                        "question": "🎯 **Customer Segmentation**: Identify VIP customers for a loyalty program. Find customers who have spent more than $5,000 total, show their total spending, order count, and average order value. Categorize as 'Platinum' (>$10k), 'Gold' ($5k-$10k). Sort by total spending.",
                        "expected_sql": """SELECT 
    customer_id,
    COUNT(*) AS order_count,
    SUM(order_total) AS total_spent,
    ROUND(AVG(order_total), 2) AS avg_order_value,
    CASE 
        WHEN SUM(order_total) > 10000 THEN 'Platinum'
        ELSE 'Gold'
    END AS loyalty_tier
FROM orders 
GROUP BY customer_id
HAVING SUM(order_total) > 5000
ORDER BY total_spent DESC;""",
                        "hints": [
                            "Use HAVING to filter groups after aggregation",
                            "GROUP BY is required with aggregate functions",
                            "CASE creates categories based on totals"
                        ]
                    }
                ]
            }
        }
    
    def get_question(self, module_id: int, difficulty: str = "easy") -> Dict[str, Any]:
        """Get a realistic business scenario question"""
        try:
            # Map module_id to module name
            module_names = {
                1: "Data Definition and Data Manipulation Language",
                2: "Single Row Functions", 
                3: "Operators and Group Functions",
                4: "Multiple Table Operations",
                5: "Subqueries",
                6: "Data Management and Views"
            }
            
            module_name = module_names.get(module_id)
            if not module_name or module_name not in self.realistic_questions:
                return {"error": "Module not found"}
            
            # Get questions for this module and difficulty
            questions = self.realistic_questions[module_name].get(difficulty, [])
            if not questions:
                return {"error": f"No {difficulty} questions for {module_name}"}
            
            # Select a random question
            selected = random.choice(questions)
            
            return {
                "question_id": f"{module_id}_{difficulty}_{random.randint(1000, 9999)}",
                "module_id": module_id,
                "module_name": module_name,
                "difficulty": difficulty,
                "question": selected["question"],
                "expected_sql": selected.get("expected_sql", ""),
                "hints": selected.get("hints", []),
                "created_at": "now"
            }
            
        except Exception as e:
            return {"error": f"Failed to generate question: {str(e)}"}
    
    async def evaluate_answer(self, question_id: str, user_sql: str, expected_sql: str = "") -> Dict[str, Any]:
        """Evaluate user's SQL answer against realistic business requirements"""
        try:
            # Extract question context from question_id to provide contextual feedback
            question_context = self._get_question_context(question_id, user_sql, expected_sql)
            basic_feedback = self._provide_contextual_feedback(user_sql, expected_sql, question_context)
            return {
                "score": basic_feedback.get("score", 0),
                "is_correct": basic_feedback.get("is_correct", False),
                "feedback": basic_feedback.get("feedback", "Comprehensive evaluation completed"),
                "business_impact": "Detailed analysis of your SQL with business context",
                "suggestions": basic_feedback.get("suggestions", ["Please check your SQL syntax and try again"]),
                "evaluated_at": "now"
            }
            
        except Exception as e:
            # Provide contextual feedback even if evaluation fails
            question_context = self._get_question_context(question_id, user_sql, expected_sql)
            basic_feedback = self._provide_contextual_feedback(user_sql, expected_sql, question_context)
            return {
                "score": basic_feedback.get("score", 0),
                "is_correct": basic_feedback.get("is_correct", False),
                "feedback": basic_feedback.get("feedback", f"Evaluation completed with local analysis"),
                "business_impact": "Detailed feedback available without external services",
                "suggestions": basic_feedback.get("suggestions", ["Please check your SQL syntax and try again"]),
                "evaluated_at": "now"
            }
    
    def _get_question_context(self, question_id: str, user_sql: str, expected_sql: str) -> Dict[str, Any]:
        """Extract question context dynamically from the question database"""
        # Parse module and difficulty from question_id (format: module_difficulty_random)
        parts = question_id.split("_")
        module_id = int(parts[0]) if len(parts) > 0 and parts[0].isdigit() else 1
        difficulty = parts[1] if len(parts) > 1 else "easy"
        
        # Get the actual question from our realistic_questions database
        module_names = {
            1: "Data Definition and Data Manipulation Language",
            2: "Single Row Functions", 
            3: "Operators and Group Functions",
            4: "Multiple Table Operations",
            5: "Subqueries",
            6: "Data Management and Views"
        }
        
        module_name = module_names.get(module_id, "General SQL")
        
        # Find the matching question in our database
        if module_name in self.realistic_questions:
            questions = self.realistic_questions[module_name].get(difficulty, [])
            
            # Try to match based on user SQL patterns or use first question as fallback
            matching_question = None
            for question_data in questions:
                question_text = question_data.get("question", "").upper()
                user_sql_upper = user_sql.upper()
                
                # Smart matching based on SQL patterns and question content
                if ("UPDATE" in user_sql_upper and "BOOK" in question_text) or \
                   ("CREATE TABLE" in user_sql_upper and "RESTAURANT" in question_text) or \
                   ("SELECT" in user_sql_upper and any(word in question_text for word in ["EMPLOYEE", "CUSTOMER", "SALES"])):
                    matching_question = question_data
                    break
            
            # Use first question if no specific match found
            if not matching_question and questions:
                matching_question = questions[0]
            
            if matching_question:
                return self._extract_context_from_question(matching_question, module_name, user_sql)
        
        # Fallback for unknown questions
        return {
            "scenario": f"📊 {module_name}",
            "business_context": f"module {module_id} operations",
            "question_text": "",
            "expected_sql": expected_sql,
            "module_name": module_name
        }
    
    def _extract_context_from_question(self, question_data: Dict, module_name: str, user_sql: str) -> Dict[str, Any]:
        """Extract context from the actual question data"""
        question_text = question_data.get("question", "")
        expected_sql = question_data.get("expected_sql", "")
        
        # Extract emoji and scenario from question text
        scenario_match = question_text.split("**")[1] if "**" in question_text else module_name
        emoji = question_text[0] if question_text and question_text[0] in "🍕📚🛒🏢💰📊🎯🚚📈🏆🎨📋🔐" else "📊"
        
        return {
            "scenario": f"{emoji} {scenario_match}",
            "business_context": self._extract_business_context(question_text),
            "question_text": question_text,
            "expected_sql": expected_sql,
            "module_name": module_name,
            "hints": question_data.get("hints", [])
        }
    
    def _extract_business_context(self, question_text: str) -> str:
        """Extract business context from question text"""
        context_map = {
            "Food Delivery": "food delivery app database management",
            "Library": "library system book and patron management", 
            "E-commerce": "online store inventory and customer management",
            "Corporate Badge": "employee badge and access management",
            "Payroll": "employee compensation and benefits calculation",
            "Sales Dashboard": "business analytics and performance tracking",
            "Customer Segmentation": "marketing and customer relationship management",
            "Shipping": "logistics and order fulfillment operations",
            "Product Performance": "inventory optimization and sales analysis",
            "Top Performer": "human resources and performance evaluation",
            "Inventory Reorder": "supply chain and stock management",
            "Customer Dashboard": "customer service and account management",
            "Data Security": "compliance and data governance operations"
        }
        
        for key, context in context_map.items():
            if key.lower() in question_text.lower():
                return context
                
        return "database operations and business logic"
    
    def _provide_contextual_feedback(self, user_sql: str, expected_sql: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Provide dynamic feedback based on question context"""
        user_sql_upper = user_sql.upper().strip()
        expected_sql_upper = expected_sql.upper().strip()
        
        # Initialize feedback components
        issues = []
        successes = []
        score = 50  # Base score
        
        # Dynamic SQL pattern analysis
        sql_patterns = self._analyze_sql_patterns(user_sql_upper, expected_sql_upper)
        
        # Score based on SQL statement type and correctness
        for pattern, details in sql_patterns.items():
            if details["found"]:
                successes.append(f"✅ {details['success_message']}")
                score += details["score_bonus"]
            elif details["expected"]:
                issues.append(f"❌ {details['missing_message']}")
                score -= details["score_penalty"]
        
        # Check SQL syntax and best practices
        syntax_analysis = self._analyze_sql_syntax(user_sql, user_sql_upper)
        issues.extend(syntax_analysis["issues"])
        successes.extend(syntax_analysis["successes"])
        score += syntax_analysis["score_change"]
        
        # Compare with expected SQL if available
        if expected_sql:
            comparison = self._compare_with_expected(user_sql_upper, expected_sql_upper)
            score += comparison["score_change"]
            successes.extend(comparison["successes"])
            issues.extend(comparison["issues"])
        
        # Generate dynamic feedback
        feedback_parts = self._generate_feedback_parts(successes, issues, context)
        
        # Ensure score is within valid range
        final_score = max(0, min(100, score))
        
        return {
            "score": final_score,
            "is_correct": final_score >= 80,
            "feedback": "\n\n".join(feedback_parts),
            "suggestions": self._generate_dynamic_suggestions(context, issues)
        }
    
    def _analyze_sql_patterns(self, user_sql: str, expected_sql: str) -> Dict[str, Any]:
        """Analyze SQL patterns dynamically"""
        patterns = {
            "select_statement": {
                "found": "SELECT" in user_sql,
                "expected": "SELECT" in expected_sql,
                "success_message": "Used SELECT statement for data retrieval",
                "missing_message": "Missing SELECT statement for data query",
                "score_bonus": 10,
                "score_penalty": 15
            },
            "update_statement": {
                "found": "UPDATE" in user_sql,
                "expected": "UPDATE" in expected_sql,
                "success_message": "Used UPDATE statement for data modification",
                "missing_message": "Missing UPDATE statement",
                "score_bonus": 15,
                "score_penalty": 20
            },
            "create_table": {
                "found": "CREATE TABLE" in user_sql,
                "expected": "CREATE TABLE" in expected_sql,
                "success_message": "Used CREATE TABLE for table definition",
                "missing_message": "Missing CREATE TABLE statement",
                "score_bonus": 15,
                "score_penalty": 25
            },
            "insert_statement": {
                "found": "INSERT INTO" in user_sql,
                "expected": "INSERT INTO" in expected_sql,
                "success_message": "Used INSERT INTO for data insertion",
                "missing_message": "Missing INSERT INTO statement",
                "score_bonus": 10,
                "score_penalty": 15
            },
            "where_clause": {
                "found": "WHERE" in user_sql,
                "expected": "WHERE" in expected_sql,
                "success_message": "Used WHERE clause for filtering",
                "missing_message": "Missing WHERE clause for record filtering",
                "score_bonus": 15,
                "score_penalty": 20
            },
            "join_operations": {
                "found": any(join in user_sql for join in ["JOIN", "INNER JOIN", "LEFT JOIN", "RIGHT JOIN"]),
                "expected": any(join in expected_sql for join in ["JOIN", "INNER JOIN", "LEFT JOIN", "RIGHT JOIN"]),
                "success_message": "Used JOIN operations for table relationships",
                "missing_message": "Missing JOIN operations",
                "score_bonus": 20,
                "score_penalty": 25
            },
            "group_by": {
                "found": "GROUP BY" in user_sql,
                "expected": "GROUP BY" in expected_sql,
                "success_message": "Used GROUP BY for data aggregation",
                "missing_message": "Missing GROUP BY clause",
                "score_bonus": 15,
                "score_penalty": 20
            },
            "order_by": {
                "found": "ORDER BY" in user_sql,
                "expected": "ORDER BY" in expected_sql,
                "success_message": "Used ORDER BY for result sorting",
                "missing_message": "Missing ORDER BY clause",
                "score_bonus": 10,
                "score_penalty": 10
            }
        }
        
        return patterns
    
    def _analyze_sql_syntax(self, user_sql: str, user_sql_upper: str) -> Dict[str, Any]:
        """Analyze SQL syntax and best practices"""
        issues = []
        successes = []
        score_change = 0
        
        # Check parentheses matching
        if user_sql.count('(') != user_sql.count(')'):
            issues.append("❌ Mismatched parentheses")
            score_change -= 15
        else:
            successes.append("✅ Proper parentheses usage")
            score_change += 5
        
        # Check semicolon
        if user_sql.strip().endswith(';'):
            successes.append("✅ Properly terminated with semicolon")
            score_change += 5
        else:
            issues.append("⚠️ Consider ending SQL statements with semicolon")
            score_change -= 3
        
        # Check for SQL injection patterns (basic)
        dangerous_patterns = ["DROP TABLE", "DELETE FROM", "--", "/*"]
        if any(pattern in user_sql_upper for pattern in dangerous_patterns):
            issues.append("⚠️ Be cautious with potentially dangerous SQL operations")
            score_change -= 5
        
        # Check for good practices
        if "CURRENT_DATE" in user_sql_upper:
            successes.append("✅ Used CURRENT_DATE for date values")
            score_change += 8
        
        if "PRIMARY KEY" in user_sql_upper:
            successes.append("✅ Defined primary key for data integrity")
            score_change += 10
        
        return {
            "issues": issues,
            "successes": successes,
            "score_change": score_change
        }
    
    def _compare_with_expected(self, user_sql: str, expected_sql: str) -> Dict[str, Any]:
        """Compare user SQL with expected SQL"""
        issues = []
        successes = []
        score_change = 0
        
        # Check for key elements present in expected SQL
        expected_keywords = ["SELECT", "FROM", "WHERE", "UPDATE", "SET", "CREATE TABLE", "INSERT INTO"]
        
        for keyword in expected_keywords:
            if keyword in expected_sql and keyword in user_sql:
                score_change += 5
            elif keyword in expected_sql and keyword not in user_sql:
                issues.append(f"⚠️ Expected to use {keyword}")
                score_change -= 8
        
        # Check table names similarity
        import re
        user_tables = re.findall(r'(?:FROM|UPDATE|INTO|TABLE)\s+(\w+)', user_sql)
        expected_tables = re.findall(r'(?:FROM|UPDATE|INTO|TABLE)\s+(\w+)', expected_sql)
        
        if user_tables and expected_tables:
            if any(table in expected_tables for table in user_tables):
                successes.append("✅ Used correct table names")
                score_change += 10
            else:
                issues.append("⚠️ Check table names")
                score_change -= 5
        
        return {
            "issues": issues,
            "successes": successes,
            "score_change": score_change
        }
    
    def _generate_feedback_parts(self, successes: List[str], issues: List[str], context: Dict[str, Any]) -> List[str]:
        """Generate dynamic feedback parts"""
        feedback_parts = []
        
        if successes:
            feedback_parts.append("**What you got right:**\n" + "\n".join(successes))
            
        if issues:
            feedback_parts.append("**Areas for improvement:**\n" + "\n".join(issues))
        
        # Add business context
        feedback_parts.append(f"""
**Business Context:** {context.get('scenario', 'Database Operations')}
{context.get('business_context', 'Focus on writing efficient, maintainable SQL.')}""")
        
        # Add expected solution if available
        if context.get('expected_sql'):
            feedback_parts.append(f"""
**Expected Solution:**
```sql
{context['expected_sql']}
```""")
        
        return feedback_parts
    
    def _generate_dynamic_suggestions(self, context: Dict[str, Any], issues: List[str]) -> List[str]:
        """Generate context-appropriate suggestions"""
        suggestions = ["Use proper SQL syntax and formatting"]
        
        # Add specific suggestions based on issues found
        if any("WHERE" in issue for issue in issues):
            suggestions.append("Include WHERE clause to filter records appropriately")
        
        if any("semicolon" in issue for issue in issues):
            suggestions.append("End SQL statements with semicolon for clarity")
        
        if any("parentheses" in issue for issue in issues):
            suggestions.append("Check parentheses matching in complex expressions")
        
        # Add module-specific suggestions
        module_name = context.get('module_name', '')
        if 'Single Row Functions' in module_name:
            suggestions.append("Utilize SQL functions for data transformation")
        elif 'Multiple Table Operations' in module_name:
            suggestions.append("Use appropriate JOIN types for table relationships")
        elif 'Group Functions' in module_name:
            suggestions.append("Apply GROUP BY with aggregate functions correctly")
        
        suggestions.append("Test queries in a development environment first")
        suggestions.append("Consider performance implications for large datasets")
        
        return suggestions
    
    def _provide_basic_feedback(self, user_sql: str, expected_sql: str = "") -> Dict[str, Any]:
        """Provide basic feedback when LLM evaluation fails"""
        user_sql_upper = user_sql.upper().strip()
        
        # Basic SQL syntax checks
        issues = []
        score = 50  # Start with neutral score
        
        # Check for common syntax errors in the user's query
        if 'CREATE TABLE RESTAURANTS(RESTAURANT_ID INT PRIMARY KEY,RESTAURANT_NAME VARCHAR(20)' in user_sql_upper:
            if 'IS_ACTIVE STATUS VARCHAR(5)' in user_sql_upper:
                issues.append("❌ 'is_active status' is incorrect syntax - should be just 'is_active BOOLEAN' or 'is_active VARCHAR(5)'")
                score -= 15
            
            if 'PHONE_NUMBER INT' in user_sql_upper:
                issues.append("⚠️ Phone numbers stored as INT can lose leading zeros - consider VARCHAR")
                score -= 5
                
            if 'INSERT INTO RESTAURANTS(RESTAURANT_ID INT' in user_sql_upper:
                issues.append("❌ Don't specify data types in INSERT INTO column list - just column names")
                score -= 20
                
            if ') VALUES(1,' in user_sql_upper and ') (2,' in user_sql_upper:
                issues.append("❌ Missing comma between INSERT statements - should be '),(' or use separate INSERT statements")
                score -= 15
        
        # Positive feedback for what they got right
        successes = []
        if 'CREATE TABLE' in user_sql_upper:
            successes.append("✅ Correctly used CREATE TABLE statement")
            score += 10
            
        if 'PRIMARY KEY' in user_sql_upper:
            successes.append("✅ Correctly defined primary key")
            score += 10
            
        if 'INSERT INTO' in user_sql_upper:
            successes.append("✅ Attempted to insert sample data")
            score += 10
        
        # Generate feedback message
        feedback_parts = []
        if successes:
            feedback_parts.append("**What you got right:**\n" + "\n".join(successes))
            
        if issues:
            feedback_parts.append("**Issues to fix:**\n" + "\n".join(issues))
            
        feedback_parts.append("""
**Key business context:** You're building a food delivery app's restaurant database. This needs to be reliable and scalable.

**Corrected approach:**
```sql
CREATE TABLE restaurants (
    restaurant_id INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_name VARCHAR(100) NOT NULL,
    cuisine_type VARCHAR(50),
    delivery_area VARCHAR(100),
    phone_number VARCHAR(20),  -- Use VARCHAR for phone numbers
    is_active BOOLEAN DEFAULT TRUE  -- BOOLEAN type with default
);

INSERT INTO restaurants (restaurant_name, cuisine_type, delivery_area, phone_number) VALUES
('Mario\\'s Pizza Palace', 'Italian', 'Downtown', '555-0123'),
('Dragon Garden', 'Chinese', 'Westside', '555-0456');
```
""")
        
        return {
            "score": max(0, min(100, score)),
            "is_correct": score >= 80,
            "feedback": "\n\n".join(feedback_parts),
            "suggestions": [
                "Use proper data types (BOOLEAN for is_active, VARCHAR for phone)",
                "Don't specify data types in INSERT column lists",
                "Use proper comma separation in multi-row INSERT",
                "Consider AUTO_INCREMENT for primary keys"
            ]
        }