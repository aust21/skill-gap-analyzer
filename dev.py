from src import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    

# import streamlit as st
# import source as source
# import read_cv as cv_reader
# import os

# # Get the current directory where your Python script is located
# current_dir = os.path.dirname(os.path.abspath(__file__))

# # Construct paths relative to src directory
# html_path = os.path.join(current_dir, 'templates', 'index.html')
# css_path = os.path.join(current_dir, 'static', 'style.css')


# def read_css_file(css_file):
#     with open(css_file, 'r') as f:
#         st.html(f"<style/>{f.read()}</style>")

# read_css_file(css_path)


# # Python code
# st.markdown("""
#     <style>
#         section[data-testid="stSidebar"] {
#             display: none;
#         }
#         .main .block-container {
#             max-width: 100%;
#             padding: 2rem;
#             margin: 0;
#         }
#         [data-testid="stSidebarNav"] {
#             display: none;
#         }
#         [data-testid="stHeader"] {
#             display: none;
#         }
#         div[data-testid="stToolbar"] {
#             display: none;
#         }
#         footer {
#             display: none;
#         }
#         .stApp {
#             margin: 0 auto;
#             font-family: -apple-system, BlinkMacSystemFont, sans-serif;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # Your container code
# with st.container():
#     cols = st.columns([1, 1])  # Equal width columns
    
#     with cols[0]:
#         st.subheader("Upload Resume")
#         resume_file = st.file_uploader("Attach your PDF resume", type="pdf")

#     with cols[1]:
#         st.subheader("Enter Job Title")
#         job_title = st.text_input("Job Title")
    

# # Process input after user submits
# if st.button("Analyse", key="analyse"):
#     if resume_file and job_title:
#         temp_path = f"temp_{resume_file.name}"
#         with open(temp_path, "wb") as f:
#             f.write(resume_file.read())

#         skills = source.main(job_title)
#         skills_from_resume = cv_reader.main(temp_path, skills)

#         st.write("Extracted Skills:", skills_from_resume)
#     st.write("This app is still in development.....")