from fastapi import APIRouter, HTTPException
from typing import List
from app.models import LearningModule, SubmitAnswerRequest, SubmitAnswerResponse
from app.database import execute_query, execute_insert
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

@router.get("/modules/{module_id}/business-question")
async def get_business_scenario_question(module_id: int, difficulty: str = "easy"):
    """Generate a realistic business scenario question using LLM"""
    try:
        question = await question_service.get_business_question(str(module_id), difficulty)
        return question
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate question: {str(e)}")

@router.post("/practice/evaluate-business-answer")
async def evaluate_business_answer(request: dict):
    """Evaluate user's answer using LLM"""
    try:
        question_id = request.get("question_id")
        user_sql = request.get("user_sql")
        question_context = request.get("question_context", "")
        
        if not question_id or not user_sql:
            raise HTTPException(status_code=400, detail="Missing question_id or user_sql")
        
        evaluation = await question_service.evaluate_answer(question_id, user_sql, question_context)
        
        # Store the attempt
        user_id = request.get("user_id", "anonymous")
        await store_user_attempt(user_id, question_id, user_sql, evaluation)
        
        return evaluation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to evaluate answer: {str(e)}")

@router.get("/practice/progress/{user_id}")
async def get_user_progress(user_id: str):
    """Get user's progress and generate personalized analysis"""
    try:
        # Get recent attempts
        query = """
        SELECT ua.*, q.module_id, q.difficulty_level
        FROM user_attempts ua
        LEFT JOIN questions q ON ua.question_id = q.id
        WHERE ua.user_id = ?
        ORDER BY ua.created_at DESC
        LIMIT 20
        """
        attempts = execute_query(query, (user_id,))
        
        # Generate personalized analysis using LLM
        analysis = await question_service.get_personalized_analysis(user_id, attempts)
        
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get progress: {str(e)}")

@router.get("/practice/progress")
async def get_default_progress():
    """Get default progress for anonymous users"""
    try:
        # Return empty progress for new users
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get progress: {str(e)}")

@router.post("/practice/question")
async def get_practice_question(request: dict):
    """Generate a practice question - matches frontend expectation"""
    try:
        module_id = request.get("module_id", 1)
        difficulty = request.get("difficulty", "easy")
        
        question = await question_service.get_business_question(str(module_id), difficulty)
        return question
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate question: {str(e)}")

@router.post("/practice/validate-sql")
async def validate_sql_syntax(request: dict):
    """Validate SQL syntax using LLM"""
    try:
        user_sql = request.get("sql", "")
        if not user_sql:
            return {"is_valid": False, "error": "No SQL provided"}
        
        # Use LLM to validate SQL
        validation_prompt = f"Is this SQL syntax valid? Just respond with 'VALID' or 'INVALID: error description'\n\nSQL: {user_sql}"
        result = await question_service._call_llm(validation_prompt, temperature=0.1)
        
        is_valid = "VALID" in result.upper() and "INVALID" not in result.upper()
        error = result if not is_valid else None
        
        return {"is_valid": is_valid, "error": error}
    except Exception as e:
        return {"is_valid": False, "error": str(e)}

@router.get("/cheat-sheet")
async def get_cheat_sheet():
    """Get SQL cheat sheet"""
    return question_service.get_cheat_sheet()

@router.post("/cheat-sheet/example")
async def get_dynamic_example(request: dict):
    """Generate a dynamic business scenario example for a cheat sheet item"""
    try:
        command = request.get("command")
        syntax = request.get("syntax") 
        category = request.get("category")
        
        if not command:
            raise HTTPException(status_code=400, detail="Missing command parameter")
        
        example = await question_service.generate_dynamic_example(command, syntax, category)
        return example
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate example: {str(e)}")

async def store_user_attempt(user_id: str, question_id: str, user_sql: str, evaluation: dict):
    """Store user attempt in database"""
    try:
        # Get attempt number
        attempt_query = """
        SELECT COUNT(*) as count FROM user_attempts 
        WHERE user_id = ? AND question_id = ?
        """
        attempt_count = execute_query(attempt_query, (user_id, question_id))
        attempt_number = attempt_count[0]["count"] + 1 if attempt_count else 1
        
        # Store the attempt
        insert_attempt_query = """
        INSERT INTO user_attempts 
        (user_id, question_id, user_sql, is_correct, llm_feedback, score, attempt_number)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        execute_insert(
            insert_attempt_query,
            (
                user_id,
                question_id,
                user_sql,
                evaluation.get("is_correct", False),
                evaluation.get("feedback", ""),
                evaluation.get("score", 0),
                attempt_number
            )
        )
    except Exception as e:
        print(f"Error storing attempt: {e}")