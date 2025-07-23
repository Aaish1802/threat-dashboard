import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os

# Set page config
st.set_page_config(page_title="Threat Intelligence Dashboard", layout="wide")

# App title
st.markdown("# 🧠 Threat Intelligence Dashboard")
st.markdown("An interactive dashboard to visualize classified threat feeds from the threat intelligence database.")

# Debug: Show files in directory
st.markdown("📁 **Files in current directory:**")
st.json(os.listdir())

# Load the SQLite database
try:
    conn = sqlite3.connect("threat_feeds.db")
    cursor = conn.cursor()

    # Query all data
    query = "SELECT * FROM Classified_threats"
    cursor.execute(query)
    data = cursor.fetchall()

    # Get column names
    columns = [description[0] for description in cursor.description]

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=columns)

    # Success message
    st.success("✅ Successfully loaded threat data from the database.")

    # Display table
    st.subheader("📊 Threat Table")
    st.dataframe(df, use_container_width=True)

    # Optional filter by threat type
    if 'threat_type' in df.columns:
        st.subheader("🔍 Filter Threats by Type")
        selected_type = st.selectbox("Choose Threat Type", df['threat_type'].unique())
        filtered_df = df[df['threat_type'] == selected_type]

        # Display filtered table
        st.dataframe(filtered_df, use_container_width=True)

        # Chart
        st.subheader("📈 Threat Severity Distribution")
        fig = px.histogram(filtered_df, x="threat_name", color="severity", barmode="group",
                           title=f"Threats under '{selected_type}'", labels={"threat_name": "Threat"})
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("⚠️ 'threat_type' column not found. Skipping chart.")

except Exception as e:
    st.error(f"❌ Error loading data: {e}")
