#!/usr/bin/env python3
"""
Test the actual API response structure
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.api.cheatsheet import get_cheatsheet
from app.models import CheatSheetEntry
import asyncio
import json

async def test_api_response():
    """Test the actual cheatsheet API response"""
    
    print("Testing cheatsheet API response structure...")
    
    # Call the API function directly
    entries = await get_cheatsheet()
    
    print(f"Got {len(entries)} entries")
    print("First entry structure:")
    
    if entries:
        first_entry = entries[0]
        print(f"Type: {type(first_entry)}")
        
        if isinstance(first_entry, dict):
            print("Raw dict keys:", list(first_entry.keys()))
            print("Sample entry:", first_entry)
        else:
            print("Pydantic model fields:", first_entry.__fields__ if hasattr(first_entry, '__fields__') else 'No __fields__')
            print("Model dump:", first_entry.model_dump() if hasattr(first_entry, 'model_dump') else str(first_entry))

if __name__ == "__main__":
    try:
        asyncio.run(test_api_response())
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()