import re
from typing import Dict, List

def parse_jd_simple(jd_text: str) -> Dict:
    """
    Simple rule-based JD parser (no API key needed)
    """
    jd_text_lower = jd_text.lower()
    
    # Extract skills (common tech keywords)
    common_skills = [
        "python", "java", "javascript", "react", "node.js", "aws", 
        "docker", "kubernetes", "sql", "mongodb", "tensorflow", 
        "pytorch", "django", "flask", "fastapi", "spring boot",
        "machine learning", "data science", "devops", "ci/cd",
        "html", "css", "typescript", "angular", "vue", "php", "ruby",
        "c++", "c#", "go", "rust", "swift", "kotlin", "azure", "gcp"
    ]
    
    found_skills = []
    for skill in common_skills:
        if skill in jd_text_lower:
            found_skills.append(skill)
    
    # Extract experience
    exp_match = re.search(r'(\d+)\+?\s*years?', jd_text_lower)
    required_years = int(exp_match.group(1)) if exp_match else 3
    
    # Extract role/title
    title_patterns = [r'(?:role|position|title):\s*([^\n]+)', r'looking for\s+([^\n]+)', r'^([^\n]+)']
    role = "Software Developer"
    for pattern in title_patterns:
        match = re.search(pattern, jd_text_lower)
        if match:
            role = match.group(1).strip()
            break
    
    return {
        "required_skills": found_skills,
        "required_experience": required_years,
        "role": role,
        "raw_jd": jd_text
    }

# No OpenAI here
