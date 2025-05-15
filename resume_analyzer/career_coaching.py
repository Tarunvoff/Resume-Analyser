# career_coach.py
# AI Career Coach Chatbot

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate


class CareerCoach:
    def __init__(self, api_key):
        self.chat_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=api_key)
        self.chain = self.setup_chat_model()

    def setup_chat_model(self):
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""
                You are an AI-powered career coach with expertise in job search strategies, 
                resume optimization, interview preparation, and professional development.

                The user will provide their resume and a career-related question.
                You must answer based on both the resume and the query.

                Tailor all advice to the user's resume details such as skills, experience, education, and career goals.
            """),
            HumanMessagePromptTemplate.from_template("""
                Resume:
                {resume}

                Question:
                {user_query}
            """)
        ])
        return LLMChain(llm=self.chat_model, prompt=prompt, verbose=True)

    def get_career_advice(self, resume_text, user_query):
        try:
            return self.chain.run({'resume': resume_text, 'user_query': user_query})
        except Exception as e:
            return f"Error generating advice: {str(e)}"

if __name__ == "__main__":
    api_key = "your_google_api_key_here"  # Replace with actual API key
    coach = CareerCoach(api_key)
    query = "How can I transition from a software engineer to a data scientist?"
    response = coach.get_career_advice(query)
    print(response)
