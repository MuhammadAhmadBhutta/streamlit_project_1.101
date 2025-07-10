# modules/forecast.py

import pandas as pd
from prophet import Prophet

def run_forecast(df: pd.DataFrame, periods: int):
    """
    Forecasts overall sales using Prophet.
    Groups sales by Order Date.
    """
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    daily_sales = df.groupby('Order Date')['Sales'].sum().reset_index()
    daily_sales = daily_sales.rename(columns={'Order Date': 'ds', 'Sales': 'y'})

    model = Prophet()
    model.fit(daily_sales)

    future = model.make_future_dataframe(periods=periods, freq='M')
    forecast = model.predict(future)

    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
