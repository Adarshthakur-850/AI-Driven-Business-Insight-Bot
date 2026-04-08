import plotly.express as px
import pandas as pd

class VisualizationEngine:
    def generate_chart(self, df):
        """
        Auto-detects the best chart type for the data.
        """
        if df.empty:
            return None
            
        columns = df.columns.tolist()
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        cat_cols = df.select_dtypes(include=['object', 'string']).columns.tolist()
        date_cols = df.select_dtypes(include=['datetime', 'datetimetz']).columns.tolist()
        
        # Check if date string
        if not date_cols:
             # Create a copy to iterate safely
             for col in list(cat_cols):
                 if 'date' in col.lower() or 'time' in col.lower():
                     try:
                         df[col] = pd.to_datetime(df[col])
                         date_cols.append(col)
                         if col in cat_cols:
                             cat_cols.remove(col)
                     except:
                         pass

        # Time Series
        if date_cols and num_cols:
            return px.line(df, x=date_cols[0], y=num_cols[0], title="Trend Over Time")
            
        # Bar Chart (Categorical vs Numeric)
        if cat_cols and num_cols:
            # If too many categories, limit top 10
            if len(df) > 15:
                df = df.nlargest(10, num_cols[0])
            return px.bar(df, x=cat_cols[0], y=num_cols[0], title=f"{num_cols[0]} by {cat_cols[0]}")
            
        # Scatter (Numeric vs Numeric)
        if len(num_cols) >= 2:
            return px.scatter(df, x=num_cols[0], y=num_cols[1], title=f"{num_cols[0]} vs {num_cols[1]}")
            
        # Table (Fallback)
        return None
