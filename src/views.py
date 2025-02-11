from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
import src.read_cv as cv_reader
import src.source as job_source  
import os

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("landing/landing.html")

@views.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    view = request.args.get("view", "dash")
    resume = request.files.get("resume")
    job_title = request.form.get("job")

    if request.method == "POST":
        if job_title:  # Store job title in session
            session["job_title"] = job_title
        
        if resume:
            print("resume uploaded---------------------")
            if not os.path.exists("uploads"):
                os.mkdir("uploads")
            
            # Save file temporarily
            resume_path = f"uploads/{resume.filename}"
            resume.save(resume_path)

            # Extract text from the resume
            extracted_text = cv_reader.read_resume(resume_path)
            clean_text = cv_reader.preprocess_text(extracted_text)
            # job_source.create_data()
            job_skills = job_source.extract_skills(job_title)

            # Extract skills from resume
            matched_skills = cv_reader.extract_skills(clean_text, job_skills)

            # Store results in session
            session["matched_skills"] = list(matched_skills)
            session["missing_skills"] = list(set(job_skills) - set(matched_skills))

            return redirect(url_for("views.dashboard"))

    # Retrieve job title from session if available
    job_title = session.get("job_title", "No Job Title Provided")
    
    matched_skills = session.get("matched_skills", [])
    missing_skills = session.get("missing_skills", [])

    return render_template("dash/dashboard.html", matched_skills=matched_skills, missing_skills=missing_skills, job=job_title, view=view)


