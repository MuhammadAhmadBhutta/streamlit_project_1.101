import streamlit as st
import pandas as pd
import plotly.express as px

# Load some example data
df = px.data.gapminder().query("year == 2007")

st.title("🌍 Global Data Dashboard")

# Sidebar filter
continent = st.sidebar.selectbox("Continent", df['continent'].unique())

filtered_df = df[df['continent'] == continent]

# KPI
avg_gdp = filtered_df['gdpPercap'].mean()
st.metric("Average GDP per Capita", f"${avg_gdp:,.0f}")

# Charts
fig1 = px.scatter(
    filtered_df, x="gdpPercap", y="lifeExp",
    size="pop", color="country",
    hover_name="country", log_x=True, size_max=60,
    title="GDP vs Life Expectancy"
)

fig2 = px.bar(
    filtered_df, x="country", y="pop",
    title="Population by Country"
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)
h