import pandas as pd

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.nlp_engine import NLPEngine
from src.analytics import AnalyticsEngine
from src.database import init_db, generate_sample_data
import os

app = FastAPI(title="Business Insight Bot API")

# Initialize engines
nlp = NLPEngine()
analytics = AnalyticsEngine()

# Ensure DB is ready on startup
@app.on_event("startup")
def startup_event():
    init_db()
    generate_sample_data()

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "AI Business Bot API is running"}

@app.post("/ask")
def ask_question(request: QueryRequest):
    question = request.question
    print(f"Received question: {question}")
    
    # 1. NLP -> SQL
    sql_query = nlp.generate_sql(question)
    print(f"Generated SQL: {sql_query}")
    
    if "SELECT" not in sql_query.upper():
        return {
            "answer": "Sorry, I couldn't generate a valid query for that.",
            "sql": sql_query,
            "data": [],
            "kpis": {}
        }
        
    # 2. Execute SQL
    df = analytics.execute_query(sql_query)
    
    # 3. Compute Insights
    kpis = analytics.compute_kpis(df)
    
    # Handle NaN values for JSON compatibility
    df = df.where(pd.notnull(df), None)
    
    # Convert DF to dict for JSON response
    data = df.to_dict(orient="records")
    
    return {
        "question": question,
        "sql": sql_query,
        "data": data,
        "kpis": kpis,
        "columns": df.columns.tolist() if not df.empty else []
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
