import PyPDF2
import docx
import os
from database.db_connection import get_db_connection

class ResumeParser:
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx']
    
    def extract_text_from_pdf(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
            return ""
    
    def extract_text_from_docx(self, file_path):
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error reading DOCX {file_path}: {e}")
            return ""
    
    def extract_text(self, file_path):
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_ext == '.docx':
            return self.extract_text_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}. Supported formats: {self.supported_formats}")
    
    def save_resume_to_db(self, user_id, raw_text, file_path):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            
            # Check if resume already exists for this user
            cursor.execute("SELECT id FROM Resumes WHERE user_id = ?", (user_id,))
            existing_resume = cursor.fetchone()
            
            if existing_resume:
                # Update existing resume
                cursor.execute('''
                    UPDATE Resumes 
                    SET raw_text = ?, file_path = ?, parsed_successfully = FALSE, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                ''', (raw_text, file_path, user_id))
                resume_id = existing_resume['id']
            else:
                # Insert new resume
                cursor.execute('''
                    INSERT INTO Resumes (user_id, raw_text, file_path)
                    VALUES (?, ?, ?)
                ''', (user_id, raw_text, file_path))
                resume_id = cursor.lastrowid
            
            conn.commit()
            print(f"Resume for user {user_id} saved to database. Resume ID: {resume_id}")
            return resume_id
            
        except Exception as e:
            conn.rollback()
            print(f"Error saving resume to database: {e}")
            return None
        finally:
            conn.close()

def process_resume_file(user_id, file_path):
    parser = ResumeParser()
    
    try:
        # Extract text
        raw_text = parser.extract_text(file_path)
        
        if not raw_text:
            raise ValueError("No text could be extracted from the resume")
        
        # Save to database
        resume_id = parser.save_resume_to_db(user_id, raw_text, file_path)
        return resume_id, raw_text
        
    except Exception as e:
        print(f"Error processing resume: {e}")
        return None, None
    
    