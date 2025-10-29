from fastapi import APIRouter
from typing import List
from app.models import CheatSheetEntry
from app.database import execute_query

router = APIRouter()

@router.get("/cheatsheet", response_model=List[CheatSheetEntry])
async def get_cheatsheet():
    """Get all cheat sheet entries"""
    query = "SELECT * FROM cheat_sheet_entries ORDER BY category, topic"
    entries = execute_query(query)
    return entries

@router.get("/cheatsheet/category/{category}")
async def get_cheatsheet_by_category(category: str):
    """Get cheat sheet entries by category"""
    query = "SELECT * FROM cheat_sheet_entries WHERE category = ? ORDER BY topic"
    entries = execute_query(query, (category,))
    return entries

@router.get("/cheatsheet/search/{search_term}")
async def search_cheatsheet(search_term: str):
    """Search cheat sheet entries"""
    query = """
    SELECT * FROM cheat_sheet_entries 
    WHERE topic LIKE ? OR description LIKE ? OR example LIKE ?
    ORDER BY topic
    """
    search_pattern = f"%{search_term}%"
    entries = execute_query(query, (search_pattern, search_pattern, search_pattern))
    return entries