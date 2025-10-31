from fastapi import APIRouter, HTTPException
import logging
from typing import List
from app.models import LearningModule, SubmitAnswerRequest, SubmitAnswerResponse, DynamicExampleRequest
from app.database import execute_query_sync as execute_query, execute_insert_sync as execute_insert
from app.services.simple_question_service import ComprehensiveQuestionService
import json

# Set up logging
logging.basicConfig(level=logging.INFO)

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
        store_user_attempt(user_id, question_id, user_sql, evaluation)
        
        return evaluation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to evaluate answer: {str(e)}")

@router.get("/practice/progress/{user_id}")
async def get_user_progress(user_id: str):
    """Get user's progress across all modules - for Practice page display"""
    try:
        logging.info(f"Getting module progress for user: {user_id}")
        
        # Get progress by module from user_progress table
        progress_query = """
        SELECT 
            up.module_id,
            up.questions_attempted,
            up.questions_correct,
            up.completion_percentage,
            up.current_difficulty,
            lm.name as module_name,
            lm.description as module_description
        FROM user_progress up
        JOIN learning_modules lm ON up.module_id = lm.id
        WHERE up.user_id = ?
        ORDER BY lm.order_index
        """
        
        try:
            # First, get all modules to ensure we show all of them
            all_modules_query = """
            SELECT 
                lm.id as module_id,
                lm.name as module_name,
                lm.description as module_description,
                COALESCE(up.questions_attempted, 0) as questions_attempted,
                COALESCE(up.questions_correct, 0) as questions_correct,
                COALESCE(up.completion_percentage, 0.0) as completion_percentage,
                COALESCE(up.current_difficulty, 'easy') as current_difficulty
            FROM learning_modules lm
            LEFT JOIN user_progress up ON lm.id = up.module_id AND up.user_id = %s
            ORDER BY lm.order_index
            """
            progress_data = execute_query(all_modules_query, (user_id,))
            logging.info(f"Found progress for {len(progress_data)} modules for user {user_id}")
            return progress_data
        except Exception as db_error:
            logging.error(f"Database query failed: {db_error}")
            # Return empty array if database query fails
            return []
            
    except Exception as e:
        logging.error(f"Failed to get user progress: {e}")
        return []

@router.get("/practice/analysis/{user_id}")
async def get_user_analysis(user_id: str):
    """Get user's detailed analysis with LLM insights"""
    try:
        logging.info(f"Getting analysis for user: {user_id}")
        
        # Get recent attempts with extracted module info from dynamic question IDs
        query = """
        SELECT 
            ua.*,
            CASE 
                WHEN ua.question_id LIKE '1_%' THEN 1
                WHEN ua.question_id LIKE '2_%' THEN 2
                WHEN ua.question_id LIKE '3_%' THEN 3
                WHEN ua.question_id LIKE '4_%' THEN 4
                WHEN ua.question_id LIKE '5_%' THEN 5
                WHEN ua.question_id LIKE '6_%' THEN 6
                ELSE 1
            END as module_id,
            CASE 
                WHEN ua.question_id LIKE '%_easy_%' THEN 'easy'
                WHEN ua.question_id LIKE '%_medium_%' THEN 'medium'
                WHEN ua.question_id LIKE '%_hard_%' THEN 'hard'
                ELSE 'medium'
            END as difficulty_level
        FROM user_attempts ua
        WHERE ua.user_id = ?
        ORDER BY ua.created_at DESC
        LIMIT 20
        """
        
        attempts = execute_query(query, (user_id,))
        logging.info(f"Found {len(attempts)} attempts for user {user_id}")
        
        # Generate personalized analysis using LLM
        try:
            analysis = await question_service.get_personalized_analysis(user_id, attempts)
            return analysis
        except Exception as llm_error:
            # Fallback to simple progress data if LLM fails
            logging.warning(f"LLM analysis failed for user {user_id}: {llm_error}")
            
            # Return basic progress summary without LLM analysis
            total_attempts = len(attempts)
            correct_attempts = sum(1 for a in attempts if a.get('is_correct', False))
            accuracy = (correct_attempts / total_attempts * 100) if total_attempts > 0 else 0
            
            return {
                "user_id": user_id,
                "analysis": f"Progress Summary: {total_attempts} questions attempted with {accuracy:.1f}% accuracy. Keep practicing to improve your SQL skills!",
                "performance_summary": {
                    "total_questions": total_attempts,
                    "correct_answers": correct_attempts,
                    "accuracy_percentage": accuracy,
                    "modules_practiced": len(set(a.get('module_id') for a in attempts if a.get('module_id')))
                },
                "recent_attempts": attempts[:5]  # Last 5 attempts
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analysis: {str(e)}")

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
async def get_dynamic_example(request: DynamicExampleRequest):
    """Generate a dynamic business scenario example for a cheat sheet item"""
    try:
        example = await question_service.generate_dynamic_example(
            request.command, request.syntax, request.category
        )
        return example
    except Exception as e:
        # If this is an HTTPException (client error), re-raise so FastAPI returns the proper status
        if isinstance(e, HTTPException):
            raise

        # Use exception logging so stacktrace is captured. Also log repr(e) in case str(e) is empty.
        logger = logging.getLogger(__name__)
        logger.exception("Failed to generate dynamic example")
        logger.error(f"Exception (repr): {repr(e)}")
        try:
            logger.debug(f"Request body for dynamic example: {request}")
        except Exception:
            # ignore errors while trying to log request
            pass

        # Provide a friendly fallback so the frontend can display a helpful message
        return {
            "scenario": "Real-Time Scenario",
            "business_context": "Unable to generate real-time example at this time.",
            "table_description": "",
            "sql_example": request.syntax or request.command or "",
            "explanation": "Please try again later or refer to the static example provided.",
            "sample_data": ""
        }

def store_user_attempt(user_id: str, question_id: str, user_sql: str, evaluation: dict):
    """Store user attempt in database and update progress"""
    try:
        from app.database import execute_query_sync, execute_insert_sync
        
        # Get attempt number
        attempt_query = """
        SELECT COUNT(*) as count FROM user_attempts 
        WHERE user_id = %s AND question_id = %s
        """
        attempt_count = execute_query_sync(attempt_query, (user_id, question_id))
        attempt_number = attempt_count[0]["count"] + 1 if attempt_count else 1
        
        # Store the attempt
        insert_attempt_query = """
        INSERT INTO user_attempts 
        (user_id, question_id, user_sql, is_correct, llm_feedback, score, attempt_number)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        execute_insert_sync(
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
        
        # Update user progress for the module
        # Extract module_id from question_id (format: "module_difficulty_random")
        try:
            module_id = int(question_id.split('_')[0])
            update_user_progress(user_id, module_id, evaluation.get("is_correct", False))
        except (ValueError, IndexError):
            logging.warning(f"Could not extract module_id from question_id: {question_id}")
            
        logging.info(f"Stored attempt for user {user_id}, question {question_id}, correct: {evaluation.get('is_correct', False)}")
        
    except Exception as e:
        logging.error(f"Error storing attempt (production DB readonly): {e}")
        # In production, gracefully handle readonly database by not failing the request
        # Users can still get LLM feedback even if storage fails
        if "readonly database" in str(e).lower() or "attempt to write" in str(e).lower():
            logging.warning(f"Database readonly in production - storage skipped for user {user_id}")
            return  # Don't raise, let the evaluation response succeed
        else:
            raise  # Re-raise other errors

def update_user_progress(user_id: str, module_id: int, is_correct: bool):
    """Update user progress for a module"""
    try:
        from app.database import execute_query_sync, execute_insert_sync, execute_update_sync
        
        # Check if progress record exists
        progress_query = """
        SELECT * FROM user_progress 
        WHERE user_id = %s AND module_id = %s
        """
        existing_progress = execute_query_sync(progress_query, (user_id, module_id))
        
        if existing_progress:
            # Update existing progress
            current = existing_progress[0]
            new_attempted = current["questions_attempted"] + 1
            new_correct = current["questions_correct"] + (1 if is_correct else 0)
            new_completion = min(100.0, (new_correct / new_attempted) * 100)
            
            update_query = """
            UPDATE user_progress 
            SET questions_attempted = %s, questions_correct = %s, 
                completion_percentage = %s, last_accessed = CURRENT_TIMESTAMP
            WHERE user_id = %s AND module_id = %s
            """
            execute_update_sync(update_query, (new_attempted, new_correct, new_completion, user_id, module_id))
            
        else:
            # Create new progress record
            new_attempted = 1
            new_correct = 1 if is_correct else 0
            new_completion = new_correct / new_attempted * 100
            
            insert_query = """
            INSERT INTO user_progress 
            (user_id, module_id, questions_attempted, questions_correct, completion_percentage)
            VALUES (%s, %s, %s, %s, %s)
            """
            execute_insert_sync(insert_query, (user_id, module_id, new_attempted, new_correct, new_completion))
            
        logging.info(f"Updated progress for user {user_id}, module {module_id}")
        
    except Exception as e:
        logging.error(f"Error updating user progress: {e}")