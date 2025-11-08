import sqlite3
import os

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'job_portal.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

def init_database():
    conn = get_db_connection()
    
    try:
        # Read and execute schema
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r') as sql_file:
            sql_script = sql_file.read()
        
        conn.executescript(sql_script)
        conn.commit()
        print(" Database initialized successfully!")
        
        # Insert sample data for testing
        insert_sample_data(conn)
        
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()

def insert_sample_data(conn):
    try:
        # Sample users
        users = [
            ('recruiter@company.com', 'hashed_password_123', 'recruiter', 'John Recruiter'),
            ('alice@email.com', 'hashed_password_456', 'job_seeker', 'Alice Johnson'),
            ('bob@email.com', 'hashed_password_789', 'job_seeker', 'Bob Smith')
        ]
        
        conn.executemany('''
            INSERT OR IGNORE INTO Users (email, password_hash, user_type, full_name)
            VALUES (?, ?, ?, ?)
        ''', users)
        
        # Sample jobs
        jobs = [
            (1, 'Python Developer', 'We are looking for a skilled Python developer with experience in web development and databases.', 
             'Python, SQL, FastAPI, Docker', 2, 'Tech Corp', 'New York'),
            (1, 'Data Scientist', 'Join our data science team to work on machine learning projects and data analysis.', 
             'Python, Machine Learning, SQL, Statistics', 3, 'Data Insights Inc', 'Remote'),
        ]
        
        conn.executemany('''
            INSERT OR IGNORE INTO Jobs (recruiter_id, title, description, required_skills, required_experience, company_name, location)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', jobs)
        
        conn.commit()
        print("Data inserted successfully!")
        
    except Exception as e:
        print(f"Could not insert data: {e}")