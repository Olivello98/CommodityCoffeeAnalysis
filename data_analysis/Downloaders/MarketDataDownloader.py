from heapq import merge

import numpy as np
import pandas as pd
import datetime as dt
import seaborn as sns
import pandas_datareader as dr
import yfinance as yf
import matplotlib.pyplot as plt



#Load Data

start = dt.datetime(2024,1,1)
end = dt.datetime(2024,6,1)

# Define ticker symbols and names for coffee futures
tickers = {
    "Coffee Mar 25": "KCH25.NYB",
    "Coffee May 25": "KCK25.NYB",
    "Coffee Jul 25": "KCN25.NYB",
    "Coffee Sep 25": "KCU25.NYB"# Coffee futures
}

# Create an empty DataFrame to hold all the futures data
all_futures_data = pd.DataFrame()

# Download data and fill the DataFrame
for commodity, ticker in tickers.items():
    data = yf.download(ticker, start, end)
    data = data[['Adj Close', 'Volume']].rename(
        columns={'Adj Close': f'{commodity} Adjusted Price', 'Volume': f'{commodity} Volume'})
    data.reset_index(inplace=True)
    if all_futures_data.empty:
        all_futures_data = data
    else:
        all_futures_data = pd.merge(all_futures_data, data, on="Date", how="outer")

# Interpolate missing values linearly
all_futures_data.interpolate("linear", inplace=True)

# Display the combined table
print("Combined Futures Data:")
print(all_futures_data.head())

# Plotting the data using matplotlib
plt.figure(figsize=(12, 8))

# Define colors using a colormap
colors = plt.cm.get_cmap('tab10', len(tickers))

# Plot each commodity's volume data
for idx, commodity in enumerate(tickers.keys()):
    plt.plot(all_futures_data['Date'], all_futures_data[f'{commodity} Volume'], marker='o', linestyle='-',
             color=colors(idx), label=commodity)

# Formatting the plot
plt.title('Coffee Arabica NYMEX Futures Volumes in Q1/Q2 2024', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Daily Volume', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True, linestyle='--', linewidth=0.7)
plt.legend(title="Commodity", fontsize=12, title_fontsize='13')

# Make the plot tighter and show it
plt.tight_layout()
# plt.show()

# Plot each commodity's volume data
for idx, commodity in enumerate(tickers.keys()):
    plt.plot(all_futures_data['Date'], all_futures_data[f'{commodity} Adjusted Price'], marker='o', linestyle='-',
             color=colors(idx), label=commodity)

# Formatting the plot
plt.title('Coffee Arabica NYMEX Futures EOD Adj Prices in Q1/Q2 2024', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('EOD Price', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True, linestyle='--', linewidth=0.7)
plt.legend(title="Commodity", fontsize=12, title_fontsize='13')

# Make the plot tighter
plt.tight_layout()

# Show the plot
# plt.show()

countries = ['Brazil', 'Vietnam', 'Ethiopia', 'Uganda']
coffee_df = pd.read_csv("~/PycharmProjects/CommodityCoffeeAnalysis/data_analysis/sources/psd_coffee.csv")
filtered_coffee_df = coffee_df[coffee_df['Country'].isin(countries)]

# Display the filtered DataFrame
print(filtered_coffee_df)
