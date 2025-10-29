import requests
import json

def test_endpoints():
    base_url = "http://localhost:8000/api"
    
    print("Testing backend endpoints...")
    
    # Test health check first
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print(f"Health data: {response.json()}")
    except Exception as e:
        print(f"Failed to connect to health endpoint: {e}")
    
    # Test modules endpoint
    try:
        response = requests.get(f"{base_url}/modules")
        print(f"Modules endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"Modules data: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Failed to connect to modules endpoint: {e}")
    
    # Test question generation
    try:
        response = requests.post(f"{base_url}/practice/question", 
                               json={"module_id": 1})
        print(f"\nQuestion endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Question data keys: {list(data.keys())}")
            print(f"Question text: {data.get('question', 'No question found')[:100]}...")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Failed to connect to question endpoint: {e}")
    
    # Test user progress
    try:
        response = requests.get(f"{base_url}/practice/progress")
        print(f"\nProgress endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Progress data: {data}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Failed to connect to progress endpoint: {e}")

if __name__ == "__main__":
    test_endpoints()