# streamlit_power_bi_sidebar.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Streamlit Power BI-like Dashboard",
                   layout="wide")

st.title("📊 Power BI-like Dashboard in Streamlit")

# Sidebar - Controls
with st.sidebar:
    st.header("⚙️ Controls")
    uploaded_file = st.file_uploader("Upload your dataset (CSV or Excel)", type=['csv', 'xlsx'])

    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

        st.subheader("📌 KPI Metrics")
        kpi_cols = st.multiselect("Select numeric columns for KPI cards:", numeric_cols)

        st.subheader("📊 Chart Settings")
        chart_type = st.selectbox("Chart Type:", ["Bar", "Line", "Pie", "Scatter"])
        x_axis = st.selectbox("X-axis:", df.columns)
        y_axis = st.selectbox("Y-axis:", numeric_cols)
        color = st.selectbox("Group by (optional):", [None] + categorical_cols)

        generate_chart = st.button("Generate Chart")
    else:
        df = None

# Main canvas - Dashboard
if df is not None:
    st.subheader("🗂️ Data Preview")
    st.dataframe(df, use_container_width=True)

    # KPI Cards
    st.subheader("📌 KPI Metrics")
    if kpi_cols:
        cols = st.columns(len(kpi_cols))
        for idx, col in enumerate(kpi_cols):
            value = df[col].sum()
            cols[idx].metric(label=col, value=f"{value:,.2f}")
    else:
        st.info("👉 Please select at least one column for KPI cards in the sidebar.")

    st.markdown("---")

    # Chart
    if generate_chart:
        st.subheader(f"📊 {chart_type} Chart")
        fig = None

        if chart_type == "Bar":
            fig = px.bar(df, x=x_axis, y=y_axis, color=color)
        elif chart_type == "Line":
            fig = px.line(df, x=x_axis, y=y_axis, color=color)
        elif chart_type == "Pie":
            fig = px.pie(df, names=x_axis, values=y_axis)
        elif chart_type == "Scatter":
            fig = px.scatter(df, x=x_axis, y=y_axis, color=color)

        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👈 Upload a file and configure your dashboard in the sidebar.")
