from .resume_parser import process_resume_file
from .skill_matcher import SkillMatcher, update_parsed_resume_data
from .matching_engine import score_application, get_top_candidates

class AIService:
    def __init__(self):
        self.skill_matcher = SkillMatcher()
    
    def process_resume(self, user_id, file_path):
        try:
            # Step 1: Extract text from resume file
            resume_id, raw_text = process_resume_file(user_id, file_path)
            
            if not resume_id or not raw_text:
                return False, "Failed to process resume file"
            
            # Step 2: Extract skills, experience, and education
            skills = self.skill_matcher.extract_skills(raw_text)
            experience = self.skill_matcher.estimate_experience(raw_text)
            education = self.skill_matcher.extract_education(raw_text)
            
            # Step 3: Update database with parsed information
            success = update_parsed_resume_data(resume_id, skills, experience, education)
            
            if success:
                return True, f"Resume processed successfully. Found {len(skills)} skills."
            else:
                return False, "Failed to save parsed resume data"
                
        except Exception as e:
            return False, f"Error processing resume: {str(e)}"
    
    def score_job_application(self, application_id):
        try:
            success = score_application(application_id)
            return success, "Application scored successfully" if success else "Failed to score application"
        except Exception as e:
            return False, f"Error scoring application: {str(e)}"
    
    def get_recommended_candidates(self, job_id, limit=10):
        try:
            candidates = get_top_candidates(job_id, limit)
            return True, candidates
        except Exception as e:
            return False, f"Error getting candidates: {str(e)}"

# Global instance for easy access
ai_service = AIService()