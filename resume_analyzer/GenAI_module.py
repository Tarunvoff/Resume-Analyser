import spacy
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from collections import Counter
from spacy.matcher import PhraseMatcher

class ResumeAnalyzer:
    def __init__(self, api_key):
        self.chat_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=api_key)  # ✅ Fixed API key issue
        self.nlp = spacy.load("en_core_web_sm")
        self.skills_list = [
            "Python", "Machine Learning", "Data Analysis", "Project Management",
            "Leadership", "Java", "C++", "SQL", "Communication", "Teamwork",
            "Problem Solving", "Deep Learning", "Artificial Intelligence",
            "Cloud Computing", "Cybersecurity", "Software Development",
            "Agile Methodologies", "DevOps", "Big Data", "Data Science",
            "Natural Language Processing", "Computer Vision"
        ]
        self.chain = self.setup_chat_model()

    def setup_chat_model(self):
        prompt = ChatPromptTemplate(
            input_variables=['resume_text'],
            messages=[
                SystemMessage(content='''You are an advanced AI consultant with expertise in career trajectory analysis, professional skill assessment, and talent development. Your role is to meticulously analyze the provided resume, identify key technical and soft skills, and evaluate the candidate's expertise based on context, experience level, and industry relevance.

Carefully extract both explicitly mentioned skills and implied competencies inferred from job roles, projects, certifications, and education history. Categorize the identified skills into relevant domains such as programming languages, frameworks, analytical skills, leadership qualities, communication abilities, problem-solving aptitude, and domain-specific expertise.

Additionally, assess the depth of proficiency for each skill based on years of experience, project involvement, and role responsibilities. Provide a structured output that highlights the candidate’s strongest competencies, emerging skills, and areas for improvement. If applicable, suggest additional skills that would enhance their career prospects based on current industry trends.'''),
                HumanMessagePromptTemplate.from_template(
                    "Analyze the resume and provide career insights:\n\n{resume_text}"
                )
            ]
        )
        return LLMChain(llm=self.chat_model, prompt=prompt, verbose=True)

    def extract_skills(self, resume_text):
        matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        patterns = [self.nlp.make_doc(skill) for skill in self.skills_list]
        matcher.add("SKILLS", patterns)

        doc = self.nlp(resume_text)
        matches = matcher(doc)
        skill_counts = Counter([doc[start:end].text for _, start, end in matches])

        return {skill: min(count * 20, 100) for skill, count in skill_counts.items()}

    def get_resume_insights(self, resume_text):
        try:
            return self.chain.run({'resume_text': resume_text})
        except Exception as e:
            return f"Error processing the resume: {str(e)}"
