from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import yfinance as yf
import pandas as pd

def pre_fut(name):
    stocks = ["NVDA", "MSFT", "AMZN", "GOOGL", "META"]
    data = yf.download(stocks, period="2y")
    df = data.Close
    a = pd.DataFrame({'ds':df.index, 'y':df[name]}).reset_index().drop(columns = 'Date')
    model = Prophet(changepoint_prior_scale=0.3, daily_seasonality=False)
    model.add_seasonality(name='weekly', period=5, fourier_order= 3)
    model.add_seasonality(name='monthly', period=21, fourier_order= 5)
    model.add_seasonality(name='quartely', period=62, fourier_order=20 )
    model.add_seasonality(name='yearly', period=252, fourier_order= 25)
    model.fit(a)
    future = model.make_future_dataframe(30, freq='D')
    forecast = model.predict(future)
    fig = plot_plotly(model, forecast)
    fig.update_traces(
    line=dict(color='red'),  # Change the line color
    marker=dict(color='green'),  # Change the marker color
)
    fig.update_layout(
        title='One month prediction - {}'.format(name),
        xaxis_title='Date',
        yaxis_title='Price',
        #template='plotly_dark'  # You can change the template to a different theme
    )
    
    return fig

