import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from src.visualization import VisualizationEngine

# Config
API_URL = "http://localhost:8000/ask"
viz_engine = VisualizationEngine()

st.set_page_config(page_title="AI Business Bot", layout="wide")

st.title("🤖 AI-Driven Business Insight Bot")
st.markdown("Ask questions about your sales, customers, and products in plain English.")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "chart" in msg:
            st.plotly_chart(msg["chart"], use_container_width=True)
        if "sql" in msg:
            with st.expander("View SQL"):
                st.code(msg["sql"], language="sql")

# Input
if prompt := st.chat_input("Ask a question (e.g., 'Show total sales by country')"):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                response = requests.post(API_URL, json={"question": prompt})
                if response.status_code == 200:
                    resp_data = response.json()
                    data = pd.DataFrame(resp_data.get("data", []))
                    sql = resp_data.get("sql", "")
                    kpis = resp_data.get("kpis", {})
                    
                    # KPIs
                    if kpis:
                        keys = list(kpis.keys())
                        num_kpis = len(keys)
                        # Create rows of 3 columns
                        for i in range(0, num_kpis, 3):
                            cols = st.columns(3)
                            for j in range(3):
                                if i + j < num_kpis:
                                    key = keys[i+j]
                                    val = kpis[key]
                                    if isinstance(val, (int, float)):
                                        cols[j].metric(label=key, value=f"{val:,.2f}")
                                    else:
                                        cols[j].metric(label=key, value=str(val))
                    
                    # Chart
                    chart = None
                    if not data.empty:
                        chart = viz_engine.generate_chart(data)
                        if chart:
                            st.plotly_chart(chart, use_container_width=True)
                        else:
                            st.dataframe(data)
                    else:
                        st.write("No data found for this query.")

                    # Save to history
                    msg_payload = {"role": "assistant", "content": "Here is the insight based on your query.", "sql": sql}
                    if chart:
                         msg_payload["chart"] = chart
                    st.session_state.messages.append(msg_payload)
                    
                    with st.expander("View SQL Query"):
                        st.code(sql, language="sql")
                        
                else:
                    st.error("Error communicating with API.")
            except Exception as e:
                st.error(f"Connection Error: {e}")
