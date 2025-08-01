import pandas as pd
tickerframe = pd.read_excel(r"Yahoo Ticker Symbols - September 2017.xlsx")
tickerframe = tickerframe.iloc[3:].dropna(subset=['Yahoo Stock Tickers'])
print("Kay")
