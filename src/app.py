import streamlit as st
import source as source
import read_cv as cv_reader
import os

# Get the current directory where your Python script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct paths relative to src directory
html_path = os.path.join(current_dir, 'templates', 'index.html')
css_path = os.path.join(current_dir, 'static', 'style.css')

# Read HTML file
def read_html_file(html_file):
    with open(html_file, 'r') as f:
        return f.read()

# Read CSS file
def read_css_file(css_file):
    with open(css_file, 'r') as f:
        return f'<style>{f.read()}</style>'

# Load styles
css_content = read_css_file(css_path)
st.markdown(css_content, unsafe_allow_html=True)

# Create UI layout using Streamlit columns
st.markdown("<div class='container'>", unsafe_allow_html=True)

left, right = st.columns([1, 1])  # Two equal columns

with left:
    st.subheader("Upload Resume")
    resume_file = st.file_uploader("Attach your PDF resume", type="pdf")

with right:
    st.subheader("Enter Job Title")
    job_title = st.text_input("Job Title")

st.markdown("</div>", unsafe_allow_html=True)  # Close div

# Process input after user submits
if st.button("Analyse"):
    if resume_file and job_title:
        temp_path = f"temp_{resume_file.name}"
        with open(temp_path, "wb") as f:
            f.write(resume_file.read())

        skills = source.main(job_title)
        skills_from_resume = cv_reader.main(temp_path, skills)

        st.write("Extracted Skills:", skills_from_resume)
    st.write("This app is still in development.....")