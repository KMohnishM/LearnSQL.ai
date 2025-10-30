# SQL Learning Platform

A comprehensive, personalized SQL learning platform with interactive practice modules, intelligent chatbot assistance, progress tracking, and dynamic content generation.

## 🚀 Features

### Core Learning Features
- **🎯 Interactive Learning Journey**: 6 structured modules from basic DDL/DML to advanced procedures and triggers
- **🔄 Adaptive Difficulty**: Questions adjust based on your performance with easy, medium, and hard levels
- **🤖 AI-Powered Evaluation**: Advanced LLM-based feedback on SQL queries with detailed explanations
- **📊 Progress Tracking**: Comprehensive analytics with charts, performance trends, and learning insights
- **📚 Dynamic Cheat Sheet**: Interactive SQL reference with AI-generated business scenario examples
- **💬 Context-Aware Chatbot**: Intelligent assistant that provides help based on your current learning context

### Advanced Features
- **✨ Markdown Formatting**: Beautiful formatted content with syntax highlighting throughout the platform
- **🖥️ Full-Screen Chatbot**: Expandable chatbot interface for detailed conversations
- **📋 Copy-to-Clipboard**: Easy copying of SQL code examples and solutions
- **🎯 Business Scenarios**: Real-world practice questions with realistic business contexts
- **🔍 Smart Analysis**: Personalized learning recommendations based on performance patterns
- **💾 Progress Persistence**: Automatic saving of progress and conversation history

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, high-performance Python web framework
- **PostgreSQL** - Production-ready relational database with asyncpg
- **SQLAlchemy** - Database ORM with async support
- **OpenRouter API** - Advanced LLM integration (meta-llama/llama-3.3-8b-instruct)
- **Gemini 2.0 Flash** - Fallback LLM for enhanced reliability
- **Pydantic** - Data validation and serialization

### Frontend
- **React 18** - Modern React with hooks and context
- **Vite** - Fast build tool and development server
- **Tailwind CSS** - Utility-first CSS framework
- **ReactMarkdown** - Markdown rendering with syntax highlighting
- **React Router** - Client-side routing
- **Recharts** - Interactive charts for analytics
- **React Hot Toast** - Beautiful notifications

## 📁 Project Structure

```
sql-learning-platform/
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── main.py                   # Application entry point
│   │   ├── database.py               # Database connection and utilities
│   │   ├── models.py                 # Pydantic models for API
│   │   ├── api/                      # API route handlers
│   │   │   ├── cheatsheet.py         # Cheat sheet endpoints
│   │   │   ├── simple_practice.py    # Practice module endpoints
│   │   │   ├── analysis.py           # Analytics endpoints
│   │   │   └── chatbot.py            # Chatbot endpoints
│   │   └── services/                 # Business logic services
│   │       ├── chatbot_service.py    # Chatbot conversation logic
│   │       ├── llm_service.py        # LLM integration service
│   │       └── simple_question_service.py  # Question generation
│   ├── requirements.txt              # Python dependencies
│   ├── .env.example                  # Environment variables template
│   ├── database_simple.sql           # Database schema
│   └── README.md                     # Backend documentation
├── frontend/                         # React Frontend
│   ├── src/
│   │   ├── components/               # Reusable components
│   │   │   ├── FloatingChatbot.js    # AI assistant chatbot
│   │   │   └── Navbar.js             # Navigation component
│   │   ├── pages/                    # Page components
│   │   │   ├── CheatSheet.js         # SQL reference page
│   │   │   ├── Practice.js           # Module selection page
│   │   │   ├── PracticeModule.js     # Individual practice module
│   │   │   └── Analysis.js           # Progress analytics page
│   │   ├── context/                  # React context providers
│   │   │   └── ChatbotContext.js     # Chatbot state management
│   │   ├── services/                 # API integration
│   │   │   └── api.js                # HTTP client configuration
│   │   ├── App.jsx                   # Main application component
│   │   └── main.jsx                  # Application entry point
│   ├── package.json                  # Node.js dependencies
│   └── README.md                     # Frontend documentation
└── README.md                         # Main project documentation
```

## 📚 Learning Journey Modules

The platform offers 6 comprehensive modules designed to take you from SQL beginner to advanced practitioner:

1. **📝 Data Definition and Data Manipulation Language (DDL/DML)**
   - CREATE, ALTER, DROP table operations
   - INSERT, UPDATE, DELETE data operations
   - Database schema design principles

2. **🔒 Constraints and Data Integrity**
   - PRIMARY KEY, FOREIGN KEY relationships
   - CHECK, NOT NULL, UNIQUE constraints
   - Referential integrity concepts

3. **🔧 Single Row Functions**
   - String manipulation functions (SUBSTRING, CONCAT, UPPER, LOWER)
   - Numeric functions (ROUND, ABS, CEILING, FLOOR)
   - Date/time functions (NOW, DATE_ADD, DATE_FORMAT)
   - Conversion functions (CAST, CONVERT)

4. **📊 Operators and Group Functions**
   - WHERE clause conditions and operators
   - GROUP BY and HAVING clauses
   - Aggregate functions (COUNT, SUM, AVG, MIN, MAX)
   - Advanced filtering techniques

5. **🔗 Sub Queries, Views, and Joins**
   - Subqueries (correlated and non-correlated)
   - CREATE VIEW statements
   - INNER, LEFT, RIGHT, FULL OUTER JOINs
   - Complex multi-table queries

6. **⚡ High Level Language Extensions**
   - Stored procedures and functions
   - Cursors for row-by-row processing
   - Triggers for automated actions
   - Advanced PL/SQL concepts

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **OpenRouter API Key** ([Get one here](https://openrouter.ai/))

### Backend Setup

1. **Clone and navigate to backend**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup (PostgreSQL Recommended)**
   
   **Option A: Supabase (Recommended for Production)**
   - Create account at https://supabase.com
   - Create new project and get connection string
   
   **Option B: Local PostgreSQL**
   - Install PostgreSQL locally
   - Create database: `createdb sql_learning`
   
   **Option C: Other Cloud PostgreSQL**
   - Neon.tech (generous free tier)
   - Railway.app or ElephantSQL

5. **Environment configuration**
   ```bash
   # Edit backend/.env and configure:
   
   # Database (PostgreSQL recommended)
   DATABASE_URL=postgresql://username:password@localhost:5432/sql_learning
   # OR use your Supabase/cloud connection string
   
   # LLM API Keys
   OPENROUTER_API_KEY=your_api_key_here
   OPENROUTER_MODEL=meta-llama/llama-3.3-8b-instruct:free
   GEMINI_API_KEY=your_gemini_api_key_here
   
   ENVIRONMENT=production
   ```

6. **Initialize database**
   ```bash
   # Database will auto-initialize on first startup
   # Or manually run: python -c "import asyncio; from app.database import init_db; asyncio.run(init_db())"
   ```

7. **Start the backend server**
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`
   
   **Note:** See `POSTGRESQL_MIGRATION.md` for detailed database setup guide.

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

### Access the Application

Open your browser and navigate to `http://localhost:5173` to start learning SQL!

## 📖 Usage Guide

### 1. **Cheat Sheet** (`/`)
- Browse comprehensive SQL reference materials
- Click "Get Business Example" for AI-generated real-world scenarios
- Copy code examples with one click
- Search and filter by categories

### 2. **Practice Modules** (`/practice`)
- Select from 6 structured learning modules
- Answer business scenario questions with SQL
- Receive detailed AI feedback on your solutions
- Progress through adaptive difficulty levels

### 3. **Progress Analytics** (`/analysis`)
- View your learning statistics and performance charts
- Get personalized improvement recommendations
- Track progress across all modules
- Analyze performance trends over time

### 4. **AI Chatbot** (Available on all pages)
- Ask questions about SQL concepts
- Get help with current practice problems
- Receive context-aware assistance
- Toggle between compact and full-screen modes

## 🔧 Development

### Backend Development
- **API Documentation**: Available at `http://localhost:8000/docs` (Swagger UI)
- **Health Check**: `http://localhost:8000/api/health`
- **Database**: SQLite file at `backend/sql_learning.db`

### Frontend Development
- **Hot Reload**: Automatic reloading on file changes
- **Component Structure**: Modular React components with hooks
- **State Management**: React Context for global state
- **Styling**: Tailwind CSS with custom components

### Adding New Features
1. **Backend**: Add routes in `app/api/`, business logic in `app/services/`
2. **Frontend**: Create components in `src/components/`, pages in `src/pages/`
3. **Database**: Update schema in `database_simple.sql` and models in `app/models.py`

## 🧪 Testing

### Backend Testing
```bash
cd backend
python test_chatbot.py          # Test chatbot functionality
python test_evaluation.py       # Test SQL evaluation
python test_llm.py              # Test LLM integration
```

### Frontend Testing
```bash
cd frontend
npm run lint                    # Check code quality
npm run build                   # Build for production
npm run preview                 # Preview production build
```

## 🚀 Production Deployment

### Backend Production
```bash
# Install production dependencies
pip install -r requirements.txt

# Set production environment variables
export OPENROUTER_API_KEY=your_production_key
export OPENROUTER_MODEL=meta-llama/llama-3.3-8b-instruct:free
export GEMINI_API_KEY=your_gemini_production_key

# Run with Gunicorn
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend Production
```bash
# Build for production
npm run build

# Serve static files (example with serve)
npm install -g serve
serve -s dist -l 3000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **OpenRouter** for providing access to advanced language models
- **FastAPI** for the excellent Python web framework
- **React Team** for the powerful frontend library
- **Tailwind CSS** for the utility-first CSS framework

---

**Happy Learning! 🎓 Master SQL with our intelligent, personalized platform.**