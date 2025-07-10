# app.py

import streamlit as st
import pandas as pd

from modules.opportunity import detect_opportunities
from modules.forecast import run_forecast
from modules.generator import generate_action_plan
from modules.utils import plot_forecast

st.set_page_config(page_title="📈 Superstore Opportunity Scanner", layout="wide")

st.title("🚀 Dynamic Business Opportunity Scanner & Action Planner")

# Upload or use default
uploaded_file = st.file_uploader("📂 Upload your business data (.xlsx)", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.success("✅ Data uploaded successfully!")
else:
    df = pd.read_excel("data/Sample_Superstore.xlsx")
    st.info("📄 Using built-in Superstore dataset.")

# Drop unwanted columns if they exist
df = df.drop(columns=[col for col in df.columns if col.strip() in ["A`"]], errors='ignore')

st.write("🔍 Preview:", df.head())

# Detect Opportunities
if st.button("🔍 Scan for Opportunities"):
    opportunities = detect_opportunities(df)
    st.subheader("📈 Potential Opportunities")
    st.write(opportunities)

# Run Forecast
st.subheader("📊 Revenue Forecast Simulator")
periods = st.slider("Select forecast horizon (months)", 1, 24, 6)
forecast_df = run_forecast(df, periods)

fig = plot_forecast(forecast_df)
st.plotly_chart(fig, use_container_width=True)

# Generate Action Plan with Gemini
if st.button("🤖 Generate AI-Powered Action Plan"):
    if 'opportunities' not in locals():
        opportunities = detect_opportunities(df)
    plan = generate_action_plan(opportunities)
    st.subheader("✅ Recommended Action Plan")
    st.write(plan)

    st.download_button("📥 Download Action Plan", plan, file_name="action_plan.txt")

st.caption("💡 Powered by Streamlit + Google Gemini + Prophet")
