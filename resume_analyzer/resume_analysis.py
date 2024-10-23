import streamlit as st
import os
import tempfile
import matplotlib.pyplot as plt
from io import BytesIO
from fpdf import FPDF
from file_handling import FileHandler
from GenAI_module import ChatBot

# Streamlit app UI
st.set_page_config(page_title="Resume Analyzer", layout="wide")
st.title("AI-Powered Resume Analyzer")

# Instructions
st.markdown("""
Upload your resume in either PDF or DOCX format. Our AI model will extract relevant information from your resume and provide a detailed analysis, including career insights, skills assessments, and suggested career pathways.
""")

# Input for API key
api_key = st.text_input("Enter your OpenAI API key")

# Initialize FileHandler
file_handler = FileHandler()

# Upload a resume
uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=['pdf', 'docx'])

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    temp_dir = tempfile.TemporaryDirectory()
    temp_file_path = os.path.join(temp_dir.name, uploaded_file.name)

    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(uploaded_file.read())

    # Extract text from the uploaded file
    try:
        resume_text = file_handler.extract_text(temp_file_path)
        st.text_area("Extracted Resume Text", resume_text, height=300)

        # Get the number of pages in the file
        page_count = file_handler.get_file_page_count(temp_file_path)
        st.write(f"Total pages: {page_count}")

        # Check if API key is provided
        if api_key:
            chat_bot = ChatBot(api_key)  # Initialize with API key

            # Generate insights using the chatbot
            st.write("Analyzing resume for career insights...")
            insights = chat_bot.get_resume_insights(resume_text)

            # Display the insights
            st.subheader("Resume Insights:")
            st.write(insights)

            # Add a download button for the analysis as a PDF
            def create_pdf(insights_text):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(200, 10, txt="Resume Insights", align="C")
                pdf.multi_cell(200, 10, txt=insights_text)
                return pdf.output(dest='S').encode('latin1')

            if st.button("Download Insights as PDF"):
                pdf_content = create_pdf(insights)
                st.download_button(
                    label="Download PDF",
                    data=pdf_content,
                    file_name="resume_insights.pdf",
                    mime="application/pdf"
                )
        else:
            st.warning("Your insights will not be available until you provide an API key.")

        # Plot skills analysis chart (Placeholder)
        st.subheader("Skills Analysis")
        skills = ["Python", "Machine Learning", "Project Management", "Data Analysis", "Leadership"]
        proficiency = [80, 70, 90, 85, 60]

        fig, ax = plt.subplots()
        ax.barh(skills, proficiency, color='skyblue')
        ax.set_xlabel('Proficiency (%)')
        ax.set_title('Skills Proficiency Based on Resume Analysis')

        st.pyplot(fig)

        # Download the chart as a PNG
        def convert_fig_to_bytes(fig):
            buf = BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)
            return buf

        st.download_button(
            label="Download Skill Analysis as PNG",
            data=convert_fig_to_bytes(fig),
            file_name="skills_analysis.png",
            mime="image/png"
        )

    except Exception as e:
        st.error(f"Error processing the file: {e}")

else:
    st.write("Please upload a resume to get started.")

# Clean up temp files after usage
if 'temp_dir' in locals():
    temp_dir.cleanup()
