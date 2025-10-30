from fastapi import APIRouter, HTTPException
from typing import List
from app.models import LearningModule, Question, SubmitAnswerRequest, SubmitAnswerResponse
from app.database import execute_query_sync as execute_query, execute_insert_sync as execute_insert
from app.services.simple_question_service import ComprehensiveQuestionService
import json

router = APIRouter()
question_service = ComprehensiveQuestionService()

@router.get("/modules", response_model=List[LearningModule])
async def get_learning_modules():
    """Get all learning modules"""
    query = "SELECT * FROM learning_modules ORDER BY order_index"
    modules = execute_query(query)
    return modules

@router.get("/modules/{module_id}")
async def get_module(module_id: int):
    """Get a specific learning module"""
    query = "SELECT * FROM learning_modules WHERE id = ?"
    modules = execute_query(query, (module_id,))
    if not modules:
        raise HTTPException(status_code=404, detail="Module not found")
    return modules[0]

@router.get("/modules/{module_id}/questions")
async def get_module_questions(module_id: int, difficulty: str = "medium"):
    """Get questions for a specific module"""
    questions = question_service.get_questions_for_module(module_id, difficulty)
    
    # If no questions exist, generate some
    if not questions:
        await question_service.generate_questions_for_module(module_id, 3)
        questions = question_service.get_questions_for_module(module_id, difficulty)
    
    # Parse hints JSON for each question
    for question in questions:
        if question.get("hints"):
            try:
                question["hints"] = json.loads(question["hints"])
            except:
                question["hints"] = []
    
    return questions

@router.get("/modules/{module_id}/next-question/{user_id}")
async def get_next_question(module_id: int, user_id: str):
    """Get the next appropriate question for a user"""
    question = question_service.get_next_question_for_user(user_id, module_id)
    
    if not question:
        # Generate questions if none exist
        await question_service.generate_questions_for_module(module_id, 3)
        question = question_service.get_next_question_for_user(user_id, module_id)
    
    if not question:
        raise HTTPException(status_code=404, detail="No questions available")
    
    return question

@router.post("/practice/submit", response_model=SubmitAnswerResponse)
async def submit_answer(request: SubmitAnswerRequest):
    """Submit and evaluate a user's SQL answer"""
    
    # Get the question
    question_query = "SELECT * FROM questions WHERE id = ?"
    questions = execute_query(question_query, (request.question_id,))
    
    if not questions:
        raise HTTPException(status_code=404, detail="Question not found")
    
    question = questions[0]
    
    # Evaluate the answer using LLM
    evaluation = await llm_service.evaluate_sql_answer(
        question["question_text"],
        request.user_sql,
        question.get("expected_sql")
    )
    
    # Get attempt number for this user and question
    attempt_query = """
    SELECT COUNT(*) as count FROM user_attempts 
    WHERE user_id = ? AND question_id = ?
    """
    attempt_count = execute_query(attempt_query, (request.user_id, request.question_id))
    attempt_number = attempt_count[0]["count"] + 1 if attempt_count else 1
    
    # Store the attempt
    insert_attempt_query = """
    INSERT INTO user_attempts 
    (user_id, question_id, user_sql, is_correct, llm_feedback, correct_sql, score, attempt_number)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    execute_insert(
        insert_attempt_query,
        (
            request.user_id,
            request.question_id,
            request.user_sql,
            evaluation["is_correct"],
            evaluation["feedback"],
            evaluation.get("correct_sql"),
            evaluation["score"],
            attempt_number
        )
    )
    
    # Update user progress
    await update_user_progress(request.user_id, question["module_id"], evaluation["is_correct"], evaluation["score"])
    
    # Check if difficulty should be adjusted
    recent_scores = question_service.get_user_recent_scores(request.user_id, question["module_id"])
    if len(recent_scores) >= 3:
        question_service.update_user_difficulty(request.user_id, question["module_id"], recent_scores)
    
    # Get next difficulty level
    progress_query = """
    SELECT current_difficulty FROM user_progress 
    WHERE user_id = ? AND module_id = ?
    """
    progress = execute_query(progress_query, (request.user_id, question["module_id"]))
    next_difficulty = progress[0]["current_difficulty"] if progress else "medium"
    
    return SubmitAnswerResponse(
        is_correct=evaluation["is_correct"],
        feedback=evaluation["feedback"],
        correct_sql=evaluation.get("correct_sql"),
        score=evaluation["score"],
        next_difficulty=next_difficulty
    )

async def update_user_progress(user_id: str, module_id: int, is_correct: bool, score: float):
    """Update user progress for a module"""
    
    # Check if progress record exists
    progress_query = """
    SELECT * FROM user_progress WHERE user_id = ? AND module_id = ?
    """
    progress = execute_query(progress_query, (user_id, module_id))
    
    if progress:
        # Update existing progress
        current = progress[0]
        new_attempted = current["questions_attempted"] + 1
        new_correct = current["questions_correct"] + (1 if is_correct else 0)
        new_percentage = (new_correct / new_attempted) * 100
        
        update_query = """
        UPDATE user_progress 
        SET questions_attempted = ?, questions_correct = ?, 
            completion_percentage = ?, last_accessed = CURRENT_TIMESTAMP
        WHERE user_id = ? AND module_id = ?
        """
        execute_query(update_query, (new_attempted, new_correct, new_percentage, user_id, module_id))
    else:
        # Create new progress record
        insert_query = """
        INSERT INTO user_progress 
        (user_id, module_id, questions_attempted, questions_correct, completion_percentage)
        VALUES (?, ?, 1, ?, ?)
        """
        completion = 100.0 if is_correct else 0.0
        execute_insert(insert_query, (user_id, module_id, 1 if is_correct else 0, completion))

@router.get("/practice/progress/{user_id}")
async def get_user_progress(user_id: str):
    """Get user's progress across all modules"""
    query = """
    SELECT up.*, lm.name as module_name, lm.description as module_description
    FROM user_progress up
    JOIN learning_modules lm ON up.module_id = lm.id
    WHERE up.user_id = ?
    ORDER BY lm.order_index
    """
    return execute_query(query, (user_id,))

@router.get("/modules/{module_id}/business-question")
async def get_business_scenario_question(module_id: int, difficulty: str = "easy"):
    """Get a realistic business scenario question for the module"""
    try:
        question = comprehensive_question_service.get_question(module_id, difficulty)
        if "error" in question:
            raise HTTPException(status_code=404, detail=question["error"])
        return question
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get business question: {str(e)}")

@router.post("/practice/evaluate-business-answer")
async def evaluate_business_answer(request: dict):
    """Evaluate user's answer to a business scenario question"""
    try:
        question_id = request.get("question_id")
        user_sql = request.get("user_sql")
        expected_sql = request.get("expected_sql", "")
        
        if not question_id or not user_sql:
            raise HTTPException(status_code=400, detail="Missing question_id or user_sql")
        
        evaluation = await comprehensive_question_service.evaluate_answer(question_id, user_sql, expected_sql)
        return evaluation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to evaluate answer: {str(e)}")

@router.get("/progress/{user_id}/module/{module_id}")
async def get_business_progress(user_id: str, module_id: int):
    """Get user's progress with business scenarios"""
    try:
        progress = comprehensive_question_service.get_module_progress(user_id, module_id)
        return progress
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get progress: {str(e)}")

@router.post("/practice/validate-sql")
async def validate_sql_syntax(request: dict):
    """Validate SQL syntax without saving to database"""
    try:
        user_sql = request.get("sql", "")
        if not user_sql:
            return {"is_valid": False, "error": "No SQL provided"}
        
        # Basic syntax validation - could be enhanced with actual SQL parser
        validation_result = await llm_service.validate_sql_syntax(user_sql)
        return validation_result
    except Exception as e:
        return {"is_valid": False, "error": str(e)}