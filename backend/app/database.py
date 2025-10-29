import sqlite3
import os
from typing import Optional

DATABASE_PATH = "sql_learning.db"

def get_db_connection():
    """Get a database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
    return conn

def init_db():
    """Initialize the database with schema"""
    conn = get_db_connection()
    
    # Read and execute schema
    schema_path = os.path.join(os.path.dirname(__file__), "..", "..", "database_simple.sql")
    with open(schema_path, 'r') as f:
        schema = f.read()
    
    # Execute each statement separately
    statements = schema.split(';')
    for statement in statements:
        statement = statement.strip()
        if statement:
            conn.execute(statement)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def execute_query(query: str, params: Optional[tuple] = None):
    """Execute a query and return results"""
    conn = get_db_connection()
    try:
        if params:
            cursor = conn.execute(query, params)
        else:
            cursor = conn.execute(query)
        
        if query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            return [dict(row) for row in results]
        else:
            conn.commit()
            return cursor.rowcount
    finally:
        conn.close()

def execute_insert(query: str, params: tuple):
    """Execute insert and return the last row id"""
    conn = get_db_connection()
    try:
        cursor = conn.execute(query, params)
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()