import os
from dotenv import load_dotenv

load_dotenv("../.env")

APP_ID = os.getenv("ADZUNA_APP_ID")
API_KEY = os.getenv("ADZUNA_API_KEY")

RESULTS_PER_PAGE = 10
COUNTRY = 'za'