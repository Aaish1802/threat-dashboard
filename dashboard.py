import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import os

# 🎯 Title
st.title("📊 Threat Intelligence Dashboard")

# 📂 Show current directory contents
st.write("📁 Files in current directory:", os.listdir())

# 🔌 Connect to SQLite DB and load threats
try:
    conn = sqlite3.connect("threat_feeds.db")
    df = pd.read_sql_query("SELECT * FROM Classified_threats", conn)
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

    # 🧾 Show Threat Table
    st.subheader("📑 Threat Table")
    st.dataframe(df)

    # 🔍 Sidebar Filters
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

    # 🧠 Load Asset Inventory
    if os.path.exists("assets.csv"):
        asset_df = pd.read_csv("assets.csv")

        # ✅ Check if ip_address column exists in both dataframes
        if 'ip_address' in df.columns and 'ip_address' in asset_df.columns:
            merged_df = pd.merge(df, asset_df, on='ip_address', how='left')

            # 💡 Show prioritized threats (High critical assets)
            st.subheader("🚨 Prioritized Threats on High-Criticality Assets")
            high_impact = merged_df[merged_df['criticality'] == 'High']
            st.dataframe(high_impact[['threat_name', 'ip_address', 'role', 'criticality']])
        else:
            st.warning("⚠️ 'ip_address' column missing in either threat data or asset inventory.")
    else:
        st.warning("⚠️ 'assets.csv' not found for asset context.")

except Exception as e:
    st.error(f"❌ Error loading data: {e}")
