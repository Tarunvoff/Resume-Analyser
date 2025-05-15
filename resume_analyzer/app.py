from flask import Flask, request, render_template, jsonify
from ats_scoring import ATSScoring
from career_coaching import CareerCoach
from resume_analysis import ResumeAnalyzer
import os

# Initialize Flask app
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize components
ats = ATSScoring()
career_coach = CareerCoach(api_key="AIzaSyCkfedzi5Y-YmFMixYVFx3valNtxQSfp10")
analyzer = ResumeAnalyzer(api_key="AIzaSyCkfedzi5Y-YmFMixYVFx3valNtxQSfp10")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        resume_file = request.files['resume']
        job_description = request.form['job_description']
        user_query = request.form.get('user_query', 'What should I improve in my resume?')

        if not resume_file:
            return "No resume file uploaded", 400

        # Save uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
        resume_file.save(file_path)

        # Score resume
        with open(file_path, 'rb') as f:
            ats_result = ats.score_resume(f, job_description)

        # Extract resume text for analysis
        from file_handling import FileHandler
        resume_text = FileHandler.extract_text(file_path)

        # Get career advice & insights
        career_advice = career_coach.get_career_advice(user_query)
        skill_scores = analyzer.extract_skills(resume_text)
        resume_insights = analyzer.get_resume_insights(resume_text)

        return jsonify({
            "ats_result": ats_result,
            "career_advice": career_advice,
            "skills": skill_scores,
            "insights": resume_insights
        })

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
