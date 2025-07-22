import streamlit as st
import pandas as pd
import sqlite3
import os

st.title("Threat Intelligence Dashboard")

# Optional Debug Check (shows files in the current directory)
st.write("Files in current directory:", os.listdir())

# Check if DB file exists before connecting
db_file = "threat_feeds.db"

if not os.path.exists(db_file):
    st.error(f"Database file '{db_file}' not found in current directory!")
else:
    try:
        # Connect to database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Check available tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        st.write("Tables found:", tables)

        # Make sure table exists before querying
        if ('Classified_threats',) in tables:
            query = "SELECT * FROM Classified_threats"
            df = pd.read_sql_query(query, conn)

            if df.empty:
                st.warning("The table 'Classified_threats' is empty.")
            else:
                st.success("Data loaded successfully!")
                st.dataframe(df)

                # Optional: Filter by severity
                severity_filter = st.selectbox("Filter by severity", ["All"] + sorted(df["severity"].unique()))
                if sever
