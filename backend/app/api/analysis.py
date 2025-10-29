from fastapi import APIRouter, HTTPException
from app.models import UserAnalytics
from app.database import execute_query
from typing import List, Dict, Any

router = APIRouter()

@router.get("/analysis/{user_id}", response_model=UserAnalytics)
async def get_user_analytics(user_id: str):
    """Get comprehensive analytics for a user"""
    
    # Get overall stats
    overall_query = """
    SELECT 
        COUNT(*) as total_attempts,
        SUM(CASE WHEN is_correct THEN 1 ELSE 0 END) as total_correct,
        AVG(score) as avg_score
    FROM user_attempts 
    WHERE user_id = ?
    """
    overall_stats = execute_query(overall_query, (user_id,))
    
    if not overall_stats or overall_stats[0]["total_attempts"] == 0:
        # Return empty analytics for new users
        return UserAnalytics(
            user_id=user_id,
            total_questions_attempted=0,
            total_correct=0,
            overall_accuracy=0.0,
            modules_progress=[],
            recent_attempts=[],
            strengths=[],
            areas_for_improvement=[]
        )
    
    stats = overall_stats[0]
    total_attempts = stats["total_attempts"]
    total_correct = stats["total_correct"]
    overall_accuracy = (total_correct / total_attempts) * 100 if total_attempts > 0 else 0
    
    # Get progress by module
    modules_query = """
    SELECT 
        up.module_id,
        lm.name as module_name,
        up.questions_attempted,
        up.questions_correct,
        up.completion_percentage,
        up.current_difficulty,
        AVG(ua.score) as avg_score
    FROM user_progress up
    JOIN learning_modules lm ON up.module_id = lm.id
    LEFT JOIN user_attempts ua ON ua.user_id = up.user_id
    LEFT JOIN questions q ON ua.question_id = q.id AND q.module_id = up.module_id
    WHERE up.user_id = ?
    GROUP BY up.module_id, lm.name, up.questions_attempted, up.questions_correct, up.completion_percentage, up.current_difficulty
    ORDER BY lm.order_index
    """
    modules_progress = execute_query(modules_query, (user_id,))
    
    # Get recent attempts
    recent_query = """
    SELECT 
        ua.created_at,
        ua.user_sql,
        ua.is_correct,
        ua.score,
        ua.llm_feedback,
        q.question_text,
        lm.name as module_name
    FROM user_attempts ua
    JOIN questions q ON ua.question_id = q.id
    JOIN learning_modules lm ON q.module_id = lm.id
    WHERE ua.user_id = ?
    ORDER BY ua.created_at DESC
    LIMIT 10
    """
    recent_attempts = execute_query(recent_query, (user_id,))
    
    # Analyze strengths and weaknesses
    strengths, areas_for_improvement = analyze_performance(modules_progress, recent_attempts)
    
    return UserAnalytics(
        user_id=user_id,
        total_questions_attempted=total_attempts,
        total_correct=total_correct,
        overall_accuracy=overall_accuracy,
        modules_progress=[dict(module) for module in modules_progress],
        recent_attempts=[dict(attempt) for attempt in recent_attempts],
        strengths=strengths,
        areas_for_improvement=areas_for_improvement
    )

@router.get("/analysis/{user_id}/detailed")
async def get_detailed_analytics(user_id: str):
    """Get detailed analytics with charts and insights"""
    
    # Performance over time
    performance_query = """
    SELECT 
        DATE(created_at) as date,
        AVG(score) as avg_score,
        COUNT(*) as attempts,
        SUM(CASE WHEN is_correct THEN 1 ELSE 0 END) as correct
    FROM user_attempts 
    WHERE user_id = ?
    GROUP BY DATE(created_at)
    ORDER BY date DESC
    LIMIT 30
    """
    performance_data = execute_query(performance_query, (user_id,))
    
    # Difficulty distribution
    difficulty_query = """
    SELECT 
        q.difficulty_level,
        COUNT(*) as attempts,
        AVG(ua.score) as avg_score,
        SUM(CASE WHEN ua.is_correct THEN 1 ELSE 0 END) as correct
    FROM user_attempts ua
    JOIN questions q ON ua.question_id = q.id
    WHERE ua.user_id = ?
    GROUP BY q.difficulty_level
    """
    difficulty_data = execute_query(difficulty_query, (user_id,))
    
    # Common mistakes
    mistakes_query = """
    SELECT 
        ua.llm_feedback,
        COUNT(*) as frequency
    FROM user_attempts ua
    WHERE ua.user_id = ? AND ua.is_correct = 0
    GROUP BY ua.llm_feedback
    ORDER BY frequency DESC
    LIMIT 5
    """
    common_mistakes = execute_query(mistakes_query, (user_id,))
    
    return {
        "performance_over_time": performance_data,
        "difficulty_distribution": difficulty_data,
        "common_mistakes": common_mistakes
    }

@router.get("/analysis/{user_id}/learning-path")
async def get_learning_path_suggestions(user_id: str):
    """Get personalized learning path suggestions"""
    
    # Get user's current progress
    progress_query = """
    SELECT 
        up.*,
        lm.name as module_name,
        lm.order_index
    FROM user_progress up
    JOIN learning_modules lm ON up.module_id = lm.id
    WHERE up.user_id = ?
    ORDER BY lm.order_index
    """
    progress = execute_query(progress_query, (user_id,))
    
    suggestions = []
    
    for module in progress:
        if module["completion_percentage"] < 70:
            suggestions.append({
                "type": "continue_module",
                "module_name": module["module_name"],
                "reason": f"You're at {module['completion_percentage']:.1f}% completion. Continue practicing to master this topic.",
                "priority": "high" if module["completion_percentage"] < 30 else "medium"
            })
        elif module["current_difficulty"] == "easy":
            suggestions.append({
                "type": "increase_difficulty",
                "module_name": module["module_name"],
                "reason": "You're doing well! Try medium difficulty questions to challenge yourself.",
                "priority": "medium"
            })
    
    # Check for modules not started
    all_modules_query = "SELECT * FROM learning_modules ORDER BY order_index"
    all_modules = execute_query(all_modules_query)
    
    started_module_ids = {p["module_id"] for p in progress}
    
    for module in all_modules:
        if module["id"] not in started_module_ids:
            suggestions.append({
                "type": "start_module",
                "module_name": module["name"],
                "reason": f"Ready to learn {module['name']}? This builds on your existing knowledge.",
                "priority": "low"
            })
            break  # Only suggest the next unstarted module
    
    return {"suggestions": suggestions}

def analyze_performance(modules_progress: List[Dict], recent_attempts: List[Dict]) -> tuple[List[str], List[str]]:
    """Analyze user performance to identify strengths and areas for improvement"""
    
    strengths = []
    areas_for_improvement = []
    
    # Analyze by module performance
    for module in modules_progress:
        accuracy = (module["questions_correct"] / module["questions_attempted"]) * 100 if module["questions_attempted"] > 0 else 0
        
        if accuracy >= 80 and module["questions_attempted"] >= 3:
            strengths.append(f"Strong performance in {module['module_name']} ({accuracy:.1f}% accuracy)")
        elif accuracy < 50 and module["questions_attempted"] >= 3:
            areas_for_improvement.append(f"Need more practice with {module['module_name']} ({accuracy:.1f}% accuracy)")
    
    # Analyze recent performance trend
    if len(recent_attempts) >= 5:
        recent_scores = [attempt["score"] for attempt in recent_attempts[:5] if attempt["score"]]
        if recent_scores:
            avg_recent_score = sum(recent_scores) / len(recent_scores)
            if avg_recent_score >= 0.8:
                strengths.append("Improving performance in recent attempts")
            elif avg_recent_score < 0.5:
                areas_for_improvement.append("Recent performance shows room for improvement")
    
    # Default messages if no specific patterns found
    if not strengths:
        strengths.append("Keep practicing to build your SQL skills!")
    
    if not areas_for_improvement:
        areas_for_improvement.append("Focus on consistency across all modules")
    
    return strengths, areas_for_improvement