import pandas as pd##slack executed
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime
import requests

# Slack Configuration
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("supply_chain_alerts_large.csv")

data = load_data()

# Streamlit Dashboard
st.title("Real-Time Supply Chain Dashboard")
st.sidebar.header("Filter Options")

# Filters
month_filter = st.sidebar.multiselect("Select Month", data['Month'].unique(), default=data['Month'].unique())
filtered_data = data[data['Month'].isin(month_filter)]

# Visualizations
st.subheader("Inventory Utilization Trends")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=filtered_data, x="Month", y="Utilization", hue="Action", ax=ax)
ax.set_title("Monthly Inventory Utilization by Action")
ax.set_ylabel("Utilization (%)")
st.pyplot(fig)

st.subheader("Risk Distribution")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data=filtered_data, x="Risk Score", hue="Action", kde=True, bins=20, ax=ax)
ax.set_title("Risk Score Distribution")
ax.set_xlabel("Risk Score")
st.pyplot(fig)

st.subheader("Raw Data")
st.dataframe(filtered_data)
