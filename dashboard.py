import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import os

# 🎯 Title
st.title("📊 Threat Intelligence Dashboard")

# 📂 Show current directory contents
st.write("📁 Files in current directory:", os.listdir())

# 🔌 Connect to SQLite DB
try:
    conn = sqlite3.connect("threat_feeds_updated.db")
    query = "SELECT * FROM Classified_threats"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # 🎨 Add colored badges for severity
    def severity_color(sev):
        color = {
            'Critical': '🔴',
            'High': '🟠',
            'Medium': '🟡',
            'Low': '🟢'
        }
        return f"{color.get(sev, '⚪')} {sev}"

    df['severity'] = df['severity'].apply(severity_color)

    # 🧾 Show the table
    st.subheader("📑 Threat Table")
    st.dataframe(df)

    # 🔍 Add Sidebar Filters
    st.sidebar.header("🔍 Filter Threats")
    selected_type = st.sidebar.multiselect("Select Threat Type", df['threat_type'].unique())
    selected_severity = st.sidebar.multiselect("Select Severity", df['severity'].unique())

    if selected_type:
        df = df[df['threat_type'].isin(selected_type)]
    if selected_severity:
        df = df[df['severity'].str.contains('|'.join(selected_severity))]

    # 📊 Bar Chart
    if 'threat_type' in df.columns:
        fig1 = px.bar(df, x='threat_type', color='severity', title='Threat Types by Severity Count')
        st.plotly_chart(fig1)

    # 🥧 Pie Chart
    if 'threat_type' in df.columns:
        pie_data = df['threat_type'].value_counts().reset_index()
        pie_data.columns = ['threat_type', 'count']
        fig2 = px.pie(pie_data, names='threat_type', values='count', title='Threat Type Distribution')
        st.plotly_chart(fig2)

except Exception as e:
    st.error(f"❌ Error loading data: {e}")
