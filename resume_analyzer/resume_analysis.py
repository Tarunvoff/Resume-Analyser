import streamlit as st
import os
import tempfile
import matplotlib.pyplot as plt
from io import BytesIO
from fpdf import FPDF
from file_handling import FileHandler
from GenAI_module import ResumeAnalyzer  # Fixed incorrect import

# Apply Custom CSS
def local_css():
    st.markdown("""
        <style>
            .stApp {background-color: #f5f7fa;}
            .main-title {color: #007bff; font-size: 28px; font-weight: bold; text-align: center;}
            .sub-title {font-size: 18px; font-weight: bold; color: #333;}
            .upload-box {border: 2px dashed #007bff; padding: 15px; border-radius: 10px; background-color: #fff;}
            .button {background-color: #007bff; color: white; font-size: 16px; padding: 8px; border-radius: 5px;}
        </style>
    """, unsafe_allow_html=True)

# Initialize UI
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
local_css()

st.markdown('<p class="main-title">📄 AI-Powered Resume Analyzer</p>', unsafe_allow_html=True)

# Upload Section
st.markdown('<p class="sub-title">Upload Your Resume</p>', unsafe_allow_html=True)
st.markdown('<div class="upload-box">Upload a PDF or DOCX resume file to analyze your skills and career insights.</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=['pdf', 'docx'])

# API Key Input
api_key = st.text_input("🔑 Enter your GEMINI API Key:", type="password")

# Process the Uploaded File
if uploaded_file is not None:
    temp_dir = tempfile.TemporaryDirectory()
    temp_file_path = os.path.join(temp_dir.name, uploaded_file.name)

    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(uploaded_file.read())

    # Extract text from the resume (Hidden from UI)
    try:
        file_handler = FileHandler()
        resume_text = file_handler.extract_text(temp_file_path)  # ✅ Extract text but do NOT display

        # Display basic resume details
        page_count = file_handler.get_file_page_count(temp_file_path)
        st.success(f"✅ Resume Uploaded Successfully | Total Pages: {page_count}")

        # Check API Key
        if api_key:
            chatbot = ResumeAnalyzer(api_key)

            # Show Progress Spinner
            with st.spinner("🔍 Analyzing resume for career insights..."):
                insights = chatbot.get_resume_insights(resume_text)

            # Display Resume Insights
            with st.expander("📊 Resume Insights (Click to Expand)"):
                st.write(insights)

            # Generate and Display Skills Analysis
            st.subheader("📌 Skills Analysis")
            skills_proficiency = chatbot.extract_skills(resume_text)

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

            # Download Resume Insights as PDF
            def create_pdf(insights_text):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(200, 10, txt="Resume Insights", align="C")
                pdf.multi_cell(200, 10, txt=insights_text)
                return pdf.output(dest='S').encode('latin1')

            st.markdown("---")
            st.markdown("### 📥 Download Your Report")
            col1, col2 = st.columns(2)

            with col1:
                if st.button("📄 Download Insights as PDF"):
                    pdf_content = create_pdf(insights)
                    st.download_button(
                        label="Download PDF",
                        data=pdf_content,
                        file_name="resume_insights.pdf",
                        mime="application/pdf"
                    )

            with col2:
                def convert_fig_to_bytes(fig):
                    buf = BytesIO()
                    fig.savefig(buf, format="png")
                    buf.seek(0)
                    return buf.getvalue()

                if st.button("📊 Download Skill Analysis as PNG"):
                    st.download_button(
                        label="Download PNG",
                        data=convert_fig_to_bytes(fig),
                        file_name="skills_analysis.png",
                        mime="image/png"
                    )

        else:
            st.warning("⚠ Please provide an API key to generate insights.")

    except Exception as e:
        st.error(f"❌ Error processing the file: {e}")

    temp_dir.cleanup()
else:
    st.info("📂 Please upload a resume to get started.")

st.markdown("---")

# Footer
st.markdown("### 📚 Resume Insights by [Tarun V] 📞 [Contact Me](https://www.linkedin.com/in/tarun-v-19196b329/")