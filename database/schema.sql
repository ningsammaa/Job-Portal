CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    user_type VARCHAR(50) NOT NULL CHECK (user_type IN ('job_seeker', 'recruiter')),
    full_name VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS Jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recruiter_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    required_skills TEXT NOT NULL,
    required_experience INTEGER DEFAULT 0,
    company_name VARCHAR(255),
    location VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recruiter_id) REFERENCES Users (id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS Resumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    raw_text TEXT NOT NULL,
    file_path VARCHAR(500),
    -- Parsed Fields
    extracted_skills TEXT,
    extracted_experience INTEGER,
    extracted_education TEXT,
    parsed_successfully BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users (id) ON DELETE CASCADE
);

-- Table for storing job applications
CREATE TABLE IF NOT EXISTS Applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    resume_id INTEGER NOT NULL,
    -- AI-Generated Scores
    skills_match_score REAL DEFAULT 0,
    experience_score REAL DEFAULT 0,
    overall_match_score REAL DEFAULT 0,
    application_status VARCHAR(50) DEFAULT 'pending' CHECK (application_status IN ('pending', 'reviewed', 'rejected', 'shortlisted')),
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES Jobs (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users (id) ON DELETE CASCADE,
    FOREIGN KEY (resume_id) REFERENCES Resumes (id) ON DELETE CASCADE,
    UNIQUE(job_id, user_id)
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_applications_scores ON Applications (overall_match_score DESC);
CREATE INDEX IF NOT EXISTS idx_resumes_skills ON Resumes (extracted_skills);
CREATE INDEX IF NOT EXISTS idx_jobs_skills ON Jobs (required_skills);