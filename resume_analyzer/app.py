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

# Input for OpenAI API key
api_key = st.text_input("Enter your OpenAI API Key:", type="password")

# Upload a resume
uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=['pdf', 'docx'])

# Sidebar with information
st.sidebar.title("Quick Info")
st.sidebar.info("Supported file types: PDF and DOCX. The resume will be analyzed for key skills, career trajectory, and personalized career advice.")

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    temp_dir = tempfile.TemporaryDirectory()
    temp_file_path = os.path.join(temp_dir.name, uploaded_file.name)

    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(uploaded_file.read())

    # Extract text from the uploaded file
    try:
        resume_text = FileHandler.extract_text(temp_file_path)
        st.text_area("Extracted Resume Text", resume_text, height=300)

        # Initialize the ChatBot with the API key
        chatbot = ChatBot(api_key)  # Initialize ChatBot with the API key

        # Get insights using the chatbot
        insights = chatbot.get_resume_insights(resume_text)  # Call method on the instance

        # Display the insights
        st.subheader("Resume Insights:")
        st.write(insights)

        # Get the skills proficiency
        skills_proficiency = chatbot.extract_skills(resume_text)  # Call method on the instance

        # Display the skills analysis
        st.subheader("Skills Analysis")
        if skills_proficiency:
            skills = list(skills_proficiency.keys())
            proficiency = list(skills_proficiency.values())

            fig, ax = plt.subplots()
            ax.barh(skills, proficiency, color='skyblue')
            ax.set_xlabel('Proficiency (%)')
            ax.set_title('Skills Proficiency Based on Resume Analysis')
            st.pyplot(fig)
        else:
            st.write("No relevant skills found in the resume.")

        # Add a download button for the analysis as a PDF
        def create_pdf(insights_text):
            """Generate a PDF report of the resume insights."""
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

        # Download the skills analysis chart as a PNG
        def convert_fig_to_bytes(fig):
            buf = BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)
            return buf.getvalue()  # Use getvalue() to return the bytes directly

        if st.button("Download Skill Analysis as PNG"):
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
