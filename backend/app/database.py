import os
import asyncpg
import asyncio
from typing import Optional, Dict, List, Any
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/sql_learning')

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

async def get_db_connection():
    """Get an async database connection"""
    return await asyncpg.connect(DATABASE_URL)

def get_sync_db():
    """Get a synchronous database session"""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

async def init_db():
    """Initialize the database with schema"""
    conn = await get_db_connection()
    
    try:
        # Read and execute PostgreSQL schema
        schema_path = os.path.join(os.path.dirname(__file__), "..", "..", "database_postgresql.sql")
        with open(schema_path, 'r') as f:
            schema = f.read()
        
        # Execute each statement separately
        statements = schema.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement:
                await conn.execute(statement)
        
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        await conn.close()

async def execute_query(query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
    """Execute a query and return results"""
    conn = await get_db_connection()
    try:
        if params:
            results = await conn.fetch(query, *params)
        else:
            results = await conn.fetch(query)
        
        # Convert asyncpg Records to dictionaries
        return [dict(row) for row in results]
    finally:
        await conn.close()

async def execute_insert(query: str, params: tuple) -> int:
    """Execute insert and return the last row id"""
    conn = await get_db_connection()
    try:
        # For PostgreSQL, we need to add RETURNING id to get the inserted ID
        if 'RETURNING' not in query.upper():
            query = query.rstrip(';') + ' RETURNING id'
        
        result = await conn.fetchrow(query, *params)
        return result['id'] if result else None
    finally:
        await conn.close()

async def execute_update(query: str, params: Optional[tuple] = None) -> int:
    """Execute update/delete and return affected row count"""
    conn = await get_db_connection()
    try:
        if params:
            result = await conn.execute(query, *params)
        else:
            result = await conn.execute(query)
        
        # Extract row count from result string like "UPDATE 1"
        return int(result.split()[-1]) if result else 0
    finally:
        await conn.close()

# Synchronous wrapper functions for compatibility
def execute_query_sync(query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
    """Synchronous wrapper for execute_query"""
    return asyncio.run(execute_query(query, params))

def execute_insert_sync(query: str, params: tuple) -> int:
    """Synchronous wrapper for execute_insert"""
    return asyncio.run(execute_insert(query, params))

def execute_update_sync(query: str, params: Optional[tuple] = None) -> int:
    """Synchronous wrapper for execute_update"""
    return asyncio.run(execute_update(query, params))