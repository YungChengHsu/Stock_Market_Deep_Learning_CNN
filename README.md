# Stock_Price_and_Technical_Indicators_Generator
This is a tool to download stock price data from Yahoo Finance and generate trading techincal indicators with downloaded stock price data (in .csv files) using TA-Lib.

The technical indicators obtainable with this tool:
* RSI
* CMO
* WILLR
* CCI
* ROC
* PPO
* MACD
* EMA
* TEMA
* WMA
* SMA


## Dependencies
* [TA-Lib](https://github.com/mrjbq7/ta-lib)
* [requests](https://pypi.org/project/requests/)

## Usage
1. Open and edit the `file Stock_Price_and_Technical_Indicators_Generator.py`
2. Scroll down to the bottom and fill in the **stock symbol (Ticker)**, the **start date of the stock data**, the **end date of the stock data**, the **start time of the indicator (in days)**, the **end time of the indicator (in days)** in `get_stock_raw_data(stock_symbol, start_date, end_date, indicator_time_start, indicator_time_end)`, e.g. If I want to get stock data and technical indicators of '000680.SZ' from 2020-01-01 to 2020-10-10 ranged from 17 days ago to 6 days ago, then I should fill in the function in this way: `get_stock_raw_data('000680.SZ', '2020-01-01', '2020-10-10', 6, 17)`
3. There will be 2 folders created, `Stock_price_only`, which contains **only the price data of a stock** in .csv files downloaded from Yahoo Finance, and `Stock_raw_data`, which contains both **the price data of a stock** and **technical indicators** in .csv files
