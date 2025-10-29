import requests

def test_cheatsheet():
    base_url = "http://localhost:8000/api"
    
    try:
        response = requests.get(f"{base_url}/cheat-sheet")
        print(f"Cheat sheet endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Cheat sheet items: {len(data)}")
            print(f"First item: {data[0] if data else 'No items'}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Failed to connect to cheat sheet endpoint: {e}")

if __name__ == "__main__":
    test_cheatsheet()