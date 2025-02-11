import pandas as pd
import psycopg2, os
from dotenv import load_dotenv

load_dotenv("../.env")

# TODO: Load skills from an API or job source data
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'resources', 'sample_data.json')
file = pd.read_json(file_path)

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = int(os.getenv("port"))
DBNAME = os.getenv("dbname")

# print(USER, PASSWORD, HOST, PORT, DBNAME)
conn = psycopg2.connect(
    dbname=DBNAME,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=int(PORT)
)
cursor = conn.cursor()


def create_job_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_titles (
        id SERIAL PRIMARY KEY,
        job_title VARCHAR(255) UNIQUE NOT NULL
    );
    """)
    conn.commit()


def create_skills_table():
    cursor.execute("""
    DROP TABLE IF EXISTS skills;
    CREATE TABLE skills (
        id SERIAL PRIMARY KEY,
        job_title_id INT REFERENCES job_titles(id) ON DELETE CASCADE,
        skill VARCHAR(255) NOT NULL,
        CONSTRAINT unique_job_skill UNIQUE (job_title_id, skill)
    );
    """)
    conn.commit()

def create_data():
    for record in file.to_dict(orient="records"):
        job_title = record['job_title'].strip()
        skills = record['skills']
        print(f"Processing record: {record}")

        # Insert job title
        cursor.execute("""
            INSERT INTO job_titles (job_title)
            VALUES (%s)
            ON CONFLICT (job_title) DO NOTHING
            RETURNING id;
        """, (job_title,))

        result = cursor.fetchone()
        if result:
            job_title_id = result[0]
        else:
            # If there was a conflict (job title already exists), get its ID
            cursor.execute("""
                SELECT id FROM job_titles WHERE job_title = %s;
            """, (job_title,))
            job_title_id = cursor.fetchone()[0]

        # Insert skills with explicit reference to the unique constraint
        for skill in skills:
            cursor.execute("""
                INSERT INTO skills (job_title_id, skill)
                VALUES (%s, %s)
                ON CONFLICT ON CONSTRAINT unique_job_skill DO NOTHING;
            """, (job_title_id, skill))

        conn.commit()  # Commit after each job title and its skills


def extract_skills(job_title):
    cursor.execute("""
        SELECT DISTINCT s.skill
        FROM skills s
        JOIN job_titles j ON s.job_title_id = j.id
        WHERE LOWER(j.job_title) = LOWER(%s);
    """, (job_title,))
    skills = cursor.fetchall()
    return [skill[0] for skill in skills]


def main(job_title):
    try:
        create_job_table()
        create_skills_table()
        create_data()
        skills = extract_skills(job_title)

        return skills

    except Exception as e:
        print("Error during database operation:", e)
        return None
    finally:
        cursor.close()
        conn.close()