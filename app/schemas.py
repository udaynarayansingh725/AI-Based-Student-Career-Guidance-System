from typing import Dict, List
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    academic_score: float = Field(ge=0, le=100)
    programming: float = Field(ge=0, le=100)
    databases: float = Field(ge=0, le=100)
    problem_solving: float = Field(ge=0, le=100)
    communication: float = Field(ge=0, le=100)
    creativity: float = Field(ge=0, le=100)
    teamwork: float = Field(ge=0, le=100)
    analytical: float = Field(ge=0, le=100)
    interests: List[str] = Field(default_factory=list)
    personality: Dict[str, str] = Field(default_factory=dict)


class StudentOut(StudentCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RecommendationOut(BaseModel):
    career: str
    match_percentage: float
    reason: str
    skills: List[str]
    next_steps: List[str]


class RecommendationResponse(BaseModel):
    student_id: int
    recommendations: List[RecommendationOut]
