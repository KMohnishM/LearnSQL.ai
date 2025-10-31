from pydantic import BaseModel, field_validator, Field
from typing import Optional, List
from datetime import datetime

class LearningModule(BaseModel):
    id: int
    name: str
    description: str
    order_index: int
    difficulty_level: str
    created_at: Optional[datetime] = None

class Question(BaseModel):
    id: int
    module_id: int
    question_text: str
    difficulty_level: str
    expected_sql: Optional[str] = None
    hints: Optional[str] = None
    created_at: Optional[datetime] = None

class UserProgress(BaseModel):
    id: int
    user_id: str
    module_id: int
    current_difficulty: str
    questions_attempted: int
    questions_correct: int
    completion_percentage: float
    last_accessed: Optional[datetime] = None
    started_at: Optional[datetime] = None

class UserAttempt(BaseModel):
    id: Optional[int] = None
    user_id: str
    question_id: int
    user_sql: str
    is_correct: bool
    llm_feedback: Optional[str] = None
    correct_sql: Optional[str] = None
    score: Optional[float] = None
    attempt_number: int = 1
    created_at: Optional[datetime] = None

class CheatSheetEntry(BaseModel):
    model_config = {"populate_by_name": True}
    
    id: int
    command: str = Field(alias="topic")  # Map database 'topic' field to 'command' in JSON
    category: str
    syntax: str
    example: str
    description: Optional[str] = None
    tags: Optional[str] = None
    created_at: Optional[datetime] = None

class SubmitAnswerRequest(BaseModel):
    user_id: str
    question_id: int
    user_sql: str

class SubmitAnswerResponse(BaseModel):
    is_correct: bool
    feedback: str
    correct_sql: Optional[str] = None
    score: float
    next_difficulty: Optional[str] = None

class UserAnalytics(BaseModel):
    user_id: str
    total_questions_attempted: int
    total_correct: int
    overall_accuracy: float
    modules_progress: List[dict]
    recent_attempts: List[dict]
    strengths: List[str]
    areas_for_improvement: List[str]

class DynamicExampleRequest(BaseModel):
    command: str
    syntax: Optional[str] = ""
    category: Optional[str] = ""
    
    @field_validator('command')
    @classmethod
    def validate_command(cls, v):
        if not v or not v.strip():
            raise ValueError('Command parameter cannot be empty')
        return v.strip()