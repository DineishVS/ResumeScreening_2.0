# matcher/resume_utils.py
import PyPDF2
import docx2txt

def extract_text_from_pdf(file_path):
    """
    Extract text content from a PDF file.

    Parameters:
    - file_path (str): Path to the PDF file.

    Returns:
    - str: Extracted text content.
    """
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    """
    Extract text content from a DOCX file.

    Parameters:
    - file_path (str): Path to the DOCX file.

    Returns:
    - str: Extracted text content.
    """
    return docx2txt.process(file_path)

def extract_text_from_txt(file_path):
    """
    Extract text content from a TXT file.

    Parameters:
    - file_path (str): Path to the TXT file.

    Returns:
    - str: Extracted text content.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_text(file_path):
    """
    Extract text content from supported file types (PDF, DOCX, TXT).

    Parameters:
    - file_path (str): Path to the file.

    Returns:
    - str: Extracted text content.
    """
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.txt'):
        return extract_text_from_txt(file_path)
    else:
        return ""
