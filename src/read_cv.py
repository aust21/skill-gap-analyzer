import PyPDF2, fitz, nltk, spacy, re

nlp = spacy.load("en_core_web_sm")

def read_resume(path):
    extracted_text = ""
    resume = fitz.open(path)
    for page in resume:
        extracted_text += page.get_text("text")
    return  extracted_text

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    return text

def extract_skills(text, skill_list):
    doc = nlp(text)
    skills = set()

    for token in doc:
        if token.text.title() in skill_list:
            # print(token.text)
            skills.add(token.text)
    return skills

def main(resume_file, skills):

    text_resume = read_resume(resume_file)
    clean_text = preprocess_text(text_resume)
    skills_from_resume = extract_skills(clean_text, skills)
    print(skills_from_resume)