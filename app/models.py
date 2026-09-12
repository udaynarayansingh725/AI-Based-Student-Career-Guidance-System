from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(180), unique=True, nullable=False, index=True)
    academic_score = Column(Float, nullable=False)
    programming = Column(Float, default=0)
    databases = Column(Float, default=0)
    problem_solving = Column(Float, default=0)
    communication = Column(Float, default=0)
    creativity = Column(Float, default=0)
    teamwork = Column(Float, default=0)
    analytical = Column(Float, default=0)
    interests = Column(JSON, default=list)
    personality = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, nullable=False, index=True)
    career = Column(String(120), nullable=False)
    match_percentage = Column(Float, nullable=False)
    reason = Column(String(500), nullable=False)
    skills = Column(JSON, default=list)
    next_steps = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
