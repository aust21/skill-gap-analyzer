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
    # print(jobs[0]["id"])
    return jobs[0]["id"]
    

def get_descriptions(job_id: str):
    url = "https://linkedin-data-api.p.rapidapi.com/get-job-details"

    querystring = {"id": job_id}

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json()["data"]["description"])
    return response.json()["data"]["description"]

# search("data engineer")
# get_descriptions("4161827138")