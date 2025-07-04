import streamlit as st 
import pandas as pd
import plotly.express as px

# import dataset 
st.title("Plotly Dashboard App")
df = px.data.gapminder()
st.write(df)
# st.write(df.head())
# columns names
st.subheader("📌 Column Names in Data:")
st.write(df.columns)

# summary statistics
st.subheader("Summary Statistics of the Data")
st.write(df.describe())


# data management
year_options = df['year'].unique().tolist()

year = st.selectbox("which year you want to plot?", year_options)

# df=df[df['year'] == year]

# plot the data
fig = px.scatter(df, x='gdpPercap', y='lifeExp', size='pop', 
                # color='country',
                color='continent',
                log_x=True, size_max=60,range_x=[100, 100000],range_y=[20, 90],
                animation_frame='year',
                animation_group='country')
fig.update_layout(width=800,height=400)
st.plotly_chart(fig)
