-- SQL Learning Chatbot Database Schema
-- SQLite Database Design

-- Learning modules (fixed curriculum)
CREATE TABLE learning_modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    order_index INTEGER NOT NULL,
    difficulty_level TEXT CHECK(difficulty_level IN ('beginner', 'intermediate', 'advanced')) DEFAULT 'beginner',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Questions for each module (generated or predefined)
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    difficulty_level TEXT CHECK(difficulty_level IN ('easy', 'medium', 'hard')) DEFAULT 'medium',
    expected_sql TEXT, -- Optional: model answer
    hints TEXT, -- JSON array of hints
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (module_id) REFERENCES learning_modules(id)
);

-- User progress through modules
CREATE TABLE user_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL, -- Simple string ID for now (no auth)
    module_id INTEGER NOT NULL,
    current_difficulty TEXT CHECK(current_difficulty IN ('easy', 'medium', 'hard')) DEFAULT 'easy',
    questions_attempted INTEGER DEFAULT 0,
    questions_correct INTEGER DEFAULT 0,
    completion_percentage REAL DEFAULT 0.0,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (module_id) REFERENCES learning_modules(id),
    UNIQUE(user_id, module_id)
);

-- Individual question attempts
CREATE TABLE user_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    question_id INTEGER NOT NULL,
    user_sql TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT FALSE,
    llm_feedback TEXT, -- LLM evaluation and explanation
    correct_sql TEXT, -- LLM-provided correct answer
    score REAL, -- 0-1 score from LLM
    attempt_number INTEGER DEFAULT 1, -- Multiple attempts allowed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

-- Cheat sheet entries
CREATE TABLE cheat_sheet_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,
    category TEXT NOT NULL, -- DDL, DML, etc.
    syntax TEXT NOT NULL,
    example TEXT NOT NULL,
    description TEXT,
    tags TEXT, -- JSON array for filtering
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User sessions for analytics
CREATE TABLE user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_end TIMESTAMP,
    questions_attempted INTEGER DEFAULT 0,
    avg_score REAL DEFAULT 0.0
);

-- Insert initial learning modules
INSERT INTO learning_modules (name, description, order_index, difficulty_level) VALUES
('Data Definition and Data Manipulation Language', 'Learn CREATE, ALTER, DROP, INSERT, UPDATE, DELETE statements', 1, 'beginner'),
('Constraints', 'Master PRIMARY KEY, FOREIGN KEY, CHECK, NOT NULL, UNIQUE constraints', 2, 'beginner'),
('Single Row Functions', 'Explore string, numeric, date, and conversion functions', 3, 'intermediate'),
('Operators and Group Functions', 'Understanding WHERE clauses, GROUP BY, HAVING, aggregate functions', 4, 'intermediate'),
('Sub Query, Views and Joins', 'Complex queries with subqueries, creating views, INNER/OUTER joins', 5, 'advanced'),
('High Level Language Extensions', 'Procedures, Functions, Cursors and Triggers for advanced database programming', 6, 'advanced');

-- Insert sample cheat sheet entries
INSERT INTO cheat_sheet_entries (topic, category, syntax, example, description) VALUES
('CREATE TABLE', 'DDL', 'CREATE TABLE table_name (column1 datatype, column2 datatype, ...)', 'CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(255));', 'Creates a new table with specified columns and data types'),
('SELECT', 'DML', 'SELECT column1, column2 FROM table_name WHERE condition', 'SELECT name, email FROM users WHERE age > 18;', 'Retrieves data from one or more tables'),
('INSERT', 'DML', 'INSERT INTO table_name (column1, column2) VALUES (value1, value2)', 'INSERT INTO users (name, email) VALUES (''John'', ''john@email.com'');', 'Adds new records to a table'),
('PRIMARY KEY', 'Constraints', 'column_name datatype PRIMARY KEY', 'id INT PRIMARY KEY', 'Uniquely identifies each record in a table'),
('INNER JOIN', 'Joins', 'SELECT * FROM table1 INNER JOIN table2 ON table1.id = table2.foreign_id', 'SELECT u.name, o.order_date FROM users u INNER JOIN orders o ON u.id = o.user_id;', 'Returns records that have matching values in both tables');