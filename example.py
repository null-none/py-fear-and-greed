import yfinance as yf
import numpy as np
import pandas as pd

from src.fear_and_greed import FearAndGreed


def fetch_data():
    # Fetch VIX data (Volatility Index)
    vix = yf.download("^VIX", period="7d", interval="1d")["Close"]
    vix_latest = vix.iloc[-1]

    # Fetch S&P 500 data (Market Momentum)
    sp500 = yf.download("^GSPC", period="1mo", interval="1d")["Close"]
    market_momentum = ((sp500.iloc[-1] - sp500.mean()) / sp500.mean()) * 100

    # Fetch Gold and Bond data for safe-haven ratio
    gold = yf.download("GC=F", period="1mo", interval="1d")["Close"]  # Gold Futures
    bonds = yf.download("TLT", period="1mo", interval="1d")[
        "Close"
    ]  # 20-Year Treasury ETF
    safe_haven_ratio = ((gold.iloc[-1] + bonds.iloc[-1]) / sp500.iloc[-1]) * 100

    # Trading volume data (SPY as a proxy)
    spy = yf.download("SPY", period="1mo", interval="1d")
    trading_volume_change = (
        (spy["Volume"].iloc[-1] - spy["Volume"].mean()) / spy["Volume"].mean()
    ) * 100

    return vix_latest, market_momentum, safe_haven_ratio, trading_volume_change


vix_latest, market_momentum, safe_haven_ratio, trading_volume_change = fetch_data()

fear_and_greed = FearAndGreed()
fear_and_greed_index = fear_and_greed.calculate(
    vix_latest, market_momentum, safe_haven_ratio, trading_volume_change
)

print(f"Fear and Greed Index: {fear_and_greed_index:.2f}")
