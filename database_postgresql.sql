-- PostgreSQL Database Schema for SQL Learning Chatbot
-- Converted from SQLite to PostgreSQL

CREATE TABLE learning_modules (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    order_index INTEGER NOT NULL,
    difficulty_level TEXT DEFAULT 'beginner',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    module_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    difficulty_level TEXT DEFAULT 'medium',
    expected_sql TEXT,
    hints TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (module_id) REFERENCES learning_modules(id) ON DELETE CASCADE
);

CREATE TABLE user_progress (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    module_id INTEGER NOT NULL,
    current_difficulty TEXT DEFAULT 'easy',
    questions_attempted INTEGER DEFAULT 0,
    questions_correct INTEGER DEFAULT 0,
    completion_percentage DECIMAL DEFAULT 0.0,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (module_id) REFERENCES learning_modules(id) ON DELETE CASCADE,
    UNIQUE(user_id, module_id)
);

CREATE TABLE user_attempts (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    question_id TEXT NOT NULL, -- Changed to TEXT to support dynamic question IDs
    user_sql TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT FALSE,
    llm_feedback TEXT,
    correct_sql TEXT,
    score DECIMAL,
    attempt_number INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cheat_sheet_entries (
    id SERIAL PRIMARY KEY,
    topic TEXT NOT NULL,
    category TEXT NOT NULL,
    syntax TEXT NOT NULL,
    example TEXT NOT NULL,
    description TEXT,
    tags TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_sessions (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_end TIMESTAMP,
    questions_attempted INTEGER DEFAULT 0,
    avg_score DECIMAL DEFAULT 0.0
);

-- Create indexes for better performance
CREATE INDEX idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX idx_user_attempts_user_id ON user_attempts(user_id);
CREATE INDEX idx_user_attempts_question_id ON user_attempts(question_id);
CREATE INDEX idx_user_attempts_created_at ON user_attempts(created_at);

-- Insert learning modules
INSERT INTO learning_modules (name, description, order_index, difficulty_level) VALUES
('Data Definition and Data Manipulation Language', 'Master database fundamentals including table creation, data types, and basic CRUD operations. Learn CREATE, ALTER, DROP, INSERT, UPDATE, DELETE statements with proper syntax and safety practices. Build foundation skills for database design and data management.', 1, 'beginner'),
('Constraints and Database Integrity', 'Understand data integrity through PRIMARY KEY, FOREIGN KEY, CHECK, NOT NULL, UNIQUE, and DEFAULT constraints. Learn referential integrity, cascade operations, and proper constraint implementation for robust database design.', 2, 'beginner'),
('Single Row Functions', 'Explore comprehensive string manipulation (UPPER, LOWER, SUBSTRING, CONCAT), numeric functions (ROUND, ABS, CEILING), date/time operations (DATEADD, DATEDIFF), and data type conversions. Master data transformation and formatting techniques.', 3, 'intermediate'),
('Operators and Group Functions', 'Master logical operators (AND, OR, IN, LIKE, BETWEEN), aggregate functions (COUNT, SUM, AVG, MIN, MAX), GROUP BY, HAVING, ORDER BY, and result limiting. Build advanced filtering and data analysis skills.', 4, 'intermediate'),
('Subqueries, Views and Joins', 'Advanced multi-table operations including all JOIN types (INNER, LEFT, RIGHT, FULL OUTER, CROSS, SELF), subqueries (scalar, correlated, EXISTS), Common Table Expressions (CTEs), and view management. Master complex query design and optimization.', 5, 'advanced'),
('High-Level Language Extensions', 'Expert-level database programming with stored procedures, user-defined functions, cursors, triggers, dynamic SQL, exception handling, and transaction management. Implement enterprise-level business logic and automation.', 6, 'advanced');

-- Insert cheat sheet entries
INSERT INTO cheat_sheet_entries (topic, category, syntax, example, description) VALUES
('CREATE TABLE', 'DDL', 'CREATE TABLE table_name (column1 datatype, column2 datatype)', 'CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100))', 'Creates a new table with specified columns and data types'),
('SELECT', 'DML', 'SELECT column1, column2 FROM table_name WHERE condition', 'SELECT name, email FROM users WHERE age > 18', 'Retrieves data from one or more tables'),
('INSERT', 'DML', 'INSERT INTO table_name (column1, column2) VALUES (value1, value2)', 'INSERT INTO users (name, email) VALUES (''John'', ''john@example.com'')', 'Adds new records to a table'),
('PRIMARY KEY', 'Constraints', 'column_name datatype PRIMARY KEY', 'id INT PRIMARY KEY', 'Uniquely identifies each record in a table'),
('INNER JOIN', 'Joins', 'SELECT * FROM table1 INNER JOIN table2 ON table1.id = table2.foreign_id', 'SELECT u.name, o.order_date FROM users u INNER JOIN orders o ON u.id = o.user_id', 'Returns records that have matching values in both tables');