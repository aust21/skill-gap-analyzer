import os
import requests
import psycopg2, os, sys, logging
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.engine import create_engine
from dotenv import load_dotenv

load_dotenv()

url = "https://jsearch.p.rapidapi.com/search"

querystring = {
    "query":"developer jobs in south africa",
    "page":"1",
    "num_pages":"1","country":"za","date_posted":"all"
}
API_KEY = os.getenv("RAPID_API")
headers = {
	"x-rapidapi-key": API_KEY,
	"x-rapidapi-host": "jsearch.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
