def calculate_cumulative_returns(df):
      # df = dataframe with prices
      # Calculate the cumulative return for each stock over the entire period
    cumulative_return = (df.iloc[-1] / df.iloc[0] - 1) * 100
    
    return cumulative_return