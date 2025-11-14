import pandas as pd

def one_year_financial_summary(financials):
    if financials is None or financials.empty:
        return None

    df = financials.T
    df["Revenue Growth %"] = df["Total Revenue"].pct_change() * 100
    df["Net Income Growth %"] = df["Net Income"].pct_change() * 100

    return df.tail(2)
