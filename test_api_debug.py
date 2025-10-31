#!/usr/bin/env python3
"""
Test script to check the API endpoints and data flow
"""

import requests
import json

def test_api_endpoints():
    base_url = "http://127.0.0.1:8000"
    
    print("Testing API endpoints...")
    
    # Test 1: Get modules
    print("\n1. Testing GET /api/modules")
    try:
        response = requests.get(f"{base_url}/api/modules")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Modules found: {len(data) if isinstance(data, list) else 'Invalid data'}")
            if isinstance(data, list) and data:
                print(f"First module: {data[0].get('name', 'No name')} (ID: {data[0].get('id', 'No ID')})")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error testing modules: {e}")
    
    # Test 2: Get user progress with a test user ID
    test_user_id = "user_test_123456789_abcdefghi"
    print(f"\n2. Testing GET /api/user-progress/{test_user_id}")
    try:
        response = requests.get(f"{base_url}/api/user-progress/{test_user_id}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Progress entries: {len(data) if isinstance(data, list) else 'Invalid data'}")
            if isinstance(data, list):
                print(f"Progress data: {json.dumps(data, indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error testing user progress: {e}")

    # Test 3: Test with actual browser user ID format
    import time
    import random
    browser_user_id = f"user_{int(time.time() * 1000)}_{random.randint(100000000, 999999999)}"
    print(f"\n3. Testing with browser-like user ID: {browser_user_id}")
    try:
        response = requests.get(f"{base_url}/api/user-progress/{browser_user_id}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Progress entries: {len(data) if isinstance(data, list) else 'Invalid data'}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error testing browser user ID: {e}")

if __name__ == "__main__":
    test_api_endpoints()