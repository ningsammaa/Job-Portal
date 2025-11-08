from database.db_connection import get_db_connection
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MatchingEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
    
    def calculate_skills_similarity(self, job_skills, resume_skills):
        if not job_skills or not resume_skills:
            return 0.0
        
        try:
            # Create TF-IDF matrix
            tfidf_matrix = self.vectorizer.fit_transform([job_skills, resume_skills])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            return float(similarity[0][0])
            
        except Exception as e:
            print(f"Error in skills similarity calculation: {e}")
            return self.fallback_similarity(job_skills, resume_skills)
    
    def fallback_similarity(self, job_skills, resume_skills):
        if not job_skills or not resume_skills:
            return 0.0
        
        job_skills_set = set(skill.strip().lower() for skill in job_skills.split(','))
        resume_skills_set = set(skill.strip().lower() for skill in resume_skills.split(','))
        
        if not job_skills_set:
            return 0.0
        
        intersection = job_skills_set.intersection(resume_skills_set)
        union = job_skills_set.union(resume_skills_set)
        
        return len(intersection) / len(union) if union else 0.0
    
    def calculate_experience_score(self, job_experience, resume_experience):
        if job_experience == 0:  # No experience requirement
            return 1.0
        
        if resume_experience >= job_experience:
            return 1.0
        else:
            # Linear scaling for partial match
            return resume_experience / job_experience
    
    def calculate_match_score(self, job_id, resume_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            
            # Get job data
            cursor.execute('''
                SELECT required_skills, required_experience 
                FROM Jobs WHERE id = ?
            ''', (job_id,))
            job = cursor.fetchone()
            
            if not job:
                print(f"Job {job_id} not found")
                return 0.0, 0.0, 0.0
            
            # Get resume data
            cursor.execute('''
                SELECT extracted_skills, extracted_experience 
                FROM Resumes WHERE id = ?
            ''', (resume_id,))
            resume = cursor.fetchone()
            
            if not resume or not resume['extracted_skills']:
                print(f"Resume {resume_id} not found or not parsed")
                return 0.0, 0.0, 0.0
            
            job_skills = job['required_skills']
            job_experience = job['required_experience'] or 0
            resume_skills = resume['extracted_skills']
            resume_experience = resume['extracted_experience'] or 0
            
            # Calculate individual scores
            skills_score = self.calculate_skills_similarity(job_skills, resume_skills)
            experience_score = self.calculate_experience_score(job_experience, resume_experience)
            
            # Calculate overall score (weighted average)
            overall_score = (skills_score * 0.7) + (experience_score * 0.3)
            
            return skills_score, experience_score, overall_score
            
        except Exception as e:
            print(f"Error calculating match score: {e}")
            return 0.0, 0.0, 0.0
        finally:
            conn.close()

def score_application(application_id):
    engine = MatchingEngine()
    conn = get_db_connection()
    
    try:
        cursor = conn.cursor()
        
        # Get application details
        cursor.execute('''
            SELECT a.id, a.job_id, a.resume_id 
            FROM Applications a 
            WHERE a.id = ?
        ''', (application_id,))
        
        application = cursor.fetchone()
        if not application:
            print(f"Application {application_id} not found")
            return False
        
        job_id = application['job_id']
        resume_id = application['resume_id']
        
        # Calculate scores
        skills_score, exp_score, overall_score = engine.calculate_match_score(job_id, resume_id)
        
        # Update application with scores
        cursor.execute('''
            UPDATE Applications 
            SET skills_match_score = ?, experience_score = ?, overall_match_score = ?
            WHERE id = ?
        ''', (skills_score, exp_score, overall_score, application_id))
        
        conn.commit()
        print(f"Application {application_id} scored. Overall: {overall_score:.2f}")
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"Error scoring application {application_id}: {e}")
        return False
    finally:
        conn.close()

def get_top_candidates(job_id, limit=10):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                u.id as user_id,
                u.full_name,
                u.email,
                r.extracted_skills,
                r.extracted_experience,
                a.overall_match_score,
                a.skills_match_score,
                a.experience_score
            FROM Applications a
            JOIN Users u ON a.user_id = u.id
            JOIN Resumes r ON a.resume_id = r.id
            WHERE a.job_id = ? 
            ORDER BY a.overall_match_score DESC
            LIMIT ?
        ''', (job_id, limit))
        
        candidates = cursor.fetchall()
        return [dict(candidate) for candidate in candidates]
        
    except Exception as e:
        print(f"Error getting top candidates: {e}")
        return []
    finally:
        conn.close()