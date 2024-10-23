import os
import zipfile
import xml.etree.ElementTree as ET
import pdfplumber
import docx

class FileHandler:
    @staticmethod
    def extract_text(file_path):
        """Extract text from a file based on its extension."""
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == '.docx':
            return FileHandler.extract_text_from_docx(file_path)
        elif file_extension == '.pdf':
            return FileHandler.extract_text_from_pdf(file_path)
        else:
            raise ValueError("Unsupported file type. Please provide a '.docx' or '.pdf' file.")

    @staticmethod
    def extract_text_from_docx(docx_path):
        """Extract text from a DOCX file."""
        doc = docx.Document(docx_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return "\n".join(full_text)

    @staticmethod
    def extract_text_from_pdf(pdf_path):
        """Extract text from a PDF file using pdfplumber."""
        text = ''
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + '\n'
        return text

    @staticmethod
    def get_file_page_count(file_path):
        """Get the number of pages in a file based on its extension."""
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == '.docx':
            docx = zipfile.ZipFile(file_path)
            xml_content = docx.read('docProps/app.xml')
            docx.close()
            root = ET.fromstring(xml_content)
            return int(root.find('{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}Pages').text)
        elif file_extension == '.pdf':
            with pdfplumber.open(file_path) as pdf:
                return len(pdf.pages)
        else:
            raise ValueError("Unsupported file type. Please provide a '.docx' or '.pdf' file.")
