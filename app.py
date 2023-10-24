
import yfinance as yf
import pandas as pd
import plotly.express as px
import streamlit as st
from financial_functions import calculate_cumulative_returns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
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

st.title(":bar_chart: Financial Data Dashboard")
st.markdown("Created by [Georgios Tsimplis](https://www.linkedin.com/in/georgios-tsimplis)")
st.markdown(f"Last update: {current_datetime_copenhagen}, DK Timezone, (3 months data)")

data = yf.download(selected_stocks, period="3mo")
df = data.Close
df_ret = df.pct_change(1)
df_monthly_ret = df.resample('M').ffill().pct_change()

volatility = df_ret.std()
cumulative_returns = calculate_cumulative_returns(df)

fig_cum = px.bar(x=cumulative_returns.index, y=cumulative_returns.values, labels={"x": "Stocks", "y": "Cumulative Returns (%)"},
             title="Cumulative Returns for Each Stock (3 months)",
             color_discrete_sequence=['green'])

# Customize the layout (optional)
fig_cum.update_layout(xaxis_title_font=dict(size=15), yaxis_title_font=dict(size=15),width =350, height =400)

fig_vol = px.bar(x=volatility.index, y=volatility.values, labels={"x": "Stocks", "y": "Volatility"},
             title="Volatility for Each Stock  (3 months)",
             color_discrete_sequence=['orange'])

# Customize the layout (optional)
fig_vol.update_layout(xaxis_title_font=dict(size=15), yaxis_title_font=dict(size=15), width =350, height =400)

fig_pr = px.line(df, x=df.index, y=df.columns, title='Stock Prices Over Time')
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
for i, stock in enumerate(selected_stocks):
    row = (i // 3) + 1  # Determine the row based on the index
    col = (i % 3) + 1   # Determine the column based on the index
    
    # Add a scatter plot for the current stock to the subplot
    fig.add_trace(go.Scatter(x=df_ret.index, y=df_ret[stock], mode='lines', name=stock), row=row, col=col)

# Update the layout of the subplot (customize as needed)
fig.update_layout(title_text="Stock Returns Over Time", showlegend=True)
#######################################################
# Metrics calculation
diff_df = (data.Close - data.Open)/data.Close
diff_data =  diff_df.iloc[-1]
max_stock = diff_data.idxmax()
max_value = max(diff_data)

min_stock = diff_data.idxmin()
min_value = min(diff_data)



st.markdown("## Metrics")
col1, col2 = st.columns(2)

col1.metric("Today's best performance", max_stock, str(round(max_value, 6)*100) + "%")
col2.metric("Today's worst performance", min_stock, str(round(min_value, 6)*100) + "%")
st.markdown("___")


left_column, middle_column, right_column = st.columns(3)

with left_column:
    if view == "Stock Prices":
        st.subheader("Stock Prices")
        st.dataframe(df.sort_values(by='Date', ascending=False))
    elif view == "Daily Returns":
        st.subheader("Daily Returns")
        st.dataframe(df_ret.sort_values(by='Date', ascending=False))
    elif view == "Monthly Returns":
        st.subheader("Monthly Returns")
        st.dataframe(df_monthly_ret.sort_values(by='Date', ascending=False))
with middle_column:
    #st.subheader("Cumulative Return for each stock:")
    st.plotly_chart(fig_cum)
with right_column:
    #st.subheader("Volatility for each stock:")
    st.plotly_chart(fig_vol)

st.markdown('---')
left_column1,  right_column1 = st.columns(2)

with left_column1:
    #st.subheader("Average Rating:")
    st.plotly_chart(fig_pr)
with right_column1:
    #st.subheader("Total Sales:")
    st.plotly_chart(fig)

