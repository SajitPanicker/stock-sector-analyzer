import yfinance as yf
import pandas as pd

def get_technicals(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")

        if hist.empty:
            return {"history": None}

        hist["SMA20"] = hist["Close"].rolling(20).mean()
        hist["SMA50"] = hist["Close"].rolling(50).mean()
        hist["SMA200"] = hist["Close"].rolling(200).mean()

        return {
            "history": hist,
            "sma20": hist["SMA20"].iloc[-1],
            "sma50": hist["SMA50"].iloc[-1],
            "sma200": hist["SMA200"].iloc[-1],
        }

    except Exception as e:
        return {"history": None}
