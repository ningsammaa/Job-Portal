import pytest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ai.skill_matcher import SkillMatcher

def test_skill_extraction():
    matcher = SkillMatcher()
    
    sample_text = "I have experience with Python, JavaScript, and React. Also worked with machine learning projects."
    skills = matcher.extract_skills(sample_text)
    
    assert 'python' in skills
    assert 'javascript' in skills
    assert 'react' in skills
    assert 'machine learning' in skills
    print("Skill extraction test passed!")

def test_experience_estimation():
    matcher = SkillMatcher()
    
    sample_text = "I have 5 years of experience in software development."
    experience = matcher.estimate_experience(sample_text)
    
    assert experience == 5
    print("Experience estimation test passed!")

if __name__ == "__main__":
    test_skill_extraction()
    test_experience_estimation()
    print("All tests passed!")