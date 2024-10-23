import tkinter as tk
from tkinter import filedialog, Label, Button, Frame, Scrollbar, Text
from resume_analysis import ResumeAnalyzer, TextExtractor
from file_handling import FileHandler
from GenAI_module import ChatBot

# Domain skills and weights configurations
domains = {
    "Software Development": {
        "Embedded Systems": {
            "expected": ["Embedded C", "Real-Time Systems", "AUTOSAR", "RTOS", "Microcontrollers"],
            "found": []
        },
        "ADAS": {
            "expected": ["Sensor Fusion", "ADAS", "MATLAB/Simulink", "Embedded C", "AUTOSAR"],
            "found": []
        },
        "Software Engineering": {
            "expected": ["Model-Based Design", "Software Testing and Validation", "Python", "C++", "Agile Methodologies"],
            "found": []
        },
        "Web Development": {
            "expected": ["JavaScript", "HTML5", "CSS", "React", "Angular", "Web APIs", "Node.js"],
            "found": []
        }
    },
    "Data Analysis": {
        "Data Science": {
            "expected": ["Machine Learning", "Deep Learning", "Python", "R", "Data Visualization", "Statistical Analysis"],
            "found": []
        },
        "Data Engineering": {
            "expected": ["Big Data Technologies", "Hadoop", "Spark", "Data Warehousing", "ETL Processes", "SQL"],
            "found": []
        }
    }
}

weights = {
    'basic_info': 20,
    'skills': 30,
    'education': 20,
    'domain_skills': 30
}

class UIManager:
    def __init__(self, master):
        """Initialize the UI manager with all components."""
        self.master = master
        self.text_extractor = TextExtractor()
        self.resume_analyzer = ResumeAnalyzer(domains, weights)
        self.chat_bot = ChatBot()
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface for the resume analyzer application."""
        self.master.title("Resume Analyzer")
        self.master.geometry("1000x600")

        self.left_frame = Frame(self.master, width=500, height=600, bg='light grey')
        self.left_frame.pack(side='left', fill='y')

        self.right_frame = Frame(self.master, width=500, height=600, bg='white')
        self.right_frame.pack(side='right', fill='y')

        self.resume_text = Text(self.left_frame, wrap='word', yscrollcommand=set())
        scrollbar = Scrollbar(self.left_frame, command=self.resume_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.resume_text.config(yscrollcommand=scrollbar.set)
        self.resume_text.pack(expand=True, fill='both', padx=10, pady=10)

        open_file_btn = Button(self.right_frame, text="Open File", padx=10, pady=5, fg='white', bg='#4CAF50', command=self.load_file)
        open_file_btn.pack(pady=20)

        self.output_text = tk.StringVar()
        output_label = Label(self.right_frame, textvariable=self.output_text, bg='white', fg='#333', font=('Helvetica', 12), justify='left', anchor='nw', wraplength=480)
        output_label.pack(fill='both', expand=True, padx=10, pady=10)

        self.ai_response_text = Text(self.right_frame, wrap='word', yscrollcommand=set())
        ai_scrollbar = Scrollbar(self.right_frame, command=self.ai_response_text.yview)
        ai_scrollbar.pack(side='right', fill='y')
        self.ai_response_text.config(yscrollcommand=ai_scrollbar.set)
        self.ai_response_text.pack(expand=True, fill='both', padx=10, pady=10)

    def load_file(self):
        """Handle file loading for resume analysis."""
        file_path = filedialog.askopenfilename(initialdir="/", title="Select file",
                                               filetypes=(("documents", "*.docx;*.pdf"), ("all files", "*.*")))
        if file_path:
            self.display_resume(file_path)
            self.process_file(file_path)

    def display_resume(self, file_path):
        """Display the resume text in the UI."""
        text = FileHandler.extract_text(file_path)
        self.resume_text.delete(1.0, tk.END)
        self.resume_text.insert(tk.END, text)

    def process_file(self, file_path):
        """Process the resume file and display analysis results."""
        text = FileHandler.extract_text(file_path)
        name = self.text_extractor.extract_name(text)
        email = self.text_extractor.extract_email(text)
        mobile_number = self.text_extractor.extract_mobile_number(text)
        degrees = self.text_extractor.extract_degree(text)
        skills_found = self.resume_analyzer.extract_skills(text)
        domain, sub_domain = self.resume_analyzer.suggest_domain_and_subdomain(skills_found)
        score = self.resume_analyzer.score_resume(name, email, mobile_number, degrees, skills_found, domain, sub_domain)
        self.display_results(name, email, mobile_number, domain, sub_domain, degrees, score)
        self.display_ai_insights(text)

    def display_results(self, name, email, mobile_number, domain, sub_domain, degrees, score):
        """Display the analysis results in the UI."""
        result_text = (f"Name: {name}\nEmail: {email}\nMobile Number: {mobile_number}\n"
                       f"Recommended Domain: {domain}\nRecommended Sub-Domain: {sub_domain}\nDegrees: {degrees}\nScore: {score}%")
        self.output_text.set(result_text)

    def display_ai_insights(self, resume_text):
        """Display AI-generated insights based on the resume text."""
        ai_insights = self.chat_bot.get_resume_insights(resume_text)
        if ai_insights:
            self.ai_response_text.insert(tk.END, "\n\nAI Insights:\n" + ai_insights)
        else:
            self.ai_response_text.insert(tk.END, "\n\nAI Insights:\nNo insights available.")

    def mainloop(self):
        """Run the main loop for the tkinter application."""
        self.master.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    app = UIManager(root)
    app.mainloop()
