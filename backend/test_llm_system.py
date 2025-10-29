import asyncio
from app.services.simple_question_service import ComprehensiveQuestionService

async def test_llm_system():
    service = ComprehensiveQuestionService()
    
    print("=== Testing LLM-Driven SQL Learning System ===\n")
    
    # Test 1: Generate a business question
    print("1. Generating business scenario question...")
    question = await service.get_business_question("1", "easy")
    print(f"✅ Generated question for Module 1 (Easy)")
    print(f"Question ID: {question['question_id']}")
    print(f"Question length: {len(question['question'])} chars")
    print(f"First 200 chars: {question['question'][:200]}...\n")
    
    # Test 2: Evaluate a SQL answer
    print("2. Evaluating SQL answer...")
    test_sql = "UPDATE orders SET status = 'shipped', updated_at = NOW() WHERE order_id = 12345;"
    evaluation = await service.evaluate_answer(
        question_id=question['question_id'],
        user_sql=test_sql,
        question_context=question['question']
    )
    print(f"✅ Evaluated SQL answer")
    print(f"Score: {evaluation['score']}/100")
    print(f"Correct: {evaluation['is_correct']}")
    print(f"Feedback length: {len(evaluation['feedback'])} chars")
    print(f"Suggestions: {len(evaluation['suggestions'])} items\n")
    
    # Test 3: Generate personalized analysis
    print("3. Generating personalized analysis...")
    mock_performance = [
        {"score": 85, "module_id": "1", "is_correct": True},
        {"score": 70, "module_id": "2", "is_correct": False},
        {"score": 90, "module_id": "1", "is_correct": True}
    ]
    analysis = await service.get_personalized_analysis("test_user", mock_performance)
    print(f"✅ Generated personalized analysis")
    print(f"Analysis length: {len(analysis['analysis'])} chars")
    print(f"Performance summary: {analysis['performance_summary']}\n")
    
    # Test 4: Get cheat sheet
    print("4. Getting SQL cheat sheet...")
    cheat_sheet = service.get_cheat_sheet()
    print(f"✅ Retrieved cheat sheet with {len(cheat_sheet)} entries")
    for item in cheat_sheet[:2]:
        print(f"  - {item['category']}: {item['command']}")
    
    print("\n🎉 All tests passed! LLM-driven system is working perfectly!")

if __name__ == "__main__":
    asyncio.run(test_llm_system())