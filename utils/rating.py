def rating_engine(fund, hist):
    score = 0
    reasons = []
    latest = hist.iloc[-1]

    if fund.get("P/E Ratio") and fund["P/E Ratio"] < 25:
        score += 1
        reasons.append("P/E < 25")
    if fund.get("ROE") and fund["ROE"] > 0.15:
        score += 1
        reasons.append("ROE > 15%")
    if fund.get("Debt to Equity") and fund["Debt to Equity"] < 1:
        score += 1
        reasons.append("Low debt")

    if latest["Close"] > latest["SMA20"] > latest["SMA50"]:
        score += 1
        reasons.append("Bullish SMA trend")
    if latest["RSI"] < 70:
        score += 1
        reasons.append("Healthy RSI")

    if score >= 4:
        return "BUY", score, reasons
    elif score >= 2:
        return "HOLD", score, reasons
    else:
        return "SELL", score, reasons
