# library imports
import streamlit as st 
import pandas as pd 
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import datetime 
import yfinance as yf
from datetime import date , timedelta
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller


# Title of the app
app_name = 'Stock Market Forecasting App'

st.title(app_name)

st.subheader('This app is helping you to forecast stock prices using SARIMAX Model.')

# Add an image from online link
st.image("./image/img.jpg",width=1024)

# take input from the user of app about the start and end date

#sider
st.sidebar.header('Select Date Range')

start_date = st.sidebar.date_input('Start date', value=pd.to_datetime('2024-01-01'))
end_date = st.sidebar.date_input('End date', value=pd.to_datetime('2024-12-31'))

# add ticker symbol list 
ticker_list = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NFLX', 'NVDA', 'BRK.B','PYPL']

ticker = st.sidebar.selectbox('Select Ticker Symbol of Company', ticker_list)

# Download stock data
data = yf.download(ticker, start=start_date, end=end_date)

# Add Date column
data.insert(0, 'Date', data.index, True)
data.reset_index(drop=True, inplace=True)

# 🔥 Flatten MultiIndex columns to strings like "Close"
if isinstance(data.columns, pd.MultiIndex):
    data.columns = [col[0] for col in data.columns]



st.write(f"Data for {ticker} from {start_date} to {end_date}")
st.write(data)

# show clean column names
st.write("📌 Column Names in Data:")
st.write(data.columns.tolist())



data.columns = data.columns.get_level_values(0)  # or data.columns = data.columns.droplevel(1)

# plot the data using plotly
st.header("📊 Data Visualization")
st.subheader("Select columns to visualize")

st.write("**Note:** Select one or more columns (e.g., Close, Adj Close, Volume) from the sidebar.")

# Add multiselect in sidebar
available_columns = ['Open', 'High', 'Low', 'Close','Volume']
selected_columns = st.sidebar.multiselect("Choose columns to visualize", options=available_columns, default=['Close'])

if selected_columns:
    fig = go.Figure()
    for col in selected_columns:
        fig.add_trace(go.Scatter(x=data['Date'], y=data[col], mode='lines', name=col))
    
    fig.update_layout(
        title=f"{ticker} Stock Data - {', '.join(selected_columns)}",
        xaxis_title="Date",
        yaxis_title="Value",
        width=1000,
        height=600
    )
    st.plotly_chart(fig)
else:
    st.warning("Please select at least one column to visualize.")

# add a select box to select column from the data

column = st.selectbox('Select the column to be used for forecasting', data.columns[1:])

# subsetting the data 
data = data[['Date', column]]

st.write("selected Data")
st.write(data)

# ADF test check Stationary 
st.header('Is data Stationary?')
st.write('**Note:** if p-value is less than 0.05, then data is stationary.')
st.write(adfuller(data[column])[1]<0.05) 

# lets Decompose the data
st.header('Decomposition of the data')
decomposition = seasonal_decompose(data[column], model='additive', period=12)
st.write(decomposition.plot())      

# make same plot using plotly
st.write('Decomposition of the data using Plotly')
st.plotly_chart(px.line(x=data["Date"],y=decomposition.trend, title='Trend Component',width=1000,height=400, labels={'x': 'Date', 'y': 'Price'}).update_traces(line_color='blue'))
st.plotly_chart(px.line(x=data["Date"],y=decomposition.seasonal, title='Seasonal Component',width=1000,height=400, labels={'x': 'Date', 'y': 'Price'}).update_traces(line_color='orange'))
st.plotly_chart(px.line(x=data["Date"],y=decomposition.resid, title='Residual Component',width=1000,height=400, labels={'x': 'Date', 'y': 'Price'}).update_traces(line_color='green'))

# let's run tha model
# user input for three parameters of the model and seasonal order
p = st.slider('Select the value of p',0,5,2)
d = st.slider('Select the value of q',0,5,1)
q = st.slider('Select the value of d',0,5,2)
seasonal_order = st.number_input('Select the value of seasonal p',0,24,12) 

# train the model 
model = sm.tsa.statespace.SARIMAX(data[column], order=(p,d,q), seasonal_order=(p,d,q,seasonal_order))
model = model.fit()

# print the summary of the model
st.header('Model Summary')
st.write(model.summary())
st.write("---")


# predict the future values (Forecasting)

forecast_period = st.number_input('Select the number of days to forecast', 1,365,10)

# predict the future values
predictions = model.get_prediction(start=len(data), end=len(data)+forecast_period)
predictions = predictions.predicted_mean

# add index to results dataframe as dates 
predictions.index = pd.date_range(start=end_date, periods=len(predictions), freq='D')
predictions = pd.DataFrame(predictions)
predictions.insert(0, 'Date', predictions.index)
predictions.reset_index(drop=True, inplace=True)
st.write("## Predictions", predictions)
st.write("## Actual Data",data)

# let's plot the predictions and actual data using plotly
fig = go.Figure()
# add actual data to the plot 
fig.add_trace(go.Scatter(x=data['Date'], y=data[column], mode='lines', name='Actual Data',line=dict(color='blue')))
# add predictions to the plot
fig.add_trace(go.Scatter(x=predictions['Date'], y=predictions["predicted_mean"], mode='lines', name='Predictions',line=dict(color='red')))
# set the title and axis labels
fig.update_layout(
    title=f"{ticker} Stock Price Predictions",
    xaxis_title="Date",
    yaxis_title="Price",
    width=1000,
    height=600
)

# show the plot
st.plotly_chart(fig)

# Add buttons to show and hide separate plots 
show_plots = False
if st.button('Show/Hide Separate Plots'):
    if not show_plots:
        st.write(px.line(data, x='Date', y=column, title=f"{ticker} Stock Price", width=1000, height=400, labels={'x': 'Date', 'y': 'Price'}).update_traces(line_color='blue'))
        st.write(px.line(predictions, x='Date', y='predicted_mean', title=f"{ticker} Stock Price Predictions", width=1000, height=400, labels={'x': 'Date', 'y': 'Price'}).update_traces(line_color='red'))
        show_plots = True
    else:
        st.write("Separate plots are hidden.")
        show_plots = False
# add hide plots button
hide_plots = False
if st.button('Hide Separate Plots'):
    if not hide_plots:
        hide_plots = True
    else:
        hide_plots = False

st.write("---")
