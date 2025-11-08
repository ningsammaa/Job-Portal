import re
from database.db_connection import get_db_connection

class SkillMatcher:
    def __init__(self):
        self.known_skills = {
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php', 'go', 'rust', 'swift', 'kotlin',
            'sql', 'r', 'matlab', 'scala', 'perl',
            
            # Web Technologies
            'html', 'css', 'react', 'angular', 'vue', 'django', 'flask', 'fastapi', 'node.js', 'express.js',
            'spring', 'laravel', 'ruby on rails',
            
            # Databases
            'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'cassandra',
            
            # DevOps & Cloud
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins', 'git', 'ci/cd', 'terraform', 'ansible',
            
            # Data Science & AI
            'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
            'data analysis', 'data visualization', 'tableau', 'power bi', 'natural language processing', 'nlp',
            
            # Soft Skills
            'project management', 'agile', 'scrum', 'leadership', 'communication', 'problem solving', 'teamwork',
            'time management', 'critical thinking',
        }
    
    def extract_skills(self, text):
        if not text:
            return []
        
        text_lower = text.lower()
        found_skills = set()
        
        for skill in self.known_skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found_skills.add(skill)
        
        return list(found_skills)
    
    def estimate_experience(self, text):
        if not text:
            return 0
        
        # Patterns to find experience mentions
        experience_patterns = [
            r'(\d+)\+?\s*years?\s*experience',
            r'experience:\s*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s*in',
            r'(\d+)\+?\s*years?\s*of',
            r'(\d+)-(\d+)\s*years?\s*experience'
        ]
        
        max_experience = 0
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    # For ranges like "2-5 years", take the higher number
                    numbers = [int(m) for m in match if m.isdigit()]
                    if numbers:
                        max_experience = max(max_experience, max(numbers))
                else:
                    # Single number match
                    if match.isdigit():
                        max_experience = max(max_experience, int(match))
        
        return max_experience
    
    def extract_education(self, text):
        education_keywords = {
            'phd': 'PhD',
            'doctorate': 'PhD', 
            'master': 'Master',
            'bachelor': 'Bachelor',
            'bs': 'Bachelor',
            'ba': 'Bachelor',
            'associate': 'Associate',
            'high school': 'High School'
        }
        
        text_lower = text.lower()
        education_levels = []
        
        for keyword, level in education_keywords.items():
            if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                education_levels.append(level)
        
        return education_levels[0] if education_levels else "Not Specified"

def update_parsed_resume_data(resume_id, skills, experience, education):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        skills_str = ", ".join(skills) if skills else ""
        
        cursor.execute('''
            UPDATE Resumes 
            SET extracted_skills = ?, extracted_experience = ?, extracted_education = ?, 
                parsed_successfully = TRUE, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (skills_str, experience, education, resume_id))
        
        conn.commit()
        print(f"Parsed data for resume {resume_id} updated.")
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"Error updating parsed resume data: {e}")
        return False
    finally:
        conn.close()