import yfinance as yf
import numpy as np
import pandas as pd


class FearAndGreed:
    def calculate(self, vix, market_momentum, safe_haven_ratio, trading_volume_change):
        """
        Calculate a basic Fear and Greed Index.

        Parameters:
            vix (float): Volatility index value (higher means more fear).
            market_momentum (float): Relative market performance (higher means more greed).
            safe_haven_ratio (float): Ratio of bond/gold performance to stocks (higher means more fear).
            trading_volume_change (float): Change in trading volume (higher means more greed).

        Returns:
            float: Fear and Greed Index (0 to 100).
        """
        # Normalize each factor to a scale of 0-100
        vix_score = 100 - np.clip(vix, 0, 100)  # Higher VIX = more fear
        momentum_score = np.clip(
            market_momentum, 0, 100
        )  # Higher momentum = more greed
        safe_haven_score = 100 - np.clip(
            safe_haven_ratio, 0, 100
        )  # Higher safe-haven demand = more fear
        volume_score = np.clip(
            trading_volume_change, 0, 100
        )  # Higher trading volume = more greed

        # Average all scores
        fear_and_greed_index = (
            vix_score + momentum_score + safe_haven_score + volume_score
        ) / 4
        return fear_and_greed_index
