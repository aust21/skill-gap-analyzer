import json

import psycopg2, os, sys, logging
import redis
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

load_dotenv()
# TODO: Load skills from an API or job source data

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = int(os.getenv("port"))
DBNAME = os.getenv("dbname")

# print(USER, PASSWORD, HOST, PORT, DBNAME)

def create_data(cursor, conn, file):
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
    try:
        pool = redis.ConnectionPool(
            decode_responses=True,
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            password=os.getenv("REDIS_PASSWORD"),
            username="default"
        )
        r = redis.Redis(connection_pool=pool)

        key = f"sk:{job_title.title()}"
        data = r.get(key)

        if not data:
            return ["Skill not yet available"]
        # print("-" * 50)
        # print(key)
        # print(data)
        # print("-" * 50)
        data = json.loads(data)
        return data["skills"]

    except Exception as e:
        logging.error(
            f"Something happened with extract jobs {e}"
                      , exc_info=True)


def main(job_title, cursor, conn):
    try:
        # create_job_table()
        # create_skills_table()
        # create_data()
        skills = extract_skills(job_title)

        return skills

    except Exception as e:
        print("Error during database operation:", e)
        return None
    finally:
        cursor.close()
        conn.close()