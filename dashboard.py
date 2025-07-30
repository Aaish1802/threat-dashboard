import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import os

# 🎯 Title
st.title("📊 Threat Intelligence Dashboard")

# 📂 Show current directory contents
st.write("📁 Files in current directory:", os.listdir())

# 🔌 Load Asset Inventory
asset_df = pd.read_csv("assets.csv")

# 🔌 Connect to SQLite DB
try:
    conn = sqlite3.connect("threat_feeds.db")
    query = "SELECT * FROM Classified_threats"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # 🎨 Add colored severity icons
    def severity_color(sev):
        color = {
            'Critical': '🔴',
            'High': '🟠',
            'Medium': '🟡',
            'Low': '🟢'
        }
        return f"{color.get(sev, '⚪')} {sev}"

    df['severity'] = df['severity'].apply(severity_color)

    # 🧠 Cross-reference with asset inventory
    merged_df = pd.merge(df, asset_df, left_on='ip_address', right_on='ip_address', how='left')

    # ⭐ Prioritize based on criticality
    critical_assets = merged_df[merged_df['criticality'] == 'High']

    # 📑 Show the full threat table
    st.subheader("📑 Full Threat Table")
    st.dataframe(merged_df)

    # 🔍 Sidebar filters
    st.sidebar.header("🔍 Filter Threats")
    selected_type = st.sidebar.multiselect("Select Threat Type", merged_df['threat_type'].unique())
    selected_severity = st.sidebar.multiselect("Select Severity", merged_df['severity'].unique())

    if selected_type:
        merged_df = merged_df[merged_df['threat_type'].isin(selected_type)]
    if selected_severity:
        merged_df = merged_df[merged_df['severity'].str.contains('|'.join(selected_severity))]

    # 📊 Bar Chart
    if 'threat_type' in merged_df.columns:
        fig1 = px.bar(merged_df, x='threat_type', color='severity', title='Threat Types by Severity Count')
        st.plotly_chart(fig1)

    # 🥧 Pie Chart
    if 'threat_type' in merged_df.columns:
        pie_data = merged_df['threat_type'].value_counts().reset_index()
        pie_data.columns = ['threat_type', 'count']
        fig2 = px.pie(pie_data, names='threat_type', values='count', title='Threat Type Distribution')
        st.plotly_chart(fig2)

    # 🛡️ High Criticality Asset Focus
    st.subheader("🛡️ Threats Targeting High-Criticality Assets")
    st.dataframe(critical_assets)

except Exception as e:
    st.error(f"❌ Error loading data: {e}")
