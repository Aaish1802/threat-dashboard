import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os

st.title("📊 Threat Intelligence Dashboard")

# Optional: List files in current directory for debug
st.write("📁 Files in current directory:", os.listdir())

try:
    # Connect to the database
    conn = sqlite3.connect("threat_feeds.db")
    cursor = conn.cursor()

    # Execute SQL query
    query = "SELECT * FROM Classified_threats"
    cursor.execute(query)
    data = cursor.fetchall()

    # Get column names
    columns = [description[0] for description in cursor.description]

    # Create DataFrame
    df = pd.DataFrame(data, columns=columns)

    # Display table
    st.subheader("📄 Threat Table")
    st.dataframe(df)

    # Optional Chart
    if 'threat_type' in df.columns:
        fig = px.histogram(df, x='threat_type', title='Threats by Type')
        st.plotly_chart(fig)
    else:
        st.warning("⚠️ 'threat_type' column not found. Skipping chart.")

except Exception as e:
    st.error(f"❌ Error loading data: {e}")
