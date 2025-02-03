# Dynamic Skill Gap Analyzer

## Overview

The **Dynamic Skill Gap Analyzer** is a data engineering project that extracts required skills using **Natural Language Processing (NLP)**, and compares them to a user's resume. The goal is to identify skill gaps and provide recommendations for career improvement.

## Features

NB: **The project is still in development and not all features are implemented yet**    
✅ Extract required job skills using **NLP (spaCy)**  
✅ Parse and analyze a user's resume for existing skills  
✅ Store skill data in **PostgreSQL** for historical analysis  
❌ Identify missing skills for career improvement  
❌ Create a dashboard for better visualizations


## Tech Stack

- **Python** (Data Processing & NLP)
- **spaCy** (Skill Extraction)
- **PostgreSQL** (Database Storage)

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL

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
⚠️ **NB**: Make sure you have docker, docker desktop installed and running on your system.  

   ```bash
   docker-compose up -d
   ```

## Usage

Run the entry point script:

```bash
python3 main.py
```

or 
```bash
python main.py
```

## Future Enhancements
🚀 Provide **online course suggestions** to fill skill gaps  
🚀 Fetch jobs and related skills from external sources

**Contributions Welcome!** Feel free to submit issues or pull requests. 🔥
