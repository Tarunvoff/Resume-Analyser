import streamlit as st
import os
import tempfile
import matplotlib.pyplot as plt
from io import BytesIO
from fpdf import FPDF

# Local modules
from file_handling import FileHandler
from resume_parser import ResumeParser
from Job_matcher import JobMatcher
from ats_scoring import ATSScoring
from career_coaching import CareerCoach
from GenAI_module import ResumeAnalyzer

# 🌐 Apply Custom CSS
def local_css():
    st.markdown("""
        <style>
            .stApp {background-color: #f5f7fa;}
            .title {color: #007bff; font-size: 30px; font-weight: bold; text-align: center;}
            .subtitle {font-size: 18px; font-weight: bold; color: #444; text-align: center;}
            .upload-box {border: 2px dashed #007bff; padding: 15px; border-radius: 10px; background-color: #fff; text-align: center;}
            .stButton>button {background-color: #007bff; color: white; font-size: 16px; padding: 8px; border-radius: 5px;}
        </style>
    """, unsafe_allow_html=True)

# 🌟 Streamlit Page Setup
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
local_css()

# 🧾 Header
st.markdown('<p class="title">📄 AI-Powered Resume Analyzer</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload your resume and get detailed insights, job matching, ATS scoring, and career recommendations.</p>', unsafe_allow_html=True)

# 📤 File Upload
st.markdown('<div class="upload-box">📂 Upload your resume (PDF or DOCX format)</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("📂 Upload Your Resume", type=['pdf', 'docx'])

# 🔑 API Key Input
api_key = st.text_input("🔑 Enter your GEMINI API Key:", type="password")

# 👉 Proceed only if file and API key are provided
if uploaded_file and api_key:
    # Save uploaded file to temporary location
    temp_dir = tempfile.TemporaryDirectory()
    file_path = os.path.join(temp_dir.name, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    # Initialize Modules
    file_handler = FileHandler()
    resume_text = file_handler.extract_text(file_path)
    page_count = file_handler.get_file_page_count(file_path)
    st.success(f"✅ Resume Uploaded Successfully | Total Pages: {page_count}")

    resume_parser = ResumeParser()
    job_matcher = JobMatcher()
    ats_scoring = ATSScoring()
    career_coach = CareerCoach(api_key=api_key)
    resume_analyzer = ResumeAnalyzer(api_key)

    with st.spinner("🔍 Extracting resume details..."):
        parsed_resume = resume_parser.parse_resume(file_path)
    with st.expander("📊 Parsed Resume Details (Click to Expand)"):
        st.write(parsed_resume)

    # 🔎 Job Description Matching
    job_description = st.text_area("📝 Paste Job Description for Matching:")
    if job_description:
        with st.spinner("🔍 Matching resume with job description..."):
            job_match_score = job_matcher.match_resume_to_job(file_path, job_description)
            ats_score = ats_scoring.score_resume(resume_text, job_description)

        st.subheader("📊 Job Match & ATS Score")
        st.write(f"✅ **Job Match Score:** {job_match_score}%")
        st.write(f"✅ **ATS Score:** {ats_score}%")

    # 🧠 Resume Insights
    with st.spinner("🤖 Analyzing career insights..."):
        insights = resume_analyzer.get_resume_insights(resume_text)
    with st.expander("📊 Resume Insights (Click to Expand)"):
        st.write(insights)

    # 🧪 Skill Proficiency
    st.subheader("📌 Skills Analysis")
    skills_proficiency = resume_analyzer.extract_skills(resume_text)
    if skills_proficiency:
        skills = list(skills_proficiency.keys())
        proficiency = list(skills_proficiency.values())
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.barh(skills, proficiency, color='skyblue')
        ax.set_xlabel('Proficiency (%)')
        ax.set_title('Skills Proficiency Based on Resume Analysis')
        st.pyplot(fig)
    else:
        st.warning("⚠ No relevant skills found in the resume.")

    # 🧭 Career Coach
    st.subheader("💼 Career Advice")
    user_query = st.text_input("🔍 Ask the Career Coach:")
    if user_query:
        with st.spinner("🤖 Generating career advice..."):
            advice = career_coach.get_career_advice(resume_text, user_query)  # ✅ Corrected
        st.write(advice)

    # 📥 Downloads
    st.markdown("---")
    st.markdown("### 📥 Download Your Report")
    col1, col2 = st.columns(2)

    def create_pdf(text):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(200, 10, txt="Resume Insights", align="C")
        pdf.multi_cell(200, 10, txt=text)
        return pdf.output(dest='S').encode('latin1')

    with col1:
        if st.button("📄 Download Insights as PDF"):
            pdf_content = create_pdf(insights)
            st.download_button("Download PDF", data=pdf_content, file_name="resume_insights.pdf", mime="application/pdf")

    with col2:
        def convert_fig_to_bytes(fig):
            buf = BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)
            return buf.getvalue()

        if st.button("📊 Download Skill Analysis as PNG"):
            st.download_button("Download PNG", data=convert_fig_to_bytes(fig), file_name="skills_analysis.png", mime="image/png")

    temp_dir.cleanup()
else:
    st.info("📂 Please upload a resume and enter API key to get started.")

# 📎 Footer
st.markdown("---")
st.markdown("### 📚 Resume Insights by [Tarun V](https://www.linkedin.com/in/tarun-v-19196b329/)")
