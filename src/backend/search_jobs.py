import os
import requests
import psycopg2, os, sys, logging
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("RAPID_API")
API_HOST = os.getenv("RAPID_API_HOST")

def search(job_title: str):
    url = "https://linkedin-data-api.p.rapidapi.com/search-jobs"

    querystring = {"keywords":job_title,"locationId":"92000000","datePosted":"anyTime","sort":"mostRelevant"}

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)

    # print(response.json()["data"][0]["id"])
    print(response.json())

    return response.json()["data"][0]["id"]

def get_descriptions(job_id: str):
    url = "https://linkedin-data-api.p.rapidapi.com/get-job-details"

    querystring = {"id": job_id}

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()["data"]["description"]

# search("data engineer")
# get_descriptions("4161827138")