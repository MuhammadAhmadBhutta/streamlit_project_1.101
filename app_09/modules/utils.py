# modules/utils.py

import plotly.graph_objects as go
import pandas as pd

def plot_forecast(forecast_df: pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=forecast_df['ds'],
        y=forecast_df['yhat'],
        mode='lines',
        name='Forecast'
    ))

    fig.add_trace(go.Scatter(
        x=forecast_df['ds'],
        y=forecast_df['yhat_upper'],
        mode='lines',
        name='Upper Bound',
        line=dict(dash='dash')
    ))

    fig.add_trace(go.Scatter(
        x=forecast_df['ds'],
        y=forecast_df['yhat_lower'],
        mode='lines',
        name='Lower Bound',
        line=dict(dash='dash')
    ))

    fig.update_layout(title="Sales Forecast", xaxis_title="Date", yaxis_title="Sales ($)")
    return fig
