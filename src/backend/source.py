import pandas as pd
import psycopg2, os, sys, logging
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.engine import create_engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

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