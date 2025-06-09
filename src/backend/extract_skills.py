import logging
import os, json
from dotenv import load_dotenv
from google import genai

from constants.genai_schema import GenAISchema
from constants.main import prompt
from src.backend.read_cv import read_resume, preprocess_text

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

log = logging.getLogger(__name__)


def extract_skills(job_title, file_path):
    client = genai.Client(api_key=GEMINI_API_KEY)
    resume_text = read_resume(file_path)
    clean_text = preprocess_text(resume_text)
    prompt_to_generate = prompt(job_title, clean_text)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt_to_generate,
        config={
            "response_mime_type": "application/json",
            "response_schema": list[GenAISchema],
        },
    )
    try:
        return_val = json.loads(response.text)
        # print(return_val[0])
        return return_val[0]
    except Exception as err:
        log.error(f"Error: {err}")
        return None

# extract_skills("data engineer", "./Austin_Ngobeni_CV.pdf")