import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Title
st.title("Threat Intelligence Dashboard")

# Connect to the SQLite DB
conn = sqlite3.connect("threat_feeds.db")
cursor = conn.cursor()

# Query
query = "SELECT * FROM Classified_threats"
cursor.execute(query)
data = cursor.fetchall()

# Get column names
columns = [description[0] for description in cursor.description]

# Convert to DataFrame
df = pd.DataFrame(data, columns=columns)

# Show data table
st.subheader("Threat Data")
st.dataframe(df)

# Optional: Visualize top threat types
if 'threat_type' in df.columns:
    fig = px.bar(df['threat_type'].value_counts().reset_index(), 
                 x='index', y='threat_type', 
                 labels={'index': 'Threat Type', 'threat_type': 'Count'},
                 title='Top Threat Types')
    st.plotly_chart(fig)
