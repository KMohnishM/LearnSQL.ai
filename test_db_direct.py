#!/usr/bin/env python3
"""
Test database query directly
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.database import execute_query_sync
import json

def test_db_query():
    """Test the database query directly"""
    
    print("Testing database query for cheatsheet...")
    
    query = "SELECT * FROM cheat_sheet_entries ORDER BY category, topic LIMIT 3"
    entries = execute_query_sync(query)
    
    print(f"Raw database response ({len(entries)} entries):")
    for i, entry in enumerate(entries):
        print(f"\nEntry {i+1}:")
        print(f"  Type: {type(entry)}")
        print(f"  Keys: {list(entry.keys()) if isinstance(entry, dict) else 'Not dict'}")
        print(f"  Data: {entry}")
    
    # Test what happens when we try to access 'command' vs 'topic'
    if entries:
        first = entries[0]
        print(f"\nTesting field access on first entry:")
        print(f"  first.get('topic'): {first.get('topic') if isinstance(first, dict) else 'N/A'}")
        print(f"  first.get('command'): {first.get('command') if isinstance(first, dict) else 'N/A'}")

if __name__ == "__main__":
    test_db_query()