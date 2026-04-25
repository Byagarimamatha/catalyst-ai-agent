from typing import Dict, List
import random

class OutreachSimulator:
    def __init__(self):
        self.conversations = {}
    
    def send_initial_message(self, candidate: Dict, jd_role: str) -> str:
        """Simulate sending initial outreach message"""
        message = f"""
🎯 **Opportunity Alert!**

Hi {candidate['name']},

We came across your profile as a {candidate['current_role']} and have an exciting {jd_role} role that matches your skills!

**Quick Questions:**
1. Are you currently open to new opportunities?
2. What's your expected salary range?
3. When could you potentially start?

Reply with your thoughts!

Best,
Catalyst AI Recruiter
"""
        return message
    
    def simulate_candidate_response(self, candidate_id: int, match_score: float) -> str:
        """Simulate candidate's response based on match score"""
        # Higher match score = more interested response
        if match_score > 80:
            responses = [
                "Very interested! This sounds perfect for me. I'm open to opportunities and can start in 2 weeks. Expected salary: $140k",
                "Yes, I'm actively looking! This role aligns well with my experience. Can start in 3 weeks. Looking for $150k+",
                "Definitely interested! The skills match perfectly. I'm available to start in 2 weeks. Salary expectation: $145k"
            ]
        elif match_score > 60:
            responses = [
                "I'm somewhat interested. Would like to learn more about the team and tech stack. Can start in a month. Expected around $130k",
                "Possibly interested. Can we connect for a quick chat? Currently have a 3-week notice period. Expecting $135k",
                "Sounds interesting but I'd need to understand the role better. Salary range: $125-140k"
            ]
        else:
            responses = [
                "Thanks for reaching out but I'm not currently looking. Best of luck!",
                "Not interested at this time. Thanks anyway.",
                "Already accepted another offer. Please remove me from your list."
            ]
        
        return random.choice(responses)
    
    def calculate_interest_score(self, response: str) -> Dict:
        """Calculate interest score based on response content"""
        response_lower = response.lower()
        
        # Positive keywords
        positive = ["interested", "interested", "yes", "active", "perfect", "exciting", "definitely"]
        # Negative keywords
        negative = ["not interested", "not looking", "no thanks", "already accepted", "not available"]
        
        pos_count = sum(1 for word in positive if word in response_lower)
        neg_count = sum(1 for word in negative if word in response_lower)
        
        # Calculate score
        if neg_count > 0:
            interest_score = 20
            interest_level = "Low"
        elif pos_count >= 2:
            interest_score = 90
            interest_level = "High"
        elif pos_count == 1:
            interest_score = 65
            interest_level = "Medium"
        else:
            interest_score = 40
            interest_level = "Low-Medium"
        
        # Extract availability and salary if mentioned
        availability = "Unknown"
        salary_expectation = "Unknown"
        
        import re
        # Look for start timeline
        if "week" in response_lower:
            availability = "Within weeks"
        elif "month" in response_lower:
            availability = "Within a month"
        
        # Look for salary
        salary_match = re.search(r'\$?(\d{5,6})k?', response_lower)
        if salary_match:
            salary_expectation = f"${salary_match.group(1)}k"
        
        return {
            "score": interest_score,
            "level": interest_level,
            "availability": availability,
            "salary": salary_expectation,
            "full_response": response
        }