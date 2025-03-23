import os
import requests
import psycopg2, os, sys, logging
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("RAPID_API")
API_HOST = os.getenv("RAPID_API_HOST")

def search():
    url = "https://linkedin-data-api.p.rapidapi.com/search-jobs"

    querystring = {"keywords":"golang","locationId":"92000000","datePosted":"anyTime","sort":"mostRelevant"}

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())

def get_descriptions():
    url = "https://linkedin-data-api.p.rapidapi.com/get-job-details"

    querystring = {"id": "4090994054"}

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())