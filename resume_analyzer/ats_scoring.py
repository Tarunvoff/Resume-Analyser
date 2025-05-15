# ats_scoring.py
# AI Resume Scoring & Improvements

import spacy
from Job_matcher import JobMatcher

class ATSScoring:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.job_matcher = JobMatcher()

    def score_resume(self, resume_text, job_description):
        """Scores the resume based on keyword match and readability."""

        match_result = self.job_matcher.match_resume_to_job(resume_text, job_description)
        match_score = match_result["match_score"]

        # Readability Score (basic approximation based on sentence length)
        sentences = resume_text.split(".")
        avg_sentence_length = sum(len(sent.split()) for sent in sentences) / max(len(sentences), 1)
        readability_score = max(100 - avg_sentence_length, 0)

        return {
            "match_score": match_score,
            "readability_score": readability_score,
            "overall_score": (match_score * 0.7) + (readability_score * 0.3)
        }

if __name__ == "__main__":
    ats = ATSScoring()
    sample_resume = "sample_resume.pdf"  # Change to actual file path
    sample_job_desc = "Looking for a Python Developer with experience in Machine Learning and SQL."
    result = ats.score_resume(sample_resume, sample_job_desc)
    print(result)
