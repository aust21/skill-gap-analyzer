def create_job_table(cursor, conn):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_titles (
        id SERIAL PRIMARY KEY,
        job_title VARCHAR(255) UNIQUE NOT NULL
    );
    """)
    conn.commit()


def create_skills_table(cursor, conn):
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