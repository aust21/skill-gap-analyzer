import os
import requests
import psycopg2, os, sys, logging
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("RAPID_API")
API_HOST = os.getenv("RAPID_API_HOST")

def search(job_title: str):
    url = f"https://remotive.com/api/remote-jobs?category={job_title}"
    data = requests.get(url)
    jobs_data = data.json()
    jobs = jobs_data["jobs"]
    job = jobs[0]
    # print(jobs[0]["id"])
    return (job["id"], job["description"])
    

def get_descriptions(job_id: str):
    url = "https://linkedin-data-api.p.rapidapi.com/get-job-details"

    querystring = {"id": job_id}

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())
    return response.json()["data"]["description"]

id = search("data engineer")
get_descriptions(id[0])