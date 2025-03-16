from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
import src.backend.read_cv as cv_reader
import src.backend.source as job_source
import os, sys
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

views = Blueprint("views", __name__)

@views.route("/")
def home():
    jobs = current_jobs()
    return render_template(
        "landing/landing.html", jobs=jobs)


@views.route("/error")
def error():
    tag = request.args.get("tag", "resume")
    return render_template("error.html", tag=tag)


@views.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    view = request.args.get("view", "dash")
    resume = request.files.get("resume")
    job_title = request.form.get("job")
    tag = request.args.get("tag", "resume")

    # cursor, conn = job_source.connect_to_db()
    if request.method == "POST":
        if job_title:  # Store job title in session
            session["job_title"] = job_title

        if not resume and not job_title:
            return redirect(url_for("views.error", tag="r-t"))
        if not resume:
            return redirect(url_for("views.error", tag="resume"))
        if not job_title:
            return redirect(url_for("views.error", tag="title"))
        
        if resume:
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



def current_jobs():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file = pd.read_json(os.path.join(current_dir, 'resources', 'sample_data.json'))
    jobs = set()
    for record in file.to_dict(orient="records"):
        job_title = record['job_title'].strip()
        jobs.add(job_title)

    return jobs