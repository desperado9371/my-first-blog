from django.shortcuts import render
from binance.client import Client
from datetime import datetime
import numpy as np
import pandas as pd
import ta

def post_list(request):
    client = Client('ng0Zhq6ea42X3QxMV2RAubZxs508gguTISRwM13lQFFPrDDTxRiqmq3pBvIcvJMy',
                    'vHZDWuQvPf4mcaDvzxwRbtIWDbWuCyFyyG59bCZeTW6A6sd98qbHfCsFDVDdN3wn')
    klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 month ago UTC")
    unix_timestamps = []
    for kline in klines:
        unix_timestamps.append(kline[0])

    timestamps = []

    closed_prices = []
    open_prices = []
    high_prices = []
    low_prices = []
    volume = []

    df = pd.DataFrame(list(zip(open_prices, closed_prices, high_prices, low_prices, volume)), index=timestamps,
                      columns=['open', 'close', 'high', 'low', 'volume'])

    for kline in klines:
        closed_prices.append(float(kline[4]))
        open_prices.append(float(kline[1]))
        high_prices.append(float(kline[2]))
        low_prices.append(float(kline[3]))
        volume.append(float(kline[5]))

    for unix_timestamp in unix_timestamps:
        timestamps.append(datetime.fromtimestamp(unix_timestamp / 1000).strftime("%m/%d/%Y"))

    for kline in klines:
        unix_timestamps.append(kline[0])

    candledata = []
    for i in range(len(timestamps)):
        candledata.append([timestamps[i],low_prices[i],open_prices[i],closed_prices[i],high_prices[i]])

    print(candledata)

    return render(request, 'blog/post_list.html', {'data': closed_prices,
                                                   'labels': timestamps,
                                                   'candle':candledata,})