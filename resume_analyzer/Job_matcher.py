# job_matcher.py
# AI Resume vs Job Match

import spacy
from collections import Counter
from resume_parser import ResumeParser
import tempfile
import os
from collections import Counter

class JobMatcher:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.resume_parser = ResumeParser()

    # def match_resume_to_job(self, resume_file, job_description):
    #     """Matches a resume against a job description based on skill overlap."""

    #     # Save the uploaded file to a temporary file
    #     with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(resume_file.name)[1]) as temp_file:
    #         temp_file.write(resume_file.read())
    #         temp_file_path = temp_file.name

    #     # Parse the resume using the temporary file path
    #     resume_data = self.resume_parser.parse_resume(temp_file_path)
    #     resume_text = resume_data["text"]

    #     # NLP processing
    #     job_doc = self.nlp(job_description)
    #     resume_doc = self.nlp(resume_text)

    #     job_keywords = [token.text.lower() for token in job_doc if token.is_alpha]
    #     resume_keywords = [token.text.lower() for token in resume_doc if token.is_alpha]

    #     # Calculate matching score
    #     match_score = sum((Counter(resume_keywords) & Counter(job_keywords)).values())
    #     total_keywords = len(set(job_keywords))
    #     match_percentage = (match_score / total_keywords) * 100 if total_keywords > 0 else 0

    #     # Optionally delete temp file
    #     os.remove(temp_file_path)

    #     return {
    #         "match_score": match_percentage,
    #         "matched_keywords": list(set(resume_keywords) & set(job_keywords))
    #     }
    def match_resume_to_job(self, resume_text, job_description):
        """Matches resume text against a job description based on skill overlap."""

        # NLP processing
        job_doc = self.nlp(job_description)
        resume_doc = self.nlp(resume_text)

        job_keywords = [token.text.lower() for token in job_doc if token.is_alpha]
        resume_keywords = [token.text.lower() for token in resume_doc if token.is_alpha]

        # Calculate matching score
        from collections import Counter
        match_score = sum((Counter(resume_keywords) & Counter(job_keywords)).values())
        total_keywords = len(set(job_keywords))
        match_percentage = (match_score / total_keywords) * 100 if total_keywords > 0 else 0

        return {
            "match_score": match_percentage,
            "matched_keywords": list(set(resume_keywords) & set(job_keywords))
        }


if __name__ == "__main__":
    matcher = JobMatcher()
    sample_resume = "sample_resume.pdf"  # Change to actual file path
    sample_job_desc = "Looking for a Python Developer with experience in Machine Learning and SQL."
    result = matcher.match_resume_to_job(sample_resume, sample_job_desc)
    print(result)
