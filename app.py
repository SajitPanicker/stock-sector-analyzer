import streamlit as st
import yfinance as yf
import pandas as pd
import json
from utils.fundamentals import extract_fundamentals
from utils.technicals import get_technicals
from utils.financials import one_year_financial_summary
from utils.rating import rating_engine

with open("data/sectors.json") as f:
    SECTORS = json.load(f)

st.title("📈 Indian Stock & Sector Analyzer")
st.write("Analyze Indian stocks with fundamentals, technicals, 1-year financials and buy/sell signal.")

option = st.radio("Choose Input Mode:", ["Stock", "Sector"])

if option == "Stock":
    symbol = st.text_input("Enter Indian Stock Symbol (e.g., TCS.NS, HDFCBANK.NS):")

    if symbol:
        info = yf.Ticker(symbol)
        stock_info = info.info
        hist = info.history(period="1y")
        financials = info.financials

        fundamental_data = extract_fundamentals(stock_info)
        technicals = get_technicals(ticker)
        one_year_fin = one_year_financial_summary(financials)
        rating, score, reasons = rating_engine(fundamental_data, technicals)

        st.subheader("📌 Fundamental Ratios")
        st.table(pd.DataFrame(fundamental_data.items(), columns=["Metric", "Value"]))

        st.subheader("📌 Technical Indicators")
        st.line_chart(technicals[["Close", "SMA20", "SMA50", "SMA200"]])

        st.subheader("📌 RSI (14)")
        st.line_chart(technicals[["RSI"]])

        st.subheader("📌 1-Year Financial Summary (Revenue & Profit YoY)")
        if one_year_fin is not None:
            st.table(one_year_fin)
        else:
            st.write("No financial data available")

        st.subheader(f"⭐ Recommendation: {rating} (Score: {score}/5)")
        for r in reasons:
            st.write(f"- {r}")

if option == "Sector":
    sector_name = st.text_input("Enter sector name (e.g., IT, Banking, Pharma):").title()

    if sector_name in SECTORS:
        st.subheader(f"📊 Top Stocks in {sector_name} Sector")

        ranked = []
        for stock in SECTORS[sector_name]:
            try:
                info = yf.Ticker(stock)
                stock_info = info.info
                hist = info.history(period="1y")

                fundamental_data = get_fundamentals(ticker)
                technicals = get_technicals(ticker)

                if technicals.get("history") is None:
                    st.error("No price history found. Try another ticker, e.g., TCS.NS, INFY.NS, RELIANCE.NS")
                else:
                    rating, score, reasons = rating_engine(fundamental_data, technicals)
                    st.success(f"Rating: {rating}")
                    st.write("Reasons:")
                    st.write(reasons)


                ranked.append((stock, score))
            except:
                pass

        ranked = sorted(ranked, key=lambda x: x[1], reverse=True)[:3]

        st.write("### 🏆 Top 3 Recommendations")
        for s, sc in ranked:
            st.write(f"**{s}** — Score: {sc}/5")
    else:
        st.write("Sector not found. Modify `sectors.json` to add more.")
