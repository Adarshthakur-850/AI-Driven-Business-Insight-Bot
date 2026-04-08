<<<<<<< HEAD
# AI-Driven Business Insight Bot

## Overview
This project is an intelligent business assistant that allows users to query sales, customer, and product data using natural language. It leverages a Text-to-SQL engine (powered by LLM or mock logic) and presents insights on a real-time web dashboard.

## Features
- **Natural Language Querying**: Ask "What are the top 5 products?" and get instant answers.
- **Dynamic Visualization**: Auto-generated Plotly charts based on query results.
- **Real-Time Data**: Connects to a SQL database (SQLite for demo).
- **FastAPI Backend**: Robust API handling NLP and Data processing.
- **Streamlit Dashboard**: User-friendly chat interface for executives.

## Project Structure
```
AI-Driven Business Insight Bot/
├── dashboard/
│   └── app.py              # Streamlit Frontend
├── src/
│   ├── api.py              # FastAPI Backend
│   ├── database.py         # DB Setup & Models
│   ├── nlp_engine.py       # Text-to-SQL Logic
│   ├── analytics.py        # Query Execution & KPIs
│   └── visualization.py    # Chart Generation
├── Dockerfile
├── requirements.txt
└── README.md
```

## Setup & Run

### 1. Local Installation
Prerequisite: Python 3.8+

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set OpenAI API Key (Optional, defaults to Mock mode if missing)
# export OPENAI_API_KEY="sk-..."  # Mac/Linux
# set OPENAI_API_KEY="sk-..."     # Windows

# 3. Initialize Database (First run only)
python src/database.py
```

### 2. Run the Application
You need to run the Backend and Frontend in separate terminals.

**Terminal 1: Backend API**
```bash
uvicorn src.api:app --reload
```
*API running at http://localhost:8000*

**Terminal 2: Dashboard**
```bash
streamlit run dashboard/app.py
```
*Dashboard running at http://localhost:8501*

### 3. Docker Deployment
```bash
docker build -t business-bot .
docker run -p 8000:8000 -p 8501:8501 business-bot
```
=======
# AI-Driven-Business-Insight-Bot
ml project
>>>>>>> ed75120a829df6c78e73da771cc18eef3a04f8b0
