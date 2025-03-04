import os
import requests
import psycopg2, os, sys, logging
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.engine import create_engine
from dotenv import load_dotenv

load_dotenv()

# url = "https://jsearch.p.rapidapi.com/search"
#
# querystring = {
#     "query":"developer jobs in south africa",
#     "page":"1",
#     "num_pages":"1","country":"za","date_posted":"all"
# }
# API_KEY = os.getenv("RAPID_API")
# headers = {
# 	"x-rapidapi-key": API_KEY,
# 	"x-rapidapi-host": "jsearch.p.rapidapi.com"
# }
#
# response = requests.get(url, headers=headers, params=querystring)
#
# print(response.json())

def extract_skills(job_title):
    try:
        conf = {
            'host': os.getenv("HOST"),
            'port': os.getenv("PORT"),
            'database': os.getenv("DB"),
            'user': os.getenv("USER"),
            'password': os.getenv("PASSWORD")
        }
        engine = create_engine(
            "postgresql://postgres:65AnLzPWhgkQAKth@db.czgahlgpbgwzhjsmtpuy.supabase.co:5432/postgres".format(
                **conf
            )
        )
        session = sessionmaker(bind=engine)
        session_obj = session()
        logging.info("Connected to database")

        results = session_obj.execute(
            """
            SELECT DISTINCT s.skill
            FROM job_skills s
            JOIN job_titles j ON s.job_title_id = j.id
            WHERE LOWER(j.job_title) = LOWER(:job_title);
        """, {"job_title": job_title}
            )
        skills = results.fetchall()
        return [skill[0] for skill in skills]
    except Exception as e:
        logging.error(
            f"Something happened with extract jobs {e}"
                      , exc_info=True)

data = extract_skills("data engineer")
print(data)