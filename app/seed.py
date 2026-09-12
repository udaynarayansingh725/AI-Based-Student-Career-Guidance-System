"""
Seed demo data for the AI Career Guidance System.
Run the server first: python app/main.py
Then run this script: python app/seed.py

Uses only the standard library (no requests needed).
"""
import json
import urllib.request
import urllib.error

BASE = "http://localhost:8000"

# PPT Slide 6 example: Software Developer — 92% match
DEMO_STUDENTS = [
    {
        "name": "Demo Student",
        "email": "demo@hunters.com",
        "academic_score": 88,
        "programming": 92,
        "databases": 80,
        "problem_solving": 90,
        "communication": 70,
        "creativity": 55,
        "teamwork": 75,
        "analytical": 88,
        "interests": ["Technology", "AI/ML"],
        "personality": {"Analytical": "true", "Independent": "true"},
    },
    {
        "name": "Aarav Sharma",
        "email": "aarav@demo.com",
        "academic_score": 82,
        "programming": 78,
        "databases": 85,
        "problem_solving": 88,
        "communication": 75,
        "creativity": 50,
        "teamwork": 70,
        "analytical": 94,
        "interests": ["Data", "AI/ML"],
        "personality": {"Analytical": "true", "Detail-oriented": "true"},
    },
    {
        "name": "Priya Patel",
        "email": "priya@demo.com",
        "academic_score": 76,
        "programming": 42,
        "databases": 30,
        "problem_solving": 68,
        "communication": 92,
        "creativity": 96,
        "teamwork": 88,
        "analytical": 60,
        "interests": ["Design"],
        "personality": {"Creative": "true", "Social": "true"},
    },
    {
        "name": "Vikram Singh",
        "email": "vikram@demo.com",
        "academic_score": 85,
        "programming": 62,
        "databases": 68,
        "problem_solving": 82,
        "communication": 94,
        "creativity": 70,
        "teamwork": 90,
        "analytical": 86,
        "interests": ["Business", "Data"],
        "personality": {"Social": "true", "Analytical": "true"},
    },
    {
        "name": "Ananya Reddy",
        "email": "ananya@demo.com",
        "academic_score": 87,
        "programming": 88,
        "databases": 65,
        "problem_solving": 93,
        "communication": 72,
        "creativity": 44,
        "teamwork": 68,
        "analytical": 90,
        "interests": ["Cybersecurity", "Technology"],
        "personality": {"Analytical": "true", "Independent": "true", "Detail-oriented": "true"},
    },
]


def _post(url, payload=None):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode() if payload else None,
        headers={"Content-Type": "application/json"},
        method="POST" if payload else "GET",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {}


def seed():
    print("=" * 60)
    print("  AI Career Guidance System - Demo Data Seeder")
    print("  Team: Hunters Algorithm")
    print("=" * 60)
    print()

    for s in DEMO_STUDENTS:
        try:
            status, body = _post(f"{BASE}/api/students", s)
            if status == 201:
                sid = body["id"]
                _, rec = _post(f"{BASE}/api/students/{sid}/recommendations")
                top = rec["recommendations"][0]
                print(f"[+] {s['name']} (id={sid})")
                print(f"    Top match: {top['career']} - {top['match_percentage']}%")
                print(f"    Skills: {', '.join(top['skills'])}")
                print()
            elif status == 409:
                print(f"[=] {s['name']} - already exists")
        except Exception as e:
            print(f"[!] {s['name']} - error: {e}")

    print("-" * 60)
    _, students = _post(f"{BASE}/api/students")
    print(f"Total students: {len(students)}")
    print()
    print("Explore API docs: http://localhost:8000/docs")
    print("=" * 60)


if __name__ == "__main__":
    seed()