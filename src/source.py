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


def create_data():
    for record in file.to_dict(orient="records"):
        job_title = record['job_title']
        skills = record['skills']

        # Insert the job title if it doesn't exist
        cursor.execute("""
            INSERT INTO job_titles (job_title)
            VALUES (%s)
            ON CONFLICT (job_title) DO NOTHING;
        """, (job_title,))

        # Get the job title ID (this assumes the job title is already inserted or exists)
        cursor.execute("""
            SELECT id FROM job_titles WHERE job_title = %s;
        """, (job_title,))
        job_title_id = cursor.fetchone()[0]

        # Insert skills associated with the job title
        for skill in skills:
            cursor.execute("""
                INSERT INTO skills (job_title_id, skill)
                VALUES (%s, %s);
            """, (job_title_id, skill))


def extract_skills(job_title):
    cursor.execute("""
        SELECT s.skill
        FROM skills s
        JOIN job_titles j ON s.job_title_id = j.id
        WHERE j.job_title = %s;
        """, (job_title,))

    # Fetch all results
    skills = cursor.fetchall()

    return [skill[0] for skill in skills]


def main(job_title):
    try:
        create_job_table()
        create_skills_table()
        create_data()
        skills = extract_skills(job_title)

        conn.commit()
        return skills

    except Exception as e:
        print("Error during database operation:", e)

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    job = input("Enter job title: ").title()
    main(job)
