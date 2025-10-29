import requests
import json

def test_formatted_chatbot():
    base_url = "http://localhost:8000/api"
    
    print("Testing enhanced chatbot with formatting...")
    
    # Test primary key question
    test_message = {
        "message": "I have a table created, now I want to make a column in it as primary key, how to do it?",
        "context": {
            "page": "cheatsheet",
            "module": "",
            "question": "",
            "progress": {}
        }
    }
    
    try:
        response = requests.post(f"{base_url}/chatbot/message", json=test_message)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"\n{'='*50}")
            print("FORMATTED RESPONSE:")
            print(f"{'='*50}")
            print(data.get('response', 'No response'))
            print(f"\n{'='*50}")
            print(f"Context aware: {data.get('context_aware', False)}")
            print(f"Suggestions: {data.get('suggested_actions', [])}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    test_formatted_chatbot()