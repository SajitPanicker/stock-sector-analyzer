def rating_engine(fundamental_data, technicals):
    hist = technicals.get("history")

    # Handle missing historical data
    if hist is None or hist.empty:
        return (
            "N/A",
            0,
            ["Historical price data not available. Rating cannot be computed for this ticker."]
        )

    latest = hist.iloc[-1]

    score = 0
    reasons = []

    # Fundamental scoring
    pe = fundamental_data.get("pe")
    roe = fundamental_data.get("roe")

    if pe:
        if pe < 20:
            score += 1
            reasons.append("PE ratio is attractive")
        else:
            reasons.append("PE ratio is high")

    if roe:
        if roe > 0.15:
            score += 1
            reasons.append("ROE is strong")
        else:
            reasons.append("ROE is weak")

    # Technical scoring
    sma20 = technicals.get("sma20")
    sma50 = technicals.get("sma50")
    sma200 = technicals.get("sma200")

    if sma20 and sma50 and sma20 > sma50:
        score += 1
        reasons.append("Short-term trend is positive")

    if sma50 and sma200 and sma50 > sma200:
        score += 1
        reasons.append("Medium-term trend is positive")

    if score >= 3:
        rating = "BUY"
    elif score == 2:
        rating = "HOLD"
    else:
        rating = "SELL"

    return rating, score, reasons

