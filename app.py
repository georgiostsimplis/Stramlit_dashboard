import yfinance as yf
import pandas as pd
import plotly.express as px
import streamlit as st
from financial_functions import calculate_cumulative_returns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from predict_fun import pre_fut
import numpy as np
import pytz

st.set_page_config(page_title="Stocks Dashboard", page_icon=":bar_chart:", layout="wide")

copenhagen_timezone = pytz.timezone('Europe/Copenhagen')

# Get the current date and time in the Copenhagen time zone
current_datetime_copenhagen = datetime.datetime.now(copenhagen_timezone)


# Create a sidebar for filters
with st.sidebar:
    st.title("Filters")
    
    stocks = ["NVDA", "MSFT", "AMZN", "GOOGL", "META"]
    selected_stocks = st.multiselect("Select Stocks", stocks, default=stocks)
    view = st.radio("Select View", ["Stock Prices", "Daily Returns", "Monthly Returns"])

    # Select a single stock for prediction
    selected_prediction_stock = st.selectbox("Select a Stock for Prediction", stocks, index=0)  # Set index to the default stock


st.title(":bar_chart: Financial Data Dashboard")
st.markdown("Created by [Georgios Tsimplis](https://www.linkedin.com/in/georgios-tsimplis)")
st.markdown(f"Last update: {current_datetime_copenhagen}, DK Timezone, (6 months data)")

data = yf.download(selected_stocks, period="6mo")
df = data.Close
df_ret = df.pct_change(1)
df_monthly_ret = df.resample('M').ffill().pct_change()

volatility = df_ret.std()*np.sqrt(252)
cumulative_returns = calculate_cumulative_returns(df)

if len(selected_stocks)>1:
    fig_cum = px.bar(x=cumulative_returns.index, y=cumulative_returns.values, labels={"x": "Stocks", "y": "Cumulative Returns (%)"},
                title="Cumulative Returns for Each Stock (6 months)",
                color_discrete_sequence=['green'])

    # Customize the layout (optional)
    fig_cum.update_layout(xaxis_title_font=dict(size=15), yaxis_title_font=dict(size=15),width =500, height =400)

if len(selected_stocks)>1:
    fig_vol = px.bar(x=volatility.index, y=volatility.values, labels={"x": "Stocks", "y": "Volatility"},
                title="Annualized Volatility for Each Stock",
                color_discrete_sequence=['orange'])

    # Customize the layout (optional)
    fig_vol.update_layout(xaxis_title_font=dict(size=15), yaxis_title_font=dict(size=15), width =600, height =400)

if len(selected_stocks)>1:
    fig_pr = px.line(df, x=df.index, y=df.columns, title='Stock Prices Over Time')
    fig_pr.update_xaxes(title_text='Date')
    fig_pr.update_yaxes(title_text='Price')
    fig_pr.update_layout(legend_title_text='Stocks', width =500, height =400)
else:
    fig_pr = px.line(df, x=df.index, y=df.values, title='Stock Prices Over Time')
    fig_pr.update_xaxes(title_text='Date')
    fig_pr.update_yaxes(title_text='Price')
    fig_pr.update_layout(legend_title_text='Stocks', width =500, height =400)


# Create a Plotly Line Chart for Returns
# fig = px.line(df_ret, x=df_ret.index, y=df_ret.columns, title='Stock Returns Over Time')
# fig.update_xaxes(title_text='Date')
# fig.update_yaxes(title_text='Returns')
# fig.update_layout(legend_title_text='Stocks',  width =500, height =400)

fig = make_subplots(rows=2, cols=3)

# Add scatter plots for each stock to the subplots

if len(selected_stocks)>1:
    for i, stock in enumerate(selected_stocks):
        row = (i // 3) + 1  # Determine the row based on the index
        col = (i % 3) + 1   # Determine the column based on the index
        
        # Add a scatter plot for the current stock to the subplot
        fig.add_trace(go.Scatter(x=df_ret.index, y=df_ret[stock], mode='lines', name=stock), row=row, col=col)

        # Update the layout of the subplot (customize as needed)
        fig.update_layout(title_text="Stock Returns Over Time", showlegend=True)

else:
    fig = px.line(x=df_ret.index, y=df_ret.values, labels={"x": "Date", "y": "Return"},
                title="Stock Returns Over Time",
                color_discrete_sequence=['green'])

    # Customize the layout (optional)
    fig.update_layout(xaxis_title_font=dict(size=15), yaxis_title_font=dict(size=15),width =500, height =400)


#######################################################
# Metrics calculation
diff_df = (data.Close - data.Open)/data.Open
diff_data =  diff_df.iloc[-1]
# diff_data_sorted.index[0] = diff_data.idxmax()
# max_value = max(diff_data)

# min_stock = diff_data.idxmin()
# min_value = min(diff_data)
if len(selected_stocks)>1:
    diff_data_sorted = diff_data.sort_values(ascending=False)
else:
    diff_data_sorted = diff_data


# st.markdown("## Metrics")
# col1, col2, col3, col4, col5 = st.columns(5)

# col1.metric("Today's best performance", diff_data_sorted.index[0], str(round(diff_data_sorted[0], 6)*100) + "%")
# col2.metric(" ", diff_data_sorted.index[1], str(round(diff_data_sorted[1], 6)*100) + "%")
# col3.metric(" ", diff_data_sorted.index[2], str(round(diff_data_sorted[2], 6)*100) + "%")
# col4.metric(" ", diff_data_sorted.index[3], str(round(diff_data_sorted[3], 6)*100) + "%")
# col5.metric("Today's worst performance",diff_data_sorted.index[4], str(round(diff_data_sorted[4], 6)*100) + "%")
# st.markdown("*Indicates the percentage change between the Open Price and the Close/Current Price")
# st.markdown("___")


number_of_stocks = len(selected_stocks)

st.markdown("## Metrics")
cols = st.columns(number_of_stocks)
if len(selected_stocks)>1:
    for j,each_stock in enumerate(selected_stocks):
        cols[j].metric("Today's performance", diff_data_sorted.index[j], "{:.4f}".format(round(float(diff_data_sorted[j]), 6)*100) + "%")
else:
    cols[0].metric("Today's performance", selected_stocks[0], "{:.4f}".format(round(float(diff_data_sorted), 6)*100) + "%")
st.markdown("*Indicates the percentage change between the Open Price and the Close/Current Price")
st.markdown("___")


left_column, middle_column, right_column = st.columns(3)

with left_column:
    if view == "Stock Prices":
        st.subheader("Stock Prices")
        if len(selected_stocks)>1:
            st.dataframe(df.sort_values(by='Date', ascending=False))
        else:
            st.dataframe(df.sort_values(ascending=False))
    elif view == "Daily Returns":
        st.subheader("Daily Returns")
        if len(selected_stocks)>1:
            st.dataframe(df_ret.sort_values(by='Date', ascending=False))
        else:
            st.dataframe(df_ret.sort_values(ascending=False))
    elif view == "Monthly Returns":
        st.subheader("Monthly Returns")
        if len(selected_stocks)>1:
            st.dataframe(df_monthly_ret.sort_values(by='Date', ascending=False))
        else:
            st.dataframe(df_monthly_ret.sort_values(ascending=False))
with middle_column:
    #st.subheader("Cumulative Return for each stock:")
    st.plotly_chart(fig_pr)
with right_column:
    #st.subheader("Volatility for each stock:")
    if len(selected_stocks)>1:
        st.plotly_chart(fig_cum)
    else:
        col_ = st.columns(1)
        col_[0].metric("Cumulative Return ", selected_stocks[0], cumulative_returns)

st.markdown('---')
left_column1,  right_column1 = st.columns(2)

with left_column1:
    #st.subheader("Average Rating:")
    if len(selected_stocks)>1:
        st.plotly_chart(fig_vol)
    else:
        col__ = st.columns(1)
        col__[0].metric("Annualized Volatility ", selected_stocks[0], volatility)
with right_column1:
    #st.subheader("Total Sales:")
    st.plotly_chart(fig)


st.plotly_chart(pre_fut(selected_prediction_stock))

