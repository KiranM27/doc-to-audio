"""Module for handling PDF-related operations"""
import PyPDF2
from tqdm import tqdm

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    print(f"\n📚 Reading PDF: {pdf_path}")
    text = ""
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in tqdm(reader.pages, desc="Extracting text", unit="page"):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text 