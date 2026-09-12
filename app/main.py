import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.ml_engine import explain, recommend
from app.models import Recommendation, Student
from app.schemas import RecommendationResponse, StudentCreate, StudentOut

STATIC_DIR = Path(__file__).resolve().parent / "static"

@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="AI-Based Student Career Guidance API",
    description="Backend for the Hunters Algorithm AI Career Guidance System.",
    version="2.0.0",
    lifespan=lifespan,
)

origins = [x.strip() for x in os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://localhost:5174,http://127.0.0.1:5173,http://127.0.0.1:5174",
).split(",") if x.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def home_page():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/register")
def register_page():
    return FileResponse(STATIC_DIR / "register.html")


@app.get("/recommendations")
def recommendations_page():
    return FileResponse(STATIC_DIR / "recommendations.html")


@app.get("/students")
def students_page():
    return FileResponse(STATIC_DIR / "students.html")


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "career-guidance-api"}


@app.post("/api/students", response_model=StudentOut, status_code=201)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(Student).filter(Student.email == str(payload.email)).first()
    if existing:
        raise HTTPException(status_code=409, detail="A student with this email already exists")
    data = payload.model_dump()
    data["email"] = str(payload.email)
    student = Student(**data)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@app.get("/api/students", response_model=list[StudentOut])
def list_students(db: Session = Depends(get_db)):
    return db.query(Student).order_by(desc(Student.id)).all()


@app.get("/api/students/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


def _profile(student: Student) -> dict:
    return {
        field: getattr(student, field)
        for field in [
            "academic_score", "programming", "databases", "problem_solving",
            "communication", "creativity", "teamwork", "analytical",
        ]
    } | {
        "interests": student.interests or [],
        "personality": student.personality or {},
    }


@app.post("/api/students/{student_id}/recommendations", response_model=RecommendationResponse)
def generate_recommendations(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    results = [explain(career, score) for career, score in recommend(_profile(student))]
    db.query(Recommendation).filter(Recommendation.student_id == student_id).delete(synchronize_session=False)
    for item in results:
        db.add(Recommendation(student_id=student_id, **item))
    db.commit()
    return {"student_id": student_id, "recommendations": results}


@app.get("/api/students/{student_id}/recommendations", response_model=RecommendationResponse)
def get_recommendations(student_id: int, db: Session = Depends(get_db)):
    if not db.get(Student, student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    rows = (
        db.query(Recommendation)
        .filter(Recommendation.student_id == student_id)
        .order_by(desc(Recommendation.match_percentage))
        .all()
    )
    return {"student_id": student_id, "recommendations": rows}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
