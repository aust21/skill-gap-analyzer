from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from src.backend.extract_skills import extract_skills
import src.backend.read_cv as cv_reader
import src.backend.source as job_source
import src.backend.main as process_skills
import src.backend.process as prc
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

    if request.method == "POST":
        if job_title:
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
            
            resume_analysis = extract_skills(job_title, resume_path)

            skills_in_resume = resume_analysis["resume_skills"]
            trending_skills = resume_analysis["trending_skills"]
            technical_skill_points = resume_analysis["technical_skill_score"]
            match_score = resume_analysis["overall_match"]
            soft_skill_score = resume_analysis["soft_skill_score"]
            domain_knowledge = resume_analysis["domain_knowledge"]
            tool_score = resume_analysis["tool_score"]
            strong_points = resume_analysis["strong_points"]
            missing_critical_skills = resume_analysis["missing_critical_skills"]
            tools_to_learn = resume_analysis["tools_to_learn"]
            resume_strength = resume_analysis["resume_strength"]
            career_insights = resume_analysis["career_insights"]
            recommendations = resume_analysis["recommendations"]

            session["skills_in_resume"] = skills_in_resume
            session["trending_skills"] = trending_skills
            session["technical_skill_points"] = technical_skill_points
            session["match_score"] = match_score
            session["soft_skill_score"] = soft_skill_score
            session["domain_knowledge"] = domain_knowledge
            session["tool_score"] = tool_score
            session["strong_points"] = strong_points
            session["missing_critical_skills"] = missing_critical_skills
            session["tools_to_learn"] = tools_to_learn
            session["resume_strength"] = resume_strength
            session["career_insights"] = career_insights
            session["recommendations"] = recommendations

            return redirect(url_for("views.dashboard"))

    # Retrieve job title from session if available
    job_title = session.get("job_title", "No Job Title Provided")
    
    extracted_sks = session.get("skills_in_resume", [])
    trending_sks = session.get("trending_skills", [])
    missing = session.get("missing_critical_skills", [])
    tech_points = session.get("technical_skill_points", "0")
    match_points = session.get("match_score", "0")
    soft_points = session.get("soft_skill_score", "0")
    domain_points = session.get("soft_skill_score", "0")
    tool_points = session.get("tool_score")
    strong = session.get("strong_points", [])
    tools_suggestion = session.get("tools_to_learn", [])
    strength = session.get("resume_strength", "")
    insigths = session.get("career_insights", "")
    recomm = session.get("recommendations", [])

    return render_template(
        "dash/index.html",
        extracted_skills=extracted_sks,
        skills_trending=trending_sks,
        missing = missing,
        job=job_title,
        tech_points = tech_points,
        match_points = match_points,
        soft_points = soft_points,
        domain_points=domain_points,
        tool_points = tool_points,
        strong = strong,
        tools_suggestion = tools_suggestion,
        strength = strength,
        insigths = insigths,
        recomm = recomm,
        view=view
    )



def current_jobs():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file = pd.read_json(os.path.join(current_dir, 'resources', 'sample_data.json'))
    jobs = set()
    for record in file.to_dict(orient="records"):
        job_title = record['job_title'].strip()
        jobs.add(job_title)

    return jobs