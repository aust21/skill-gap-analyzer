import src.backend.read_cv as cv_reader
import src.backend.source as job_source
import src.backend.extract_skills as skill_extractor

def run(job_title, resume_path):
    skill_in_redis = skill_extractor.skills_exists(job_title)
    if skill_in_redis:
        print(f"********skill: {job_title} found in redis***********")
        extracted_text = cv_reader.read_resume(resume_path)
        clean_text = cv_reader.preprocess_text(extracted_text)
        job_skills = job_source.extract_skills(job_title)
        matched_skills = cv_reader.extract_skills(clean_text, job_skills)
        return matched_skills, job_skills
    # print(f"********skill: {job_title} not found***********")
    return ["No matched skill"], []