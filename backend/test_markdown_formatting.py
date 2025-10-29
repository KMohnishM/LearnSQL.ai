import asyncio
import sys
import os

# Add the parent directory to the path to import our services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.chatbot_service import ChatbotService

async def test_markdown_formatting():
    """Test the chatbot with markdown formatting"""
    chatbot = ChatbotService()
    
    test_messages = [
        "How do I add a primary key to an existing table?",
        "Explain CREATE TABLE with examples",
        "What are the different types of JOINs?"
    ]
    
    print("Testing markdown formatting in chatbot responses...\n")
    
    for i, message in enumerate(test_messages, 1):
        print(f"Test {i}: {message}")
        print("-" * 50)
        
        try:
            response = await chatbot.chat_response(
                user_message=message,
                page_context={
                    "page": "practice",
                    "module": "Basic Table Operations",
                    "question": "Working with table structure",
                    "progress": {"completed": 2, "total": 10}
                }
            )
            
            print("Response:")
            print(response["response"])
            print("\nSuggested Actions:")
            for action in response.get("suggested_actions", []):
                print(f"- {action}")
            print("\n" + "="*80 + "\n")
            
        except Exception as e:
            print(f"Error: {e}\n")
            print("="*80 + "\n")

if __name__ == "__main__":
    asyncio.run(test_markdown_formatting())