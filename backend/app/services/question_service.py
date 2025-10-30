from typing import List, Dict, Any
from app.database import execute_query_sync as execute_query, execute_insert_sync as execute_insert
from app.services.llm_service import LLMService
import json
import random

class QuestionService:
    def __init__(self):
        self.llm_service = LLMService()
    
    def get_questions_for_module(self, module_id: int, difficulty: str = "medium", limit: int = 5) -> List[Dict]:
        """Get questions for a specific module and difficulty"""
        query = """
        SELECT q.*, m.name as module_name 
        FROM questions q 
        JOIN learning_modules m ON q.module_id = m.id 
        WHERE q.module_id = ? AND q.difficulty_level = ?
        ORDER BY RANDOM()
        LIMIT ?
        """
        return execute_query(query, (module_id, difficulty, limit))
    
    async def generate_questions_for_module(self, module_id: int, count: int = 3) -> List[int]:
        """Generate new questions for a module using LLM"""
        
        # Get module info
        module_query = "SELECT * FROM learning_modules WHERE id = ?"
        module = execute_query(module_query, (module_id,))
        
        if not module:
            return []
        
        module_info = module[0]
        question_ids = []
        
        difficulties = ["easy", "medium", "hard"]
        
        for i in range(count):
            difficulty = random.choice(difficulties)
            
            # Generate question using LLM
            question_data = await self.llm_service.generate_question(
                module_info["name"], 
                difficulty
            )
            
            # Insert into database
            insert_query = """
            INSERT INTO questions (module_id, question_text, difficulty_level, expected_sql, hints)
            VALUES (?, ?, ?, ?, ?)
            """
            
            hints_json = json.dumps(question_data.get("hints", []))
            
            question_id = execute_insert(
                insert_query,
                (
                    module_id,
                    question_data["question_text"],
                    difficulty,
                    question_data.get("expected_sql"),
                    hints_json
                )
            )
            
            question_ids.append(question_id)
        
        return question_ids
    
    def get_next_question_for_user(self, user_id: str, module_id: int) -> Dict[str, Any]:
        """Get the next appropriate question for a user based on their progress"""
        
        # Get user's current progress in this module
        progress_query = """
        SELECT * FROM user_progress 
        WHERE user_id = ? AND module_id = ?
        """
        progress = execute_query(progress_query, (user_id, module_id))
        
        if progress:
            current_difficulty = progress[0]["current_difficulty"]
        else:
            # Initialize user progress for this module
            insert_progress_query = """
            INSERT INTO user_progress (user_id, module_id, current_difficulty)
            VALUES (?, ?, 'easy')
            """
            execute_insert(insert_progress_query, (user_id, module_id))
            current_difficulty = "easy"
        
        # Get a question at the appropriate difficulty
        questions = self.get_questions_for_module(module_id, current_difficulty, 1)
        
        if questions:
            question = questions[0]
            # Parse hints from JSON
            if question.get("hints"):
                try:
                    question["hints"] = json.loads(question["hints"])
                except:
                    question["hints"] = []
            return question
        else:
            # If no questions exist, generate one
            return None
    
    def update_user_difficulty(self, user_id: str, module_id: int, recent_scores: List[float]):
        """Update user's difficulty level based on recent performance"""
        
        if len(recent_scores) < 3:
            return  # Need at least 3 attempts to adjust difficulty
        
        avg_score = sum(recent_scores) / len(recent_scores)
        
        # Get current difficulty
        progress_query = """
        SELECT current_difficulty FROM user_progress 
        WHERE user_id = ? AND module_id = ?
        """
        progress = execute_query(progress_query, (user_id, module_id))
        
        if not progress:
            return
        
        current_difficulty = progress[0]["current_difficulty"]
        new_difficulty = current_difficulty
        
        # Adjust difficulty based on performance
        if avg_score >= 0.8 and current_difficulty != "hard":
            if current_difficulty == "easy":
                new_difficulty = "medium"
            elif current_difficulty == "medium":
                new_difficulty = "hard"
        elif avg_score <= 0.4 and current_difficulty != "easy":
            if current_difficulty == "hard":
                new_difficulty = "medium"
            elif current_difficulty == "medium":
                new_difficulty = "easy"
        
        # Update difficulty if it changed
        if new_difficulty != current_difficulty:
            update_query = """
            UPDATE user_progress 
            SET current_difficulty = ?, last_accessed = CURRENT_TIMESTAMP
            WHERE user_id = ? AND module_id = ?
            """
            execute_query(update_query, (new_difficulty, user_id, module_id))
    
    def get_user_recent_scores(self, user_id: str, module_id: int, limit: int = 5) -> List[float]:
        """Get user's recent scores for a module"""
        query = """
        SELECT ua.score 
        FROM user_attempts ua
        JOIN questions q ON ua.question_id = q.id
        WHERE ua.user_id = ? AND q.module_id = ?
        ORDER BY ua.created_at DESC
        LIMIT ?
        """
        
        results = execute_query(query, (user_id, module_id, limit))
        return [r["score"] for r in results if r["score"] is not None]