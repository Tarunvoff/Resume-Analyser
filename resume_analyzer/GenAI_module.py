import spacy
from langchain.chat_models import ChatGoogleGemini
from langchain.schema import SystemMessage
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from collections import Counter

class ResumeAnalyzer:
    def __init__(self, api_key):
        """Initialize the ResumeAnalyzer with the Gemini API key and load the NLP model."""
        self.chat_model = ChatGoogleGemini(api_key=api_key)
        self.nlp = spacy.load("en_core_web_sm")  # Load spaCy model
        self.skills_list = [
            "Python", "Machine Learning", "Data Analysis", "Project Management",
            "Leadership", "Java", "C++", "SQL", "Communication", "Teamwork",
            "Problem Solving", "Deep Learning", "Artificial Intelligence",
            "Cloud Computing", "Cybersecurity", "Software Development",
            "Agile Methodologies", "DevOps", "Big Data", "Data Science",
            "Natural Language Processing", "Computer Vision"  # Extended skill list
        ]
        self.chain = self.setup_chat_model()  # Set up the chat model

    def setup_chat_model(self):
        """Set up the chat model with a template for processing resumes."""
        prompt = ChatPromptTemplate(
            input_variables=['resume_text'],
            messages=[
                SystemMessage(content="You are an elite AI consultant with expertise in psychometric evaluations and career trajectory analytics. You possess profound capabilities to assess complex professional histories and delineate strategic career development plans."),
                HumanMessagePromptTemplate.from_template(
                    "Proceed with an in-depth analysis of the submitted resume. Evaluate the candidate's educational and professional timeline, "
                    "identify pivotal skills and distinguishing achievements. Synthesize this data to construct a nuanced summary of potential career pathways. "
                    "Recommend refined strategies for career advancement considering emerging industry trends. Here is the resume content:\n\n{resume_text}"
                )
            ]
        )

        chain = LLMChain(
            llm=self.chat_model, 
            prompt=prompt, 
            verbose=True
        )

        return chain

    def extract_skills(self, resume_text):
        """Extract skills from the resume text and assess proficiency using NLP."""
        doc = self.nlp(resume_text)
        skill_counts = Counter()

        # Identify skills based on the predefined list
        for skill in self.skills_list:
            # Use spaCy's tokenizer to find exact matches
            skill_tokens = self.nlp(skill.lower())
            for token in doc:
                if token.lemma_ == skill_tokens[0].lemma_:  # Match lemmatized form
                    skill_counts[skill] += 1

        # Calculate proficiency based on counts
        proficiency = {skill: min(count * 20, 100) for skill, count in skill_counts.items() if count > 0}

        return proficiency  # Return the proficiency dictionary

    def get_resume_insights(self, resume_text):
        """Generate insights from the resume by running the chat model."""
        try:
            response = self.chain.run({'resume_text': resume_text})  # Use the pre-setup chain
            return response
        except Exception as e:
            print(f"Error processing the resume: {e}")
            return "Error processing the resume as your API key is Invalid!!!"
