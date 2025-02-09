import streamlit as st

st.set_page_config(page_title="My App", layout="wide")

st.title("Skill gap analyser")

resume_file = st.file_uploader("Attach your pdf resume", type="pdf")
job_title = st.text_input("Enter job title")