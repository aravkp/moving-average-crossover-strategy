# moving-average-crossover-strategy
Python script that implements a moving average crossover strategy using data from historical stock data from Yahoo Finance. Generates buy/sell signals, saves them to a csv, and plots the strategy using matplotlib.

Libraries used: os, yfinance, pandas, matplotlib

What the script does (in detail):

1. Fetches historical stock data for the ticker (TSLA in this case)
2. Computes simple moving averages 20 days and 50 days.
3. Generate buy and sell signals when the short-term average (20 days) crosses the long-term
4. Save said signals into a csv file
5. Plot the signals with matplotlib (price, SMAs, and signal arrows)
