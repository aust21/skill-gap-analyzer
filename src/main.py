import src.source as source
import src.read_cv as cv_reader

resume_file = "/home/austin/Documents/docs/Austin_Ngobeni_CV.pdf"

def get_job_title():
    while True:
        job = input("Enter a job title: ").title()
        if job:
            return job

job_title = "data engineer".title()  # get_job_title()

# Capture the returned skills list from source.main
skills = source.main(job_title)

if skills is not None:
    cv_reader.main(resume_file, skills)
else:
    print("No skills found for the provided job title.")
