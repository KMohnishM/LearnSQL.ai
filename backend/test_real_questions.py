import requests
import json

def test_real_questions():
    base_url = "http://localhost:8000/api"
    
    print("Testing question generation with LLM...")
    
    try:
        response = requests.post(f"{base_url}/practice/question", 
                               json={"module_id": 1, "difficulty": "easy"})
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Question ID: {data.get('question_id', 'N/A')}")
            print(f"Module: {data.get('module_name', 'N/A')}")
            print(f"Difficulty: {data.get('difficulty', 'N/A')}")
            print(f"\nQuestion text:")
            print(data.get('question', 'No question found'))
            print(f"\nHints: {len(data.get('hints', []))} provided")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    test_real_questions()