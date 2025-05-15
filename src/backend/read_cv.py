import spacy, re, pypdf, sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

nlp = spacy.load("en_core_web_sm")

def read_resume(path):
    extracted_text = ""
    resume = pypdf.PdfReader(path)

    for page in resume.pages:
        extracted_text += page.extract_text()
    return  extracted_text

def preprocess_text(text):

    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    return text