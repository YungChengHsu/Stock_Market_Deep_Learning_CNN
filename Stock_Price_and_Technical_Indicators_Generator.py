#!/usr/bin/env python
# coding: utf-8

from datetime import datetime

import csv
import math
import numpy as np
import os
import pandas as pd
import requests
import talib
import time


def get_time_stamp(date):
    date_split = date.split('-')
    return int(datetime.timestamp(datetime(int(date_split[0]), int(date_split[1]), int(date_split[2]))))


def get_stock_raw_data(stock_symbol, time_start, time_end):
    time_start = get_time_stamp(time_start)
    time_end = get_time_stamp(time_end) + 86400

    url = 'https://query1.finance.yahoo.com/v7/finance/download/' + stock_symbol + '?period1=' + str(time_start) + '&period2=' + str(time_end) + '&interval=1d&events=history'
    
    # Try 3 times for timeouts, and if timeout still happens after 3 attempts, print message of unsuccessfulness and return
    timeout_count = 0
    while timeout_count < 3:
        try:
            response = requests.get(url, allow_redirects=True, timeout=10)
            break
        except requests.exceptions.RequestException:
            timeout_count += 1

    if timeout_count >= 3:
        print('************ ' + stock_symbol + ' unsuccessful due to timeout. ************')
        return

    
    print(stock_symbol + ' web query done.')
    
    with open('Stock_price_only/' + stock_symbol + '.csv', 'wb') as r:
        r.write(response.content)
    
    price_data_raw = []
    with open('Stock_price_only/' + stock_symbol + '.csv', newline='') as csvfile:
        rows = csv.reader(csvfile)
        price_data_raw = list(rows)

    #print(price_data_raw)
    date = []
    high_price = []
    low_price = []
    close_price = []
    volumn = []
    for row in price_data_raw[1:]:
        if 'null' not in row:
            date.append(row[0])
            high_price.append(float(row[2]))
            low_price.append(float(row[3]))
            close_price.append(float(row[4]))
            volumn.append(float(row[6]))

    date_array = np.array(date)
    high_price_array = np.array(high_price)
    low_price_array = np.array(low_price)
    close_price_array = np.array(close_price)
    volumn_array = np.array(volumn)

    for_csv = []
    for_csv.append(date)
    for_csv.append(high_price)
    for_csv.append(low_price)
    for_csv.append(close_price)
    for_csv.append(volumn)

    header = ['date', 'highest price', 'lowest price', 'close price', 'volumn']

    # get 11 technical indicators from 6, 7, 8, ..., 10, 17 days ago 
    rsi = []
    for i in range(6, 17):
        for_csv.append(list(talib.RSI(close_price_array, timeperiod=i)))
        header.append('RSI_' + str(i))
    
    cmo = []
    for i in range(6, 17):
        for_csv.append(list(talib.CMO(close_price_array, timeperiod=i)))
        header.append('CMO_' + str(i))
        
    willR = []
    for i in range(6, 17):
        for_csv.append(list(talib.WILLR(high_price_array, low_price_array, close_price_array, timeperiod=i)))
        header.append('WILLR_' + str(i))
        
    cci = []
    for i in range(6, 17):
        for_csv.append(list(talib.CCI(high_price_array, low_price_array, close_price_array, timeperiod=i)))
        header.append('CCI_' + str(i))
        
    roc = []
    for i in range(6, 17):
        for_csv.append(list(talib.ROC(close_price_array, timeperiod=i)))
        header.append('ROC_' + str(i))
        
    ppo = []
    for i in range(6, 17):
        for_csv.append(list(talib.PPO(close_price_array, fastperiod=i, slowperiod=i+14, matype=0)))
        header.append('PPO_' + str(i))
        
    macd = []
    for i in range(6, 17):
        for_csv.append(list(talib.MACD(close_price_array, fastperiod=12, slowperiod=26, signalperiod=i)[0]))
        header.append('MACD_' + str(i))
        
    ema = []
    for i in range(6, 17):
        for_csv.append(list(talib.EMA(close_price_array, timeperiod=i)))
        header.append('EMA_' + str(i))
        
    tema = []
    for i in range(6, 17):
        for_csv.append(list(talib.TEMA(close_price_array, timeperiod=i)))
        header.append('TEMA_' + str(i))
    
    wma = []
    for i in range(6, 17):
        for_csv.append(list(talib.WMA(close_price_array, timeperiod=i)))
        header.append('WMA_' + str(i))
        
    sma = []
    for i in range(6, 17):
        for_csv.append(list(talib.SMA(close_price_array, timeperiod=i)))
        header.append('SMA_' + str(i))

    # Transpose on all the data to have the form of 'a day per row'
    for_csv = list(np.array(for_csv).T)

    with open('Stock_raw_data/' + stock_symbol + '_' + str(time_start) + '-' + str(time_end) + '.csv', 'w', newline='') as csv_file: # change file path name here
        writer = csv.writer(csv_file)
        writer.writerow(header)

        for row in for_csv:
            writer.writerow(row)
    
    print(stock_symbol + ' done.')

os.mkdir('Stock_price_only')
os.mkdir('Stock_raw_data')

get_stock_raw_data('000680.SZ', '2020-01-01', '2020-10-10')
