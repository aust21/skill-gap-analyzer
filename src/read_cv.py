import PyPDF2, fitz, nltk

def read_resume(path):
    extracted_text = ""
    resume = fitz.open(path)
    for page in resume:
        extracted_text += page.get_text("text")
    return  extracted_text

def common_skills():
    return ["python", "java", "sql", "machine learning", "deep learning",
              "pandas", "numpy", "nlp", "tensorflow", "pytorch", "aws",
              "docker", "flask", "django", "data analysis"]

text_resume = read_resume("resume")