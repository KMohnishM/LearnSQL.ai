import requests
import json

def test_dynamic_example():
    base_url = "http://localhost:8000/api"
    
    print("Testing dynamic example generation...")
    
    example_request = {
        "command": "SELECT",
        "syntax": "SELECT column1, column2 FROM table_name WHERE condition;",
        "category": "Basic Queries"
    }
    
    try:
        response = requests.post(f"{base_url}/cheat-sheet/example", json=example_request)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nScenario: {data.get('scenario', 'N/A')}")
            print(f"Business Context: {data.get('business_context', 'N/A')}")
            print(f"\nSQL Example:")
            print(data.get('sql_example', 'N/A'))
            print(f"\nExplanation: {data.get('explanation', 'N/A')}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    test_dynamic_example()