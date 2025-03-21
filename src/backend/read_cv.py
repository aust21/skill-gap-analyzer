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

def extract_skills(text, skill_list):

    # print("*"*50)
    # print(skill_list)
    # print("*" * 50)
    # print(text)
    # print("*" * 50)
    doc = nlp(text)
    skills = set()

    for token in doc:
        word = token.text.lower()
        # print(word)
        if (word.title() in skill_list
                or word in skill_list
                or word.capitalize() in skill_list
                or word.upper() in skill_list):
            skills.add(token.text)
    return skills

def main(resume_file, skills):

    text_resume = read_resume(resume_file)
    clean_text = preprocess_text(text_resume)
    skills_from_resume = extract_skills(clean_text, skills)
    return skills_from_resume