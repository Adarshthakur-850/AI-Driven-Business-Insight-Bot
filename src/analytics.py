import pandas as pd
from sqlalchemy import text
from src.database import get_db

class AnalyticsEngine:
    def __init__(self):
        pass
        
    def execute_query(self, sql_query):
        """
        Executes SQL query and returns result as DataFrame.
        """
        db = next(get_db())
        try:
            result = db.execute(text(sql_query))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            return df
        except Exception as e:
            print(f"Query Execution Error: {e}")
            return pd.DataFrame()
        finally:
            db.close()

    def compute_kpis(self, df):
        """
        Computes generic KPIs from the result DataFrame.
        """
        kpis = {}
        if df.empty:
            return kpis
            
        # Total numeric sum (likely revenue/quantity)
        numeric_cols = df.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            kpis[f"Total {col}"] = df[col].sum()
            kpis[f"Avg {col}"] = df[col].mean()
            
        # Row count
        kpis["Row Count"] = len(df)
        
        return kpis
