# SQL Learning Platform - Backend API

FastAPI-based backend service for the SQL Learning Platform with LLM integration, practice evaluation, and comprehensive analytics.

## 🚀 Features

- **🔌 RESTful API**: Modern FastAPI with automatic OpenAPI documentation
- **🤖 LLM Integration**: Advanced OpenRouter API integration with meta-llama/llama-3.3-8b-instruct
- **🎯 Smart Evaluation**: Context-aware SQL query evaluation and feedback
- **📊 Analytics Engine**: Comprehensive user progress tracking and insights
- **💬 Intelligent Chatbot**: Context-aware conversational AI assistant
- **🔄 Dynamic Content**: AI-generated practice questions and business scenarios
- **📦 SQLite Database**: Lightweight, embedded database for data persistence

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py                       # FastAPI application entry point
│   ├── database.py                   # Database connection and utilities
│   ├── models.py                     # Pydantic models for request/response
│   ├── api/                          # API route handlers
│   │   ├── __init__.py
│   │   ├── cheatsheet.py             # SQL cheat sheet endpoints
│   │   ├── simple_practice.py        # Practice module endpoints
│   │   ├── analysis.py               # User analytics endpoints
│   │   └── chatbot.py                # Chatbot conversation endpoints
│   └── services/                     # Business logic services
│       ├── __init__.py
│       ├── chatbot_service.py        # Chatbot conversation management
│       ├── llm_service.py            # LLM integration service
│       └── simple_question_service.py # Question generation service
├── requirements.txt                  # Python dependencies
├── .env.example                      # Environment variables template
├── database_simple.sql               # Database schema definition
├── sql_learning.db                   # SQLite database file (auto-generated)
├── venv/                            # Virtual environment (created during setup)
└── README.md                        # This documentation
```

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.8+** with pip
- **OpenRouter API Key** ([Sign up here](https://openrouter.ai/))

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your API key
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 3. Database Initialization

```bash
# Initialize database with schema
python -c "from app.database import init_db; init_db()"
```

### 4. Run the Server

```bash
# Development server with auto-reload
uvicorn app.main:app --reload

# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Health Check
```http
GET /api/health
```
Response:
```json
{
  "status": "healthy",
  "message": "API is running properly"
}
```

## 🔗 API Endpoints

### 1. Cheat Sheet Endpoints

#### Get All Cheat Sheet Entries
```http
GET /api/cheatsheet
```
**Response:** Array of cheat sheet entries
```json
[
  {
    "id": 1,
    "topic": "SELECT Statement",
    "category": "Basic Queries",
    "syntax": "SELECT column1, column2 FROM table_name",
    "example": "SELECT name, age FROM users",
    "description": "Retrieve data from database tables",
    "tags": "select,query,basic",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

#### Get Cheat Sheet by Category
```http
GET /api/cheatsheet/category/{category}
```
**Parameters:**
- `category` (string): Category name (e.g., "Basic Queries", "Joins", "Functions")

#### Search Cheat Sheet
```http
GET /api/cheatsheet/search/{search_term}
```
**Parameters:**
- `search_term` (string): Search term to find in topic, description, or example

#### Generate Dynamic Business Example
```http
POST /api/cheat-sheet/example
```
**Request Body:**
```json
{
  "command": "SELECT",
  "syntax": "SELECT column1, column2 FROM table_name",
  "category": "Basic Queries"
}
```
**Response:**
```json
{
  "business_scenario": "E-commerce Customer Analysis",
  "context": "You work for an online retail company...",
  "example_sql": "SELECT customer_name, total_orders FROM customers",
  "explanation": "This query retrieves customer names and their order counts..."
}
```

### 2. Practice Module Endpoints

#### Get Learning Modules
```http
GET /api/modules
```
**Response:** Array of learning modules
```json
[
  {
    "id": 1,
    "name": "Data Definition and Data Manipulation Language",
    "description": "Learn CREATE, ALTER, DROP, INSERT, UPDATE, DELETE operations",
    "order_index": 1,
    "difficulty_level": "beginner",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

#### Get Specific Module
```http
GET /api/modules/{module_id}
```
**Parameters:**
- `module_id` (integer): Module ID

#### Generate Business Scenario Question
```http
GET /api/modules/{module_id}/business-question?difficulty={difficulty}
```
**Parameters:**
- `module_id` (integer): Module ID (1-6)
- `difficulty` (string): "easy", "medium", or "hard"

**Response:**
```json
{
  "question_id": "q_1704067200_easy",
  "question": "You're working for a restaurant chain...",
  "business_context": "Restaurant Management System",
  "table_schema": "CREATE TABLE restaurants (id INT, name VARCHAR(100)...)",
  "difficulty": "easy",
  "module_id": "1",
  "hints": ["Think about which tables you need to join", "Consider using aggregate functions"],
  "expected_concepts": ["SELECT", "FROM", "WHERE"]
}
```

#### Evaluate User Answer
```http
POST /api/practice/evaluate-business-answer
```
**Request Body:**
```json
{
  "question_id": "q_1704067200_easy",
  "user_sql": "SELECT * FROM restaurants WHERE city = 'New York'",
  "question_context": "Find all restaurants in New York",
  "user_id": "user_123"
}
```
**Response:**
```json
{
  "is_correct": true,
  "score": 0.95,
  "feedback": "Excellent! Your query correctly filters restaurants by city...",
  "strengths": ["Correct use of WHERE clause", "Proper syntax"],
  "improvements": ["Consider specifying columns instead of using *"],
  "corrected_sql": "SELECT name, address FROM restaurants WHERE city = 'New York'",
  "explanation": "Your solution works perfectly..."
}
```

#### Get Practice Question (Alternative endpoint)
```http
POST /api/practice/question
```
**Request Body:**
```json
{
  "module_id": 1,
  "difficulty": "easy"
}
```

#### Validate SQL Syntax
```http
POST /api/practice/validate-sql
```
**Request Body:**
```json
{
  "sql": "SELECT name, age FROM users WHERE age > 25"
}
```
**Response:**
```json
{
  "is_valid": true,
  "error": null
}
```

#### Get User Progress
```http
GET /api/practice/progress/{user_id}
```
**Parameters:**
- `user_id` (string): User identifier

**Response:**
```json
{
  "user_id": "user_123",
  "overall_stats": {
    "total_attempts": 45,
    "correct_answers": 38,
    "accuracy": 84.4
  },
  "module_progress": [
    {
      "module_id": 1,
      "module_name": "DDL/DML",
      "questions_attempted": 12,
      "questions_correct": 10,
      "current_difficulty": "medium"
    }
  ],
  "recommendations": ["Focus on JOIN operations", "Practice subqueries"]
}
```

### 3. Analytics Endpoints

#### Get User Analytics
```http
GET /api/analysis/{user_id}
```
**Response:**
```json
{
  "user_id": "user_123",
  "total_questions_attempted": 45,
  "total_correct": 38,
  "overall_accuracy": 84.4,
  "modules_progress": [
    {
      "module_id": 1,
      "module_name": "DDL/DML",
      "questions_attempted": 12,
      "questions_correct": 10,
      "completion_percentage": 83.3,
      "current_difficulty": "medium",
      "avg_score": 0.87
    }
  ],
  "recent_attempts": [
    {
      "created_at": "2024-01-15T14:30:00",
      "user_sql": "SELECT * FROM users",
      "is_correct": true,
      "score": 0.9,
      "llm_feedback": "Great job!",
      "question_text": "Retrieve all user data",
      "module_name": "DDL/DML"
    }
  ],
  "strengths": ["Strong performance in DDL/DML", "Consistent improvement"],
  "areas_for_improvement": ["Need more practice with Joins", "Focus on optimization"]
}
```

#### Get Detailed Analytics
```http
GET /api/analysis/{user_id}/detailed
```
**Response:**
```json
{
  "performance_over_time": [
    {
      "date": "2024-01-15",
      "avg_score": 0.85,
      "attempts": 5,
      "correct": 4
    }
  ],
  "difficulty_distribution": [
    {
      "difficulty_level": "easy",
      "attempts": 20,
      "avg_score": 0.92,
      "correct": 18
    }
  ],
  "common_mistakes": [
    {
      "llm_feedback": "Missing WHERE clause condition",
      "frequency": 3
    }
  ]
}
```

#### Get Learning Path Suggestions
```http
GET /api/analysis/{user_id}/learning-path
```
**Response:**
```json
{
  "suggestions": [
    {
      "type": "continue_module",
      "module_name": "Joins and Subqueries",
      "reason": "You're at 65% completion. Continue practicing to master this topic.",
      "priority": "high"
    },
    {
      "type": "increase_difficulty",
      "module_name": "DDL/DML",
      "reason": "You're doing well! Try medium difficulty questions.",
      "priority": "medium"
    }
  ]
}
```

### 4. Chatbot Endpoints

#### Send Message to Chatbot
```http
POST /api/chatbot/message
```
**Request Body:**
```json
{
  "message": "How do I use JOIN in SQL?",
  "context": {
    "page": "practice",
    "module": "Joins and Subqueries",
    "question": "Find customers who have placed orders",
    "progress": {
      "questionCount": 5,
      "difficulty": "medium"
    }
  }
}
```
**Response:**
```json
{
  "response": "Great question about JOINs! Since you're working on finding customers who have placed orders, you'll want to use an INNER JOIN...",
  "suggestions": [
    "Try writing a simple INNER JOIN",
    "Practice with LEFT JOIN next",
    "Review the table relationships"
  ]
}
```

#### Clear Chatbot Memory
```http
POST /api/chatbot/clear
```
**Response:**
```json
{
  "message": "Conversation memory cleared"
}
```

#### Chatbot Health Check
```http
GET /api/chatbot/health
```
**Response:**
```json
{
  "status": "healthy",
  "message": "Chatbot service is running"
}
```

## 🗄️ Database Schema

The application uses SQLite with the following main tables:

### learning_modules
- `id` (INTEGER PRIMARY KEY)
- `name` (TEXT)
- `description` (TEXT)
- `order_index` (INTEGER)
- `difficulty_level` (TEXT)
- `created_at` (TIMESTAMP)

### cheat_sheet_entries
- `id` (INTEGER PRIMARY KEY)
- `topic` (TEXT)
- `category` (TEXT)
- `syntax` (TEXT)
- `example` (TEXT)
- `description` (TEXT)
- `tags` (TEXT)
- `created_at` (TIMESTAMP)

### user_attempts
- `id` (INTEGER PRIMARY KEY)
- `user_id` (TEXT)
- `question_id` (TEXT)
- `user_sql` (TEXT)
- `is_correct` (BOOLEAN)
- `llm_feedback` (TEXT)
- `score` (REAL)
- `attempt_number` (INTEGER)
- `created_at` (TIMESTAMP)

### user_progress
- `id` (INTEGER PRIMARY KEY)
- `user_id` (TEXT)
- `module_id` (INTEGER)
- `current_difficulty` (TEXT)
- `questions_attempted` (INTEGER)
- `questions_correct` (INTEGER)
- `completion_percentage` (REAL)
- `last_accessed` (TIMESTAMP)
- `started_at` (TIMESTAMP)

## 🤖 LLM Integration

### OpenRouter Configuration
The application uses OpenRouter API with the following model:
- **Model**: `meta-llama/llama-3.3-8b-instruct`
- **Temperature**: Varies by use case (0.7 for creative content, 0.3 for evaluation)
- **Max Tokens**: 2000

The model is configurable via environment variable `OPENROUTER_MODEL`. If not set, the default used by the application is `meta-llama/llama-3.3-8b-instruct:free`.

**Fallback System**: The application includes a robust fallback system:
1. **Primary**: OpenRouter API with configurable model
2. **Fallback**: Google Gemini 2.0 Flash (requires `GEMINI_API_KEY`)
3. **Final Fallback**: Local static responses for basic functionality

### Use Cases
1. **Question Generation**: Creates realistic business scenario questions
2. **Answer Evaluation**: Provides detailed feedback on SQL queries
3. **Chatbot Responses**: Context-aware conversational assistance
4. **Dynamic Examples**: Generates business-relevant code examples
5. **Progress Analysis**: Personalized learning recommendations

## 🧪 Testing

### Manual Testing
```bash
# Test chatbot functionality
python test_chatbot.py

# Test question evaluation
python test_evaluation.py

# Test LLM integration
python test_llm.py

# Test question generation
python test_real_questions.py
```

### API Testing
```bash
# Test all endpoints
curl http://localhost:8000/api/health
curl http://localhost:8000/api/modules
curl http://localhost:8000/api/cheatsheet
```

## 🚀 Production Deployment

### Environment Variables
```bash
# Required
OPENROUTER_API_KEY=your_production_api_key
OPENROUTER_MODEL=meta-llama/llama-3.3-8b-instruct:free  # optional, override model if needed
GEMINI_API_KEY=your_gemini_api_key_here  # optional, fallback LLM

# Optional
DATABASE_URL=sqlite:///production.db
LOG_LEVEL=INFO
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Gunicorn Production Server
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🛠️ Development

### Adding New Endpoints
1. Create route handler in appropriate file in `app/api/`
2. Add business logic to `app/services/`
3. Update models in `app/models.py` if needed
4. Test with Swagger UI at `/docs`

### Database Migrations
1. Update `database_simple.sql`
2. Create migration script if needed
3. Run `init_db()` to apply changes

### Error Handling
The API uses FastAPI's built-in error handling with custom exceptions:
- `400 Bad Request`: Invalid input parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server errors with detailed messages

## 📊 Monitoring & Logging

### Health Checks
- `/api/health`: General API health
- `/api/chatbot/health`: Chatbot service health

### Logging
Logs are written to console and can be configured for production:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

## 🤝 Contributing

1. Follow FastAPI best practices
2. Add type hints for all functions
3. Include docstrings for all endpoints
4. Test endpoints with example requests
5. Update this README for new features

---

**Built with ❤️ using FastAPI and modern Python practices.**