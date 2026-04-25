import openai
import re
from typing import Dict, List

# You'll add your OpenAI API key later
openai.api_key = ""  # Add your key or use environment variable

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
        "machine learning", "data science", "devops", "ci/cd"
    ]
    
    found_skills = []
    for skill in common_skills:
        if skill in jd_text_lower:
            found_skills.append(skill)
    
    # Extract experience (look for numbers like "3+ years", "5 years")
    exp_match = re.search(r'(\d+)\+?\s*years?', jd_text_lower)
    required_years = int(exp_match.group(1)) if exp_match else 3  # default 3 years
    
    # Extract role/title
    title_patterns = [r'(?:role|position|title):\s*([^\n]+)', r'looking for\s+([^\n]+)']
    role = "Software Developer"  # default
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

def parse_jd_with_ai(jd_text: str, api_key: str) -> Dict:
    """
    Advanced JD parser using OpenAI (more accurate)
    """
    openai.api_key = api_key
    
    prompt = f"""
    Parse this job description and extract:
    1. Required skills (as a list)
    2. Required years of experience (as a number)
    3. Job role/title
    
    Job Description:
    {jd_text}
    
    Return in this exact JSON format:
    {{
        "required_skills": ["skill1", "skill2"],
        "required_experience": 3,
        "role": "Job Title"
    }}
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        return result
    except:
        # Fallback to simple parser if API fails
        return parse_jd_simple(jd_text)