# dashboard.py

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Title
st.title("Threat Intelligence Dashboard")

# Connect to your SQLite database
conn = sqlite3.connect('threat_feeds.db')
df = pd.read_sql_query("SELECT * FROM Classified_threats", conn)

# Filters
st.sidebar.header("Apply Filters")
date_filter = st.sidebar.date_input("Filter by Date Range", [])
type_filter = st.sidebar.multiselect("Threat Type", df['threat_type'].dropna().unique())
actor_filter = st.sidebar.multiselect("Actor", df['actor'].dropna().unique())
severity_range = st.sidebar.slider("Severity Range", 0, 10, (0, 10))

# Apply filters
if date_filter:
    df = df[
        (pd.to_datetime(df['date']) >= pd.to_datetime(date_filter[0])) &
        (pd.to_datetime(df['date']) <= pd.to_datetime(date_filter[1]))
    ]
if type_filter:
    df = df[df['threat_type'].isin(type_filter)]
if actor_filter:
    df = df[df['actor'].isin(actor_filter)]
df = df[df['severity'].between(severity_range[0], severity_range[1])]

# IOC Frequency Chart
st.subheader("IOC Frequency")
ioc_counts = df['ioc_type'].value_counts().reset_index()
fig1 = px.bar(ioc_counts, x='index', y='ioc_type', labels={'index': 'IOC Type', 'ioc_type': 'Count'})
st.plotly_chart(fig1)

# Top Threat Categories
st.subheader("Top Threat Categories")
threat_counts = df['threat_type'].value_counts().reset_index()
fig2 = px.pie(threat_counts, names='index', values='threat_type', title="Threat Type Distribution")
st.plotly_chart(fig2)

# Source Reliability Scores
if 'reliability_score' in df.columns:
    st.subheader("Source Reliability Scores")
    fig3 = px.histogram(df, x='reliability_score', nbins=10)
    st.plotly_chart(fig3)

st.success("Dashboard Ready ✅")
