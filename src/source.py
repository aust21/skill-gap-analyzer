import pandas as pd
import psycopg2

# TODO: load skills from a third party source like an API
file = pd.read_json("resources/sample_data.json")
conn = psycopg2.connect(
    dbname="job_skills",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

def create_job_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_titles(
    id SERIAL PRIMARY KEY,
    job_title VARCHAR(255) UNIQUE NOT NULL
    );
    """)

def create_skills_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skills (
    id SERIAL PRIMARY KEY,
    job_title_id INT REFERENCES job_titles(id) ON DELETE CASCADE,
    skill VARCHAR(255) NOT NULL
    );
    """)

create_job_table()
create_skills_table()

conn.commit()
cursor.close()
conn.close()