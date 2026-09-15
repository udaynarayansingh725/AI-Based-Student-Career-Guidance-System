# AI-Based Student Career Guidance System

An AI-powered platform that provides personalized, data-driven career guidance to students by analyzing academic records, skills & aptitudes, and personality profiles.

---



---

## Problem Statement

Students lack personalized, data-driven career guidance. Key gaps:

- **No Personalized Guidance** — Generic advice doesn't account for individual strengths
- **Pressure-Driven Decisions** — Career choices driven by peer/family pressure, not aptitude
- **No Unified System** — Scattered resources, no single platform for holistic guidance

**Why it matters:** Mismatch leads to lower engagement, weak academic performance, and delayed career clarity.

---

## Proposed Solution

An AI-powered platform analyzing **three dimensions**:

| Dimension | What It Captures |
|---|---|
| Academic Records | Scores, grades, academic performance |
| Skills & Aptitudes | Programming, databases, problem-solving, analytical thinking |
| Personality Profile | Communication, creativity, teamwork, interests, personality traits |

**Benefits:** Personalized guidance + Objective insight + Unified system

---

## Architecture & Workflow

### Pipeline (4 Steps)

```
Registration → Data Processing → ML Prediction (Random Forest) → Ranked Output
```

### Layered Architecture

```
┌─────────────────┐
│  Web Frontend    │  (React / Next.js)
├─────────────────┤
│  API Layer       │  (FastAPI + SQLAlchemy)
├─────────────────┤
│  Processing Eng. │  (ML Engine — RandomForest)
├─────────────────┤
│  Data Layer      │  (PostgreSQL / SQLite)
└─────────────────┘
```

---

## Tech Stack

| Component | Technology | Why |
|---|---|---|
| API Framework | **FastAPI** | High performance, async support, auto-generated docs |
| Database | **PostgreSQL** (prod) / **SQLite** (dev) | Reliable, scalable relational storage |
| ML Model | **Random Forest** (scikit-learn) | Multiple trees, diverse samples, majority voting |
| Deployment | **Linode** | Affordable cloud hosting |

### Why Random Forest?

- **Multiple Decision Trees** — Reduces overfitting vs single tree
- **Diverse Samples** — Each tree trained on different data subset
- **Majority Voting** — Final prediction from collective decision

---

## Key Features

1. **Complete Profile Analysis** — Analyzes 8 skill dimensions + interests + personality
2. **AI-Powered Recommendations** — RandomForest classifier with interest/personality adjustments
3. **Affordable Alternative** — Free ML-based guidance vs expensive career counselors

### Example Output

```
Student Profile: Programming=92, Databases=80, Problem-Solving=90, Analytical=88
                 Interests=[Technology, AI/ML], Personality=[Analytical, Independent]

Recommended Career: Software Developer — 92% Match
Core Skills: Programming, Databases, Problem-Solving, Logic, Version Control
Next Steps: Build portfolio projects, Practice DSA, Learn Git and APIs
```

---

## Supported Career Paths

| Career | Key Skills |
|---|---|
| Software Developer | Programming, Databases, Problem-Solving, Logic, Version Control |
| Data Analyst | SQL, Python, Statistics, Data Visualization |
| UI/UX Designer | Figma, Creativity, User Research, Visual Design |
| Business Analyst | Requirements, Communication, Analytics, Documentation |
| Cybersecurity Analyst | Networking, Security, Linux, Risk Analysis |

---

## Setup & Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/ai-career-guidance.git
cd ai-career-guidance

# Install dependencies
pip install -r requirements.txt

# Run the server (serves frontend + API)
python app/main.py
# or
uvicorn app.main:app --reload

# Seed demo data (server must be running)
python app/seed.py
```

---

## Frontend (Web UI)

A built-in zero-dependency multi-page web interface (HTML/CSS/JS, no `npm` needed) is served automatically by FastAPI.

| Page | URL | Purpose |
|---|---|---|
| Home | `/` | Landing page with overview |
| Register | `/register` | Student registration form (8 skill sliders, interests, personality) |
| Recommendations | `/recommendations` | AI career predictions with animated match bars, skills & next steps |
| Students | `/students` | List of all registered students |
| Edit | `/edit?id=X` | Edit an existing student's profile |

**Features:**
- Separate pages with navigation bar
- **Dark / Light / System themes** — pickable from the navigation bar, saved in `localStorage`
- One-click career prediction
- **Edit student profiles** — update details and refresh recommendations automatically
- Student selector + "Generate / Refresh" on the recommendations page
- Animated match-percentage bars for top 5 careers
- Follow this flow: **Register → Recommendations → Students → Edit**

Source: `app/static/` (`index.html`, `register.html`, `recommendations.html`, `students.html`, `style.css`, `app.js`)

---

## Database

### Development — SQLite (default)

Out of the box the API uses SQLite (`career_guidance.db`). Zero setup.

### Production — PostgreSQL (recommended)

| Variable | Description |
|---|---|
| `DATABASE_URL` | `postgresql://user:password@host:5432/dbname` |

```bash
# Local PostgreSQL
export DATABASE_URL=postgresql://career:career_pass@localhost:5432/career_guidance
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Web frontend |
| POST | `/api/students` | Register a student |
| GET | `/api/students` | List all students |
| GET | `/api/students/{id}` | Get student by ID |
| PUT | `/api/students/{id}` | Update student (edit profile) |
| POST | `/api/students/{id}/recommendations` | Generate ML recommendations |
| GET | `/api/students/{id}/recommendations` | Get saved recommendations |

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./career_guidance.db` | Database connection string |
| `CORS_ORIGINS` | `http://localhost:5173,...` | Comma-separated allowed origins |

---

## Docker + PostgreSQL (full stack)

```bash
docker compose up --build
```

Starts PostgreSQL 16 (`db`) + API (`api`). The API connects to PostgreSQL via `DATABASE_URL`.

To run only the API container:

```bash
docker build -t career-guidance-api .
docker run -p 8000:8000 career-guidance-api
```

---

## Project Structure

```
AI-Career-Guidance-Backend-Fixed/
├── app/
│   ├── main.py          # FastAPI application, routes & frontend serving
│   ├── database.py      # SQLAlchemy engine & session
│   ├── models.py        # Database models (Student, Recommendation)
│   ├── schemas.py       # Pydantic validation schemas
│   ├── ml_engine.py     # RandomForest ML pipeline
│   ├── seed.py          # Demo data seeder
│   └── static/          # Web frontend (multi-page, zero dependency)
│       ├── index.html
│       ├── register.html
│       ├── recommendations.html
│       ├── students.html
│       ├── style.css
│       └── app.js
├── ml/
│   └── career_model.joblib  # Serialized ML model
├── docker-compose.yml   # PostgreSQL + API stack
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Linode Cloud Hosting](https://www.linode.com/)

---

**Thank You!**
