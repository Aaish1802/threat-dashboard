import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Threat Intelligence Dashboard", layout="wide")

st.title("🔍 Threat Intelligence Dashboard")

# Connect to the local SQLite database
conn = sqlite3.connect("threat_feeds.db")
cursor = conn.cursor()

# Check if the table exists
try:
    cursor.execute("SELECT * FROM Classified_threats")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=columns)
except Exception as e:
    st.error(f"Error accessing database: {e}")
    st.stop()

# Filters
with st.sidebar:
    st.header("🔎 Filters")
    threat_types = df['Type'].unique()
    selected_types = st.multiselect("Filter by Type", threat_types, default=threat_types)

    severities = df['Severity'].unique()
    selected_severities = st.multiselect("Filter by Severity", severities, default=severities)

# Apply filters
filtered_df = df[
    (df['Type'].isin(selected_types)) &
    (df['Severity'].isin(selected_severities))
]

# Display filtered data
st.subheader("📋 Filtered Threat Intelligence Feed")
st.dataframe(filtered_df, use_container_width=True)

# Charts
st.subheader("📊 Threats by Type")
threat_counts = filtered_
