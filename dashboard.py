import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os

# Debug: list files to confirm if the database is available
st.write("📁 Files in current directory:", os.listdir())

# Connect to the SQLite database
try:
    conn = sqlite3.connect("threat_feeds.db")
    cursor = conn.cursor()

    # Execute SQL query
    query = "SELECT * FROM Classified_threats"
    cursor.execute(query)
    data = cursor.fetchall()

    # Get column names
    columns = [description[0] for description in cursor.description]

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=columns)

    # Display title and table
    st.title("🔐 Threat Intelligence Dashboard")
    st.dataframe(df)

    # Optional: Display a chart (you can customize this)
    if 'threat_type' in df.columns:
        fig = px.histogram(df, x='threat_type', title='Threat Distribution by Type')
        st.plotly_chart(fig)
    else:
        st.warning("⚠️ 'threat_type' column not found in your data. Chart not generated.")

except Exception as e:
    st.error(f"❌ Error loading data: {e}")
