from typing import Dict, List
import numpy as np

def calculate_match_score(candidate: Dict, jd_requirements: Dict) -> Dict:
    """
    Calculate match score between candidate and JD
    Returns score and explanation
    """
    required_skills = set([s.lower() for s in jd_requirements["required_skills"]])
    candidate_skills = set([s.lower() for s in candidate["skills"]])
    
    # Skill match
    matched_skills = required_skills.intersection(candidate_skills)
    skill_score = len(matched_skills) / len(required_skills) if required_skills else 1.0
    
    # Experience match
    required_exp = jd_requirements["required_experience"]
    candidate_exp = candidate["experience_years"]
    
    if candidate_exp >= required_exp:
        exp_score = 1.0
    else:
        exp_score = candidate_exp / required_exp
    
    # Combined score (70% skills, 30% experience)
    match_score = (skill_score * 0.7 + exp_score * 0.3) * 100
    
    # Generate explanation
    explanation = f"""
    **Match Analysis:**
    - ✅ Matched Skills: {', '.join(matched_skills) if matched_skills else 'None'}
    - ❌ Missing Skills: {', '.join(required_skills - candidate_skills)}
    - 💼 Experience: {candidate_exp} years (Required: {required_exp}+)
    - 📊 Skill Match Rate: {skill_score*100:.0f}%
    - 🎯 Overall Match: {match_score:.1f}/100
    """
    
    return {
        "score": round(match_score, 1),
        "explanation": explanation,
        "matched_skills": list(matched_skills),
        "missing_skills": list(required_skills - candidate_skills)
    }