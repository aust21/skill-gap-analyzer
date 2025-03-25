import os, redis
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def get_skills_from_groq():
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Explain the importance of fast language models",
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    print(chat_completion.choices[0].message.content)


def skills_exists(job_title: str):
    conn = redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=os.getenv("REDIS_PORT"),
        decode_responses=True,
        password=os.getenv("REDIS_PASSWORD"),
        username="default"
    )
    job_title = job_title.title()
    key = f"sk:{job_title}"

    data = conn.get(key)

    if data:
        return True
    return False