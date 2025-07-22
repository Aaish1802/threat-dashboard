import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Threat Intelligence Dashboard", layout="wide")

# Debug: list files to confirm the database is available
st.write("📂 Files in current directory:", os.listdir())

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
    st.title("📊 Threat Intelligence Dashboard")
    st.dataframe(df)

    # Optional chart
    if 'threat_type' in df.columns:
        fig = px.histogram(df, x='threat_type', title='Threat Distribution by Type')
        st.plotly_chart(fig)
    else:
        s
