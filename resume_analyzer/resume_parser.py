import spacy
import os
from file_handling import FileHandler

class ResumeParser:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.file_handler = FileHandler()

    def parse_resume(self, file_path):
        """Extracts text and key entities from a resume."""
        
        # Print the file path for debugging
        print("Processing file:", file_path)
        
        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Extract file extension
        file_extension = os.path.splitext(file_path)[1].lower()
        print("Detected extension:", file_extension)  # Debugging
        
        # Validate file extension
        if file_extension not in [".pdf", ".docx"]:
            raise ValueError(f"Unsupported file type: {file_extension}. Please provide a '.docx' or '.pdf' file.")
        
        # Extract text from the file
        resume_text = self.file_handler.extract_text(file_path)
        
        # Process text with NLP
        doc = self.nlp(resume_text)
        
        # Return extracted entities
        return {
            "text": resume_text,
            "entities": [(ent.text, ent.label_) for ent in doc.ents]
        }

if __name__ == "__main__":
    parser = ResumeParser()
    
    # Change this to the actual file path you are using

    
    try:
        result = parser.parse_resume()
        print(result)
    except Exception as e:
        print("Error:", e)
