from app.services.comprehensive_question_service import ComprehensiveQuestionService
import asyncio

async def test_dynamic_evaluation():
    service = ComprehensiveQuestionService()
    
    # Test different SQL patterns
    test_cases = [
        {
            'name': 'UPDATE Query',
            'user_sql': 'UPDATE books SET status = "damaged", return_date = CURRENT_DATE, late_fee = 15.00 WHERE book_id = 42;',
            'question_id': 'update_library_book_damage'
        },
        {
            'name': 'SELECT with JOIN',
            'user_sql': 'SELECT c.name, o.total FROM customers c JOIN orders o ON c.id = o.customer_id WHERE o.date >= "2024-01-01";',
            'question_id': 'select_customer_orders'
        },
        {
            'name': 'CREATE TABLE',
            'user_sql': 'CREATE TABLE restaurants (id INT PRIMARY KEY, name VARCHAR(100), cuisine VARCHAR(50)); INSERT INTO restaurants VALUES (1, "Mario\'s Pizza", "Italian");',
            'question_id': 'create_restaurant_table'
        }
    ]
    
    for test in test_cases:
        print(f'\n=== Testing {test["name"]} ===')
        try:
            result = await service.evaluate_answer(
                question_id=test['question_id'],
                user_sql=test['user_sql']
            )
            print(f'Score: {result["score"]}/100')
            print(f'Correct: {result["is_correct"]}')
            print(f'Feedback length: {len(result["feedback"])} chars')
            print(f'Suggestions: {len(result["suggestions"])} items')
            print(f'First suggestion: {result["suggestions"][0] if result["suggestions"] else "None"}')
        except Exception as e:
            print(f'Error: {e}')

if __name__ == '__main__':
    asyncio.run(test_dynamic_evaluation())