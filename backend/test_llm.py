import asyncio
from app.services.simple_question_service import ComprehensiveQuestionService

async def test_llm():
    service = ComprehensiveQuestionService()
    
    print("Testing LLM connection...")
    print(f"API Key loaded: {'Yes' if service.openrouter_api_key else 'No'}")
    
    # Test simple prompt
    try:
        result = await service._call_llm("What is SQL? Give a very brief answer.", temperature=0.1)
        print(f"LLM Response: {result}")
        print("LLM is working!")
    except Exception as e:
        print(f"LLM Error: {e}")
    
    # Test question generation
    try:
        print("\nTesting question generation...")
        question = await service.get_business_question("1", "easy")
        print(f"Question generated successfully!")
        print(f"Question keys: {list(question.keys())}")
        print(f"Question text: {question.get('question', 'No question')[:200]}...")
    except Exception as e:
        print(f"Question generation error: {e}")

if __name__ == "__main__":
    asyncio.run(test_llm())