import ccxt
import time
import requests


# This program fetches data, manipulates it and sends it as a webhook to the given url once every minute

# This is needed to run the program exactly once every 60 seconds
startTime = time.time()

while True:
    # Create the data
    fifty_two_minutes_ago = int(time.time() - 52 * 60) * 1000  # Unix timestamp in milliseconds
    data = ccxt.binance().fetch_ohlcv('BTC/USDT', '1m', since=fifty_two_minutes_ago)

    open, high, low, close = [data[-1][i] for i in (1, 2, 3, 4)]

    # Dictionary that stores all the values (and add some of them)
    normalized_values = {'closeOpen': close / open, 'lowOpen': low / open, 'highOpen': high / open}

    # Close / Previous close for n-k, k = {0, ..., 10}
    for i in range(11):
        normalized_values[f'closePreviousCloseNMinus{i}'] = data[-i - 1][4] / data[-i - 2][4]

    # 20 minute close / previous close average
    twenty_minute_total = 0
    for i in range(20):
        twenty_minute_total += data[-i - 2][4] / data[-i - 3][4]
    normalized_values['twentyMinuteCloseAvg'] = twenty_minute_total / 20

    # 50 minute close / previous close average
    fifty_minute_total = 0
    for i in range(50):
        fifty_minute_total += data[-i - 2][4] / data[-i - 3][4]
    normalized_values['fiftyMinuteCloseAvg'] = fifty_minute_total / 50

    # Add the 100 minute average here if your model needs it

    # Send the webhook
    url = 'Put your webhook destination url here'
    r = requests.post(url, data=normalized_values)

    # Print a message in the console
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print("Successful run at: " + current_time)

    # Wait almost 60 seconds
    time.sleep(60 - ((time.time() - startTime) % 60.0))
