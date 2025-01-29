import requests
from env import API_KEY, APP_ID, RESULTS_PER_PAGE, COUNTRY

def get_job_postings(job_title):

    params = {
    "app_id": APP_ID,
    "app_key": API_KEY,
    "results_per_page": RESULTS_PER_PAGE,
    "what": job_title,
    "content-type": "application/json"
    }

    
    # Send request
    url = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/1"

    response = requests.get(url, params=params)

    # Parse response
    if response.status_code == 200:
        jobs = response.json().get("results", [])
        for job in jobs:
            print(f"Title: {job['title']}")
            print(f"Company: {job.get('company', {}).get('display_name', 'N/A')}")
            print(f"Location: {job['location']['display_name']}")
            print(f"Description: {job['description'][:200]}...")  # Truncated
            print(f"Job Link: {job['redirect_url']}")
            print("-" * 50)
    else:
        print("Error fetching jobs:", response.json())