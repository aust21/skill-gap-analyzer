# Dynamic Skill Gap Analyzer

## Overview

The **Dynamic Skill Gap Analyzer** is a data engineering project that fetches job postings from **Adzuna**, extracts required skills using **Natural Language Processing (NLP)**, and compares them to a user's resume. The goal is to identify skill gaps and provide recommendations for career improvement.

## Features

NB: **The project is still in developement and not all features are implemented yet**  
✅ Fetch job postings dynamically using **Adzuna API**  
✅ Extract required job skills using **NLP (spaCy)**  
✅ Parse and analyze a user's resume for existing skills  
✅ Identify missing skills for career improvement  
✅ Store job data in **PostgreSQL** for historical analysis  
✅ Visualize data and insights using **Streamlit**

## Tech Stack

- **Python** (Data Processing & NLP)
- **Adzuna API** (Job Listings)
- **spaCy** (Skill Extraction)
- **PostgreSQL** (Database Storage)
- **Streamlit** (Dashboard Visualization)

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL
- Adzuna API Key

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/aust21/skill-gap-analyzer.git
   cd skill-gap-analyzer
   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up PostgreSQL database:
   ```sql
   CREATE DATABASE skillgap;
   ```
   ```sql
   CREATE TABLE jobs (
       id SERIAL PRIMARY KEY,
       title TEXT,
       company TEXT,
       location TEXT,
       description TEXT,
       skills TEXT[],
       job_link TEXT
   );
   ```
4. Add your **Adzuna API credentials** to `.env`:

4.1. Go to [Adzuna](https://developer.adzuna.com/) and open an account
4.2. Go to [Adzuna admin access](https://developer.adzuna.com/admin/access_details) and locate App_id and API_key
4.3. Load them into your environment, replace "xxxxxxxx" with your credentials
On linux

```bash
export ADZUNA_APP_ID="xxxxxx" >> ~/.bashrc
export ADZUNA_API_KEY="xxxxxx" >> ~/.bashrc
```

On windows (I hope it works 🫠)

```bash
[System.Environment]::SetEnvironmentVariable("ADZUNA_APP_ID", "xxxxxx", "User")
[System.Environment]::SetEnvironmentVariable("ADZUNA_API_KEY", "xxxxxx", "User")

```

Copy the .env.example and rename it to .env

On linux

```bash
cp .env.example .env
```

On windows (I hope this works too)

```bash
copy .env.example .env
```

## Usage

### 1️⃣ Fetch Job Postings

Run the entry point script to fetch job postings and store them in the database:

```bash
python app.py
```

## Future Enhancements

🚀 Automate job updates using **Apache Airflow**  
🚀 Improve NLP accuracy using **BERT-based models**  
🚀 Integrate **LinkedIn API** for job recommendations  
🚀 Provide **online course suggestions** to fill skill gaps

## License

This project is licensed under the **MIT License**.

---

**Contributions Welcome!** Feel free to submit issues or pull requests. 🔥
