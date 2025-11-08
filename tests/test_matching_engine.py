import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ai.matching_engine import MatchingEngine

def test_skills_similarity():
    engine = MatchingEngine()
    
    job_skills = "Python, SQL, JavaScript, React"
    resume_skills = "Python, SQL, HTML, CSS"
    
    similarity = engine.calculate_skills_similarity(job_skills, resume_skills)
    
    assert 0 <= similarity <= 1
    print(f"Skills similarity test passed! Score: {similarity:.2f}")

def test_experience_score():
    engine = MatchingEngine()
    
    # Test case 1: More experience than required
    score1 = engine.calculate_experience_score(3, 5)
    assert score1 == 1.0
    
    # Test case 2: Less experience than required
    score2 = engine.calculate_experience_score(5, 3)
    assert score2 == 0.6
    
    # Test case 3: No experience required
    score3 = engine.calculate_experience_score(0, 2)
    assert score3 == 1.0
    
    print("Experience score test passed!")

if __name__ == "__main__":
    test_skills_similarity()
    test_experience_score()
    print("All matching engine tests passed!")