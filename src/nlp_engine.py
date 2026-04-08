import os
import openai
import re

class NLPEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
        
    def generate_sql(self, question):
        """
        Converts a natural language question into a SQL query.
        """
        if not self.api_key:
            return self._mock_sql_generation(question)

        prompt = f"""
        You are an expert SQL Data Analyst.
        Database Schema:
        - customers(customer_id, name, country, segment)
        - products(product_id, name, category, price)
        - orders(order_id, date, customer_id, product_id, quantity, total_amount)
        
        Question: {question}
        
        Return ONLY the SQL query. Do not wrap in markdown blocks.
        """
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            sql = response.choices[0].message.content.strip()
            # Clean up potential markdown formatting
            sql = re.sub(r"```sql|```", "", sql, flags=re.IGNORECASE).strip()
            return sql
        except Exception as e:
            print(f"LLM Error: {e}. Falling back to mock.")
            return self._mock_sql_generation(question)

    def _mock_sql_generation(self, question):
        """
        Simple keyword-based mock SQL generation for demo purposes without API key.
        """
        question = question.lower()
        
        if "sales" in question or "revenue" in question:
            if "country" in question:
                return """
                SELECT c.country, SUM(o.total_amount) as revenue
                FROM orders o
                JOIN customers c ON o.customer_id = c.customer_id
                GROUP BY c.country
                ORDER BY revenue DESC
                """
            elif "product" in question:
                 return """
                SELECT p.name, SUM(o.total_amount) as revenue
                FROM orders o
                JOIN products p ON o.product_id = p.product_id
                GROUP BY p.name
                ORDER BY revenue DESC
                LIMIT 10
                """
            elif "time" in question or "month" in question or "date" in question:
                return """
                SELECT o.date, SUM(o.total_amount) as revenue
                FROM orders o
                GROUP BY o.date
                ORDER BY o.date
                """
            else:
                return "SELECT SUM(total_amount) as total_revenue FROM orders"
                
        elif "count" in question or "how many" in question:
            if "customer" in question:
                return "SELECT COUNT(*) as customer_count FROM customers"
            if "order" in question:
                return "SELECT COUNT(*) as order_count FROM orders"
        
        # Default fallback
        return "SELECT * FROM orders LIMIT 5"
