# Quick Start Guide

## Prerequisites
- Python 3.8+ 
- Node.js 16+
- OpenRouter API key (get from https://openrouter.ai/)

## Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create .env file:
```bash
copy .env.example .env
```
Then edit `.env` and add your OpenRouter API key:
```
OPENROUTER_API_KEY=your_actual_api_key_here
DATABASE_URL=sqlite:///./sql_learning.db
```

5. Initialize database:
```bash
python -c "from app.database import init_db; init_db()"
```

6. Start backend server:
```bash
uvicorn app.main:app --reload
```
Backend will run on http://localhost:8000

## Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```
Frontend will run on http://localhost:3000

## Features

### 🏠 Landing Page - Cheat Sheet
- Comprehensive SQL reference with syntax and examples
- Search and filter by category (DDL, DML, Constraints, etc.)
- Copy-to-clipboard functionality
- Syntax highlighting

### 🧠 Practice Section
- 6 structured learning modules:
  1. Data Definition and Data Manipulation Language
  2. Constraints 
  3. Single Row Functions
  4. Operators and Group Functions
  5. Sub Query, Views and Joins
  6. High Level Language Extensions
- Adaptive difficulty (easy → medium → hard)
- AI-powered evaluation and feedback
- Progress tracking per module

### 📊 Analysis Section
- Overall performance metrics
- Progress charts and visualizations
- Module-wise performance breakdown
- Personalized learning recommendations
- Recent attempts history
- Strengths and improvement areas

## API Documentation

Backend API is available at http://localhost:8000/docs (Swagger UI)

Key endpoints:
- `GET /api/cheatsheet` - Get cheat sheet entries
- `GET /api/modules` - Get learning modules
- `POST /api/practice/submit` - Submit SQL answer for evaluation
- `GET /api/analysis/{user_id}` - Get user analytics

## User Flow

1. **Start** → Landing page shows SQL cheat sheet
2. **Practice** → Select a learning module
3. **Question** → AI generates questions based on difficulty
4. **Submit** → User enters SQL query
5. **Feedback** → AI evaluates and provides detailed feedback
6. **Adapt** → System adjusts difficulty based on performance
7. **Progress** → Track improvement in Analysis section

## Tech Stack

- **Frontend**: React 18, Vite, Tailwind CSS, React Router
- **Backend**: FastAPI, SQLite, Pydantic
- **AI**: OpenRouter API (GPT-3.5-turbo)
- **Charts**: Recharts
- **Syntax**: React Syntax Highlighter

## Development Notes

- No authentication required for MVP
- Simple user ID system (`user_123`) for demo
- Questions generated dynamically by AI
- Adaptive difficulty based on recent performance
- Comprehensive progress tracking and analytics