import requests
import json

def test_chatbot():
    base_url = "http://localhost:8000/api"
    
    print("Testing chatbot endpoints...")
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/chatbot/health")
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print(f"Health: {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
    
    # Test sending a message
    test_message = {
        "message": "How do I write a SELECT query?",
        "context": {
            "page": "practice",
            "module": "Basic Queries",
            "question": "Write a SELECT statement",
            "progress": {"completed": 5, "total": 10}
        }
    }
    
    try:
        response = requests.post(f"{base_url}/chatbot/message", json=test_message)
        print(f"\nMessage endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data.get('response', 'No response')}")
            print(f"Context aware: {data.get('context_aware', False)}")
            print(f"Suggestions: {data.get('suggested_actions', [])}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Message test failed: {e}")

if __name__ == "__main__":
    test_chatbot()