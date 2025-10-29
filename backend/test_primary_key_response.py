import asyncio
import json
from app.services.chatbot_service import ChatbotService

async def test_primary_key_formatting():
    """Test the specific primary key response formatting"""
    chatbot = ChatbotService()
    
    # Test the exact message that was showing formatting issues
    test_message = "How do I add a primary key to an existing table?"
    
    print("Testing Primary Key Response Formatting...")
    print("=" * 60)
    print(f"User Question: {test_message}")
    print("-" * 60)
    
    try:
        response = await chatbot.chat_response(
            user_message=test_message,
            page_context={
                "page": "practice",
                "module": "Table Operations",
                "question": "Working with table constraints",
                "progress": {"completed": 3, "total": 8}
            }
        )
        
        print("Raw Response:")
        print(response["response"])
        print("\n" + "=" * 60)
        
        # Check for proper markdown formatting
        response_text = response["response"]
        
        print("Markdown Elements Found:")
        print("-" * 30)
        
        # Check for headers
        if "###" in response_text:
            print("✅ Headers (###) found")
        else:
            print("❌ No headers found")
            
        # Check for bold text
        if "**" in response_text:
            print("✅ Bold text (**) found")
        else:
            print("❌ No bold text found")
            
        # Check for code blocks
        if "```sql" in response_text:
            print("✅ SQL code blocks found")
        else:
            print("❌ No SQL code blocks found")
            
        # Check for inline code
        if "`" in response_text and "```" not in response_text.replace("```sql", ""):
            print("✅ Inline code (`) found")
        else:
            print("❌ No inline code found")
            
        # Check for bullet points
        if "*" in response_text or "-" in response_text:
            print("✅ Bullet points found")
        else:
            print("❌ No bullet points found")
            
        print("\nSuggested Actions:")
        for action in response.get("suggested_actions", []):
            print(f"  • {action}")
            
        print("\n" + "=" * 60)
        print("✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")

if __name__ == "__main__":
    asyncio.run(test_primary_key_formatting())