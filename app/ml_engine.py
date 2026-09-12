from pathlib import Path
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

MODEL_PATH = Path(__file__).resolve().parent.parent / "ml" / "career_model.joblib"
FEATURES = [
    "academic_score", "programming", "databases", "problem_solving",
    "communication", "creativity", "teamwork", "analytical"
]

CAREERS = [
    "Software Developer", "Data Analyst", "UI/UX Designer",
    "Business Analyst", "Cybersecurity Analyst"
]

# Career archetypes: the ideal skill profile for each career path.
# The Hunters Algorithm matches a student's profile against these archetypes.
PROFILES = {
    "Software Developer": [88, 95, 86, 94, 72, 55, 78, 90],
    "Data Analyst": [82, 80, 88, 92, 78, 50, 72, 96],
    "UI/UX Designer": [78, 45, 35, 70, 90, 98, 85, 62],
    "Business Analyst": [84, 65, 70, 84, 95, 72, 92, 88],
    "Cybersecurity Analyst": [86, 90, 68, 95, 75, 45, 70, 92],
}

# ---- Random Forest model (trained on synthetic augmented profiles) ----
rng = np.random.default_rng(42)
X, y = [], []
for career, base in PROFILES.items():
    for _ in range(100):
        X.append(np.clip(np.array(base) + rng.normal(0, 8, len(base)), 0, 100))
        y.append(career)

encoder = LabelEncoder().fit(y)
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced",
)
model.fit(np.asarray(X), encoder.transform(y))

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
joblib.dump((model, encoder), MODEL_PATH)

INTEREST_WEIGHTS = {
    "Software Developer": {"Technology": 4, "AI/ML": 5},
    "Data Analyst": {"Data": 6, "AI/ML": 4, "Technology": 2},
    "UI/UX Designer": {"Design": 7},
    "Business Analyst": {"Business": 7, "Data": 2},
    "Cybersecurity Analyst": {"Cybersecurity": 8, "Technology": 2},
}

PERSONALITY_WEIGHTS = {
    "Software Developer": {"Analytical": 3, "Independent": 2, "Detail-oriented": 2},
    "Data Analyst": {"Analytical": 4, "Independent": 2, "Detail-oriented": 3},
    "UI/UX Designer": {"Creative": 5, "Social": 2},
    "Business Analyst": {"Social": 4, "Analytical": 3, "Detail-oriented": 1},
    "Cybersecurity Analyst": {"Analytical": 4, "Independent": 3, "Detail-oriented": 3},
}

CAREER_META = {
    "Software Developer": {
        "skills": ["Programming", "Databases", "Problem-Solving", "Logic", "Version Control"],
        "steps": ["Build 2-3 portfolio projects", "Practice DSA", "Learn Git and APIs"],
    },
    "Data Analyst": {
        "skills": ["SQL", "Python", "Statistics", "Problem-Solving", "Data Visualization"],
        "steps": ["Master SQL", "Build dashboard projects", "Learn pandas and Power BI"],
    },
    "UI/UX Designer": {
        "skills": ["Figma", "Creativity", "User Research", "Visual Design", "Communication"],
        "steps": ["Create a design portfolio", "Learn Figma", "Run usability tests"],
    },
    "Business Analyst": {
        "skills": ["Requirements", "Communication", "Analytics", "Documentation", "Teamwork"],
        "steps": ["Learn BA fundamentals", "Practice case studies", "Learn SQL and dashboards"],
    },
    "Cybersecurity Analyst": {
        "skills": ["Networking", "Security", "Problem-Solving", "Linux", "Risk Analysis"],
        "steps": ["Learn networking", "Practice labs", "Study security fundamentals"],
    },
}


def _skill_similarity(profile: dict, career: str) -> float:
    """0-1 similarity between a student's skill scores and a career archetype."""
    base = PROFILES[career]
    diffs = [abs(float(profile.get(f, 0)) - b) for f, b in zip(FEATURES, base)]
    return max(0.0, 1 - (sum(diffs) / len(diffs)) / 100)


def recommend(profile: dict, top_k: int = 5):
    """Rank careers for a student profile. Returns [(career, score)] where
    score is a 0-100 match percentage."""
    values = np.array([[float(profile.get(f, 0)) for f in FEATURES]])
    rf_probs = {
        career: float(prob)
        for career, prob in zip(encoder.inverse_transform(model.classes_), model.predict_proba(values)[0])
    }

    scores = {}
    for career in CAREERS:
        similarity = _skill_similarity(profile, career)
        interest_bonus = sum(
            INTEREST_WEIGHTS.get(career, {}).get(item, 0)
            for item in (profile.get("interests") or [])
        )
        personality = profile.get("personality") or {}
        personality_bonus = sum(
            weight
            for trait, weight in PERSONALITY_WEIGHTS.get(career, {}).items()
            if personality.get(trait)
        )
        bonus = min(interest_bonus + personality_bonus, 20)
        scores[career] = max(0.0, min(round(similarity * 80 + bonus, 1), 99.0))

    # Order by match score; Random Forest probability breaks near-ties.
    ranked = sorted(
        scores.items(),
        key=lambda c_s: (c_s[1], rf_probs.get(c_s[0], 0)),
        reverse=True,
    )
    return ranked[:top_k]


def explain(career: str, score: float):
    meta = CAREER_META[career]
    return {
        "career": career,
        "match_percentage": round(min(float(score), 99.9), 1),
        "reason": f"Your academic performance, skills, interests and personality show alignment with the core requirements of {career.lower()}.",
        "skills": meta["skills"],
        "next_steps": meta["steps"],
    }