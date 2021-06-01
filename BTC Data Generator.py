import ccxt
import time
import csv


# This program downloads every minute candle since the given
# UNIX timestamp and writes it to a CSV file.
# For one million candles, it takes a bit over 30 minutes to download everything.


# All UNIX times are in milliseconds
beginning = int(time.time() - 60 * 10 ** 6) * 1000  # One million minutes ago in UNIX format
now = int(time.time()) * 1000  # UNIX Time right now

# Add every minute to data since "beginning"
data = []
while beginning < now:
    data += ccxt.binance().fetch_ohlcv('BTC/USDT', '1m', since=beginning)  # Limited to 500 candles
    beginning += 500 * 60 * 1000  # Add 500 minutes
    print("Added 500 candles")

# Write to a CSV file
with open('TwoYearBitcoinData.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # Add header row
    writer.writerow(["Timestamp", "Open", "High", "Low", "Close", "Volume"])
    # Add the data
    writer.writerows(data)
