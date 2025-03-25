import os, redis, json
from dotenv import load_dotenv
from groq import Groq
import src.backend.search_jobs as job_searcher

load_dotenv()

def get_skills_from_groq(job_title: str, description: str):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Can you extract the job skills for"
                           f" a {job_title} in the following "
                           f"description. I need only soft skills and "
                           f"technical skills, nothing else. Please give me "
                           f"the skills in json "
                           f"format.\nHere is the job description:\
                           n{description}",
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    data = chat_completion.choices[0].message.content
    json_data = json.loads(data)

    # Pretty-print the parsed JSON data
    print(json.dumps(json_data, indent=4))

    # Return the parsed data if needed
    return json_data


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

# job_id = job_searcher.search("data engineer")
# job_description = job_searcher.get_descriptions(job_id)
#
# get_skills_from_groq("data engineer", job_description)