import pandas as pd
tickerframe = pd.read_excel(r"C:\Users\cbec\Downloads\Yahoo-Ticker-Symbols-September-2017\Yahoo Ticker Symbols - September 2017.xlsx")
tickerframe = tickerframe.iloc[3:].dropna(subset=['Yahoo Stock Tickers'])
print("Kay")