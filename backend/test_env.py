import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
print(f"API Key loaded: {'Yes' if api_key else 'No'}")
print(f"API Key starts with: {api_key[:10] if api_key else 'None'}...")
print(f"API Key length: {len(api_key) if api_key else 0}")