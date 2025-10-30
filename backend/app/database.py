import os
from typing import Optional, Dict, List, Any
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/sql_learning')

# SQLAlchemy setup - works in both local and Vercel environments
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    """Initialize the database with schema"""
    try:
        # Read and execute PostgreSQL schema
        schema_path = os.path.join(os.path.dirname(__file__), "..", "..", "database_postgresql.sql")
        if not os.path.exists(schema_path):
            # Fallback to simple schema and convert
            schema_path = os.path.join(os.path.dirname(__file__), "..", "..", "database_simple.sql")
        
        with open(schema_path, 'r') as f:
            schema = f.read()
        
        # Convert SQLite to PostgreSQL if needed
        if 'database_simple.sql' in schema_path:
            schema = schema.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY')
            schema = schema.replace('DATETIME', 'TIMESTAMP')
            schema = schema.replace('REAL', 'DECIMAL')
        
        # Execute schema using SQLAlchemy
        with engine.connect() as conn:
            # Execute each statement separately
            statements = schema.split(';')
            for statement in statements:
                statement = statement.strip()
                if statement and not statement.startswith('--'):
                    try:
                        conn.execute(text(statement))
                        conn.commit()
                    except Exception as e:
                        # Ignore table already exists errors
                        if 'already exists' not in str(e).lower():
                            print(f"Warning executing statement: {e}")
        
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")

def execute_query_sync(query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
    """Execute a query and return results"""
    with engine.connect() as conn:
        if params:
            # Convert tuple to dict for SQLAlchemy
            param_dict = {f'param_{i}': param for i, param in enumerate(params)}
            # Replace %s or ? with :param_0, :param_1, etc.
            formatted_query = query
            for i in range(len(params)):
                if '%s' in formatted_query:
                    formatted_query = formatted_query.replace('%s', f':param_{i}', 1)
                else:
                    formatted_query = formatted_query.replace('?', f':param_{i}', 1)
            result = conn.execute(text(formatted_query), param_dict)
        else:
            result = conn.execute(text(query))
        
        # Convert results to list of dictionaries
        columns = result.keys() if hasattr(result, 'keys') else []
        rows = result.fetchall() if hasattr(result, 'fetchall') else []
        return [dict(zip(columns, row)) for row in rows]

def execute_insert_sync(query: str, params: tuple) -> int:
    """Execute insert and return the last row id"""
    with engine.connect() as conn:
        # For PostgreSQL, add RETURNING id if not present
        if 'RETURNING' not in query.upper():
            query = query.rstrip(';') + ' RETURNING id'
        
        # Convert tuple to dict for SQLAlchemy
        param_dict = {f'param_{i}': param for i, param in enumerate(params)}
        # Replace %s or ? with :param_0, :param_1, etc.
        formatted_query = query
        for i in range(len(params)):
            if '%s' in formatted_query:
                formatted_query = formatted_query.replace('%s', f':param_{i}', 1)
            else:
                formatted_query = formatted_query.replace('?', f':param_{i}', 1)
        
        result = conn.execute(text(formatted_query), param_dict)
        conn.commit()
        
        # Get the returned ID
        row = result.fetchone()
        return row[0] if row else None

def execute_update_sync(query: str, params: Optional[tuple] = None) -> int:
    """Execute update/delete and return affected row count"""
    with engine.connect() as conn:
        if params:
            # Convert tuple to dict for SQLAlchemy
            param_dict = {f'param_{i}': param for i, param in enumerate(params)}
            # Replace %s or ? with :param_0, :param_1, etc.
            formatted_query = query
            for i in range(len(params)):
                if '%s' in formatted_query:
                    formatted_query = formatted_query.replace('%s', f':param_{i}', 1)
                else:
                    formatted_query = formatted_query.replace('?', f':param_{i}', 1)
            result = conn.execute(text(formatted_query), param_dict)
        else:
            result = conn.execute(text(query))
        
        conn.commit()
        return result.rowcount

# Aliases for compatibility
execute_query = execute_query_sync
execute_insert = execute_insert_sync
execute_update = execute_update_sync