# job_matcher.py
# AI Resume vs Job Match

import spacy
from collections import Counter
from resume_parser import ResumeParser

class JobMatcher:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.resume_parser = ResumeParser()

    def match_resume_to_job(self, resume_file, job_description):
        """Matches a resume against a job description based on skill overlap."""
        resume_data = self.resume_parser.parse_resume(resume_file)
        resume_text = resume_data["text"]
        
        job_doc = self.nlp(job_description)
        resume_doc = self.nlp(resume_text)
        
        job_keywords = [token.text.lower() for token in job_doc if token.is_alpha]
        resume_keywords = [token.text.lower() for token in resume_doc if token.is_alpha]
        
        match_score = sum((Counter(resume_keywords) & Counter(job_keywords)).values())
        total_keywords = len(set(job_keywords))
        match_percentage = (match_score / total_keywords) * 100 if total_keywords > 0 else 0

        return {"match_score": match_percentage, "matched_keywords": list(set(resume_keywords) & set(job_keywords))}

if __name__ == "__main__":
    matcher = JobMatcher()
    sample_resume = "sample_resume.pdf"  # Change to actual file path
    sample_job_desc = "Looking for a Python Developer with experience in Machine Learning and SQL."
    result = matcher.match_resume_to_job(sample_resume, sample_job_desc)
    print(result)
