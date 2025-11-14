def extract_fundamentals(info):
    return {
        "P/E Ratio": info.get("trailingPE"),
        "P/B Ratio": info.get("priceToBook"),
        "ROE": info.get("returnOnEquity"),
        "ROCE": info.get("returnOnCapitalEmployed"),
        "Debt to Equity": info.get("debtToEquity"),
        "EPS": info.get("trailingEps"),
        "Market Cap": info.get("marketCap"),
    }
