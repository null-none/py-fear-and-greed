## Fear & Greed Index 

**Explanation**

1. **Data Sources**:

• ^VIX: Volatility Index (used for fear calculation).

• ^GSPC: S&P 500 Index (used for market momentum).

• GC=F: Gold futures (safe-haven asset).

• TLT: 20+ Year Treasury Bond ETF (safe-haven asset).

• SPY: S&P 500 ETF (proxy for trading volume).

2. **Normalization**:

• We normalize each metric to a scale of 0-100 for easier calculation.

1. **Index Calculation**:

• Combine normalized scores to compute the average Fear and Greed Index.

2. **Outputs**:

• The index ranges from 0 (extreme fear) to 100 (extreme greed).

#### Example

```python
import yfinance as yf
import numpy as np
import pandas as pd

from src.fear_and_greed import FearAndGreed  # Make sure the path is correct


def fetch_data():
    # Fetch VIX data (Volatility Index)
    vix = yf.download("^VIX", period="7d", interval="1d", auto_adjust=False)["Close"]
    vix_latest = vix.iloc[-1] if not vix.empty else np.nan

    # Fetch S&P 500 data (Market Momentum)
    sp500 = yf.download("^GSPC", period="1mo", interval="1d", auto_adjust=False)[
        "Close"
    ]
    market_momentum = (
        ((sp500.iloc[-1] - sp500.mean()) / sp500.mean()) * 100
        if not sp500.empty
        else np.nan
    )

    # Fetch Gold and Bond data for safe-haven ratio
    gold = yf.download("GC=F", period="1mo", interval="1d", auto_adjust=False)["Close"]
    bonds = yf.download("TLT", period="1mo", interval="1d", auto_adjust=False)["Close"]

    safe_haven_ratio = (
        (
            (list(gold.iloc[-1])[-1] + list(bonds.iloc[-1])[-1])
            / list(sp500.iloc[-1])[-1]
        )
        * 100
        if not gold.empty and not bonds.empty and not sp500.empty
        else np.nan
    )

    # Trading volume data (SPY as a proxy)
    spy = yf.download("SPY", period="1mo", interval="1d", auto_adjust=False)
    if not spy.empty:
        trading_volume_change = (
            (spy["Volume"].iloc[-1] - spy["Volume"].mean()) / spy["Volume"].mean()
        ) * 100
    else:
        trading_volume_change = np.nan

    return vix_latest, market_momentum, safe_haven_ratio, trading_volume_change


def interpret_score(score):
    """
    Interprets the Fear and Greed score and returns a human-readable label.
    """
    if score < 20:
        return "Extreme Fear"
    elif score < 40:
        return "Fear"
    elif score < 60:
        return "Neutral"
    elif score < 80:
        return "Greed"
    else:
        return "Extreme Greed"


def main():
    print("Fetching data from Yahoo Finance...")
    vix, momentum, haven, volume = fetch_data()

    fg = FearAndGreed()
    score = fg.calculate(list(vix)[-1], list(momentum)[-1], haven, list(volume)[-1])
    print(interpret_score(score))


if __name__ == "__main__":
    main()
```