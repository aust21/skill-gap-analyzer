import PyPDF2, fitz, nltk, spacy

nlp = spacy.load("en_core_web_sm")

def read_resume(path):
    extracted_text = ""
    resume = fitz.open(path)
    for page in resume:
        extracted_text += page.get_text("text")
    return  extracted_text

# TODO: fetch common skills from an api or third party
def common_skills():
    return ["python", "java", "sql", "machine learning", "deep learning",
              "pandas", "numpy", "nlp", "tensorflow", "pytorch", "aws",
              "docker", "flask", "django", "data analysis"]

def extract_skills(text, skill_list):
    doc = nlp(text)
    skills = set()

    for token in doc:
        # print(token.text)
        if token.text in skill_list:
            skills.add(token.text)
    return skills

doc = "/home/austin/Documents/docs/Austin_Ngobeni_CV.pdf"
text_resume = read_resume(doc)
skills = common_skills()
skills_from_resume = extract_skills(text_resume, skills)
print(skills_from_resume)