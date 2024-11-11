from heapq import merge

import numpy as np
import pandas as pd
import datetime as dt
import pandas_datareader as dr
import yfinance as yf
import finplot as fplt
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

# Create an empty list to hold each DataFrame
data_frames = []

# Loop over tickers, download the data, and add each to the list
for commodity, ticker in tickers.items():
    # Download data
    data = yf.download(ticker, start, end)
    # Keep only Adjusted Close and Volume, and rename columns
    data = data[['Adj Close', 'Volume']].rename(columns={'Adj Close': 'Adjusted Price', 'Volume': 'Volume'})
    # Add a column to identify the commodity type
    data['Commodity'] = commodity
    # Reset index to make Date a column
    data.reset_index(inplace=True)
    # Append to list
    data_frames.append(data)

# Concatenate all data into one table
all_futures_data = pd.concat(data_frames, axis=1)
all_futures_data.interpolate("linear", inplace=True)
# Display the combined table
print("Combined Futures Data:")
print(all_futures_data.head())


# Plotting setup
plt.figure(figsize=(10, 6))  # Set the figure size

# Plot each column against the Date index
plt.plot(all_futures_data.index, all_futures_data['Coffee Mar 25'], marker='o', label='Coffee Mar 25')
plt.plot(all_futures_data.index, all_futures_data['Coffee May 25'], marker='o', label='Coffee May 25')
plt.plot(all_futures_data.index, all_futures_data['Coffee Jul 25'], marker='o', label='Coffee Jul 25')
plt.plot(all_futures_data.index, all_futures_data['Coffee Sep 25'], marker='o', label='Coffee Sep 25')

# Adding title and labels
plt.title('Trading Volumes for Futures over Time')
plt.xlabel('Date')
plt.ylabel('Trading Volume')
plt.xticks(rotation=45)  # Rotate date labels for better readability

# Adding a legend
plt.legend(title='Futures Types')

# Displaying the grid
plt.grid(True)

# Show the plot
plt.tight_layout()  # Adjust layout to make room for rotated x-axis labels
plt.show()