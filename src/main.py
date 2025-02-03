import src.source as source
import src.read_cv as cv_reader

resume_file = "/home/austin/Documents/docs/Austin_Ngobeni_CV.pdf"

def get_job_title():
    while True:
        job = input("Enter a job title: ").title()
        if job:
            return job

job_title = get_job_title() # "data engineer".title()

# Capture the returned skills list from source.main
skills = source.main(job_title)

cv_reader.main(resume_file, skills)
