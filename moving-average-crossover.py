import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

symbol = "TSLA"
start_date = "2020-01-01"
end_date = "2023-01-01"
short_window = 20
long_window = 50

df = yf.download(symbol, start=start_date, end=end_date, auto_adjust=False)
df.dropna(inplace=True)

#Calculation of moving averages
df["SMA20"] = df["Close"].rolling(window=short_window).mean()
df["SMA50"] = df["Close"].rolling(window=long_window).mean()

#Signal generation
df["Signal"] = 0
df.loc[df.index[long_window:], "Signal"] = (
    (df["SMA20"] > df["SMA50"]).astype(int).loc[df.index[long_window:]]
)
df["Position"] = df["Signal"].diff()

# Generates buy/sell csv
signals_df = df[df["Position"].isin([1, -1])].copy()
signals_df["Trade"] = signals_df["Position"].map({1: "Buy", -1: "Sell"})
signals_df = signals_df[["Trade", "Close", "SMA20", "SMA50"]]
signals_df.index.name = "Date"

os.makedirs("signals", exist_ok=True)
signals_df.to_csv("signals/buy_sell_signals.csv")
print("Buy/Sell signals saved to signals/buy_sell_signals.csv")

#Ploting
plt.figure(figsize=(14, 7))
plt.plot(df["Close"], label="Close Price", alpha=0.5)
plt.plot(df["SMA20"], label="SMA 20", alpha=0.75)
plt.plot(df["SMA50"], label="SMA 50", alpha=0.75)

# Buy signals
plt.plot(df[df["Position"] == 1].index,
         df["SMA20"][df["Position"] == 1],
         "^", markersize=10, color="green", label="Buy Signal")

#Sell signals
plt.plot(df[df["Position"] == -1].index,
         df["SMA20"][df["Position"] == -1],
         "v", markersize=10, color="red", label="Sell Signal")

plt.title(f"{symbol} Moving Average Crossover Strategy")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.legend()
plt.grid()

os.makedirs("plots", exist_ok=True)
plt.savefig("plots/crossover_plot.png")
plt.show()
