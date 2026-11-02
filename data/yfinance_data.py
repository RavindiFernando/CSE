"""
yfinance Historical Data - Fetches 30-day price and volume history
CSE stocks on Yahoo Finance use .CM suffix
"""

import yfinance as yf
import pandas as pd
import streamlit as st
from typing import Optional


def cse_to_yahoo(cse_symbol: str) -> str:
    """
    Convert CSE symbol to Yahoo Finance symbol.
    Example: DIAL.N0000 → DIAL.CM
    """
    base = cse_symbol.split(".")[0] if "." in cse_symbol else cse_symbol
    return f"{base}.CM"


@st.cache_data(ttl=3600)
def get_price_volume_history(cse_symbol: str, days: int = 30) -> pd.DataFrame:
    """
    Fetch 30-day (or custom) historical price and volume data for a CSE stock.
    
    Args:
        cse_symbol: CSE stock symbol (e.g., "DIAL.N0000")
        days: Number of days of history to fetch (default 30)
    
    Returns:
        DataFrame with columns: Close, Volume
        Empty DataFrame if data not available
    """
    try:
        yahoo_symbol = cse_to_yahoo(cse_symbol)
        ticker = yf.Ticker(yahoo_symbol)
        
        # Fetch historical data
        df = ticker.history(period=f"{days}d", interval="1d")
        
        # Return only Close and Volume columns
        result = df[["Close", "Volume"]].dropna()
        
        if result.empty:
            st.warning(
                f"Historical data not available for {cse_symbol} on Yahoo Finance. "
                "Pump analysis will use today's data only (less accurate)."
            )
        
        return result
    
    except Exception as e:
        st.warning(
            f"Failed to fetch historical data for {cse_symbol}: {str(e)}. "
            "Continuing with today's data only."
        )
        return pd.DataFrame()


def get_price_trends(cse_symbol: str, days: int = 30) -> dict:
    """
    Calculate price momentum and trends from historical data.
    
    Returns:
        dict with:
        - week_change_pct: 1-week price change percentage
        - month_change_pct: 30-day price change percentage
        - current_price: Latest closing price
        - avg_volume: Average volume over period
    """
    history_df = get_price_volume_history(cse_symbol, days)
    
    if history_df.empty:
        return {}
    
    closes = history_df["Close"]
    volumes = history_df["Volume"]
    current = closes.iloc[-1]
    week_ago = closes.iloc[-5] if len(closes) >= 5 else closes.iloc[0]
    month_ago = closes.iloc[0]
    
    week_change = ((current - week_ago) / week_ago) * 100 if week_ago > 0 else 0
    month_change = ((current - month_ago) / month_ago) * 100 if month_ago > 0 else 0
    
    return {
        "week_change_pct": round(week_change, 2),
        "month_change_pct": round(month_change, 2),
        "current_price": round(current, 2),
        "avg_volume": int(volumes.mean()),
        "min_price": round(closes.min(), 2),
        "max_price": round(closes.max(), 2),
    }


def get_historical_for_chart(cse_symbol: str, days: int = 30) -> Optional[pd.DataFrame]:
    """
    Get historical data formatted for charting.
    """
    df = get_price_volume_history(cse_symbol, days)
    return df if not df.empty else None
