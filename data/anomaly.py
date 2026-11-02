"""
Anomaly Detection Logic - Detects volume spikes and price momentum
Pure Python/pandas implementation for pump-and-dump pattern detection
"""

import pandas as pd
from typing import Dict, Optional


def calculate_volume_spike(history_df: pd.DataFrame, today_volume: int) -> Dict:
    """
    Calculate volume spike ratio and severity.
    
    Args:
        history_df: DataFrame with 'Volume' column (30 days of data)
        today_volume: Today's volume from CSE API
    
    Returns:
        dict with spike_ratio, avg_volume, is_anomaly, severity
    """
    if history_df.empty or len(history_df) < 5:
        return {
            "spike_ratio": None,
            "avg_volume": None,
            "is_anomaly": False,
            "severity": "unknown"
        }
    
    avg_volume = history_df["Volume"].mean()
    spike_ratio = today_volume / avg_volume if avg_volume > 0 else 0
    
    # Thresholds based on CSE thin-market characteristics
    if spike_ratio >= 5:
        severity = "EXTREME"    # > 5x normal = very suspicious
    elif spike_ratio >= 3:
        severity = "HIGH"       # 3-5x normal = suspicious
    elif spike_ratio >= 2:
        severity = "MODERATE"   # 2-3x normal = worth noting
    else:
        severity = "NORMAL"     # < 2x = nothing unusual
    
    return {
        "spike_ratio": round(spike_ratio, 2),
        "avg_volume": int(avg_volume),
        "is_anomaly": spike_ratio >= 3,
        "severity": severity,
        "today_volume": today_volume
    }


def calculate_price_momentum(history_df: pd.DataFrame) -> Dict:
    """
    Calculate 1-week and 1-month price momentum.
    
    Args:
        history_df: DataFrame with 'Close' column
    
    Returns:
        dict with week_change_pct, month_change_pct, current_price
    """
    if history_df.empty:
        return {}
    
    closes = history_df["Close"]
    current = closes.iloc[-1]
    week_ago = closes.iloc[-5] if len(closes) >= 5 else closes.iloc[0]
    month_ago = closes.iloc[0]
    
    week_change = ((current - week_ago) / week_ago) * 100 if week_ago > 0 else 0
    month_change = ((current - month_ago) / month_ago) * 100 if month_ago > 0 else 0
    
    return {
        "week_change_pct": round(week_change, 2),
        "month_change_pct": round(month_change, 2),
        "current_price": round(current, 2),
    }


def detect_pump_signals(
    price_change_pct: float,
    volume_spike_ratio: float,
    has_announcement: bool,
    avg_volume: Optional[int] = None
) -> Dict:
    """
    Detect pump-and-dump signals based on price and volume anomalies.
    
    Args:
        price_change_pct: Percentage price change today
        volume_spike_ratio: Today's volume / 30-day average volume
        has_announcement: Whether there's an official announcement
        avg_volume: 30-day average volume (for thin-market detection)
    
    Returns:
        dict with risk_score, signals, concerns
    """
    signals = []
    risk_score = 0  # 0-100
    
    # Signal 1: Volume spike > 3x with no announcement
    if volume_spike_ratio >= 3 and not has_announcement:
        signals.append("HIGH volume spike without official announcement")
        risk_score += 40
    
    # Signal 2: Price rise > 10% with volume spike but no announcement
    if price_change_pct > 10 and volume_spike_ratio >= 2 and not has_announcement:
        signals.append("Double-digit price jump with volume spike (no news)")
        risk_score += 35
    
    # Signal 3: Extreme volume spike (> 5x)
    if volume_spike_ratio >= 5:
        signals.append("EXTREME volume spike (>5x normal)")
        risk_score += 25
    
    # Signal 4: Thinly traded stock (high manipulation risk)
    if avg_volume is not None and avg_volume < 10000:
        signals.append("Thinly traded stock (low average volume)")
        risk_score += 15
    
    # Signal 5: Large price move with moderate volume
    if price_change_pct > 15 and volume_spike_ratio >= 2:
        signals.append("Large price move with elevated volume")
        risk_score += 20
    
    # Green flag: Announcement explaining the move
    if has_announcement:
        risk_score -= 25
    
    # Green flag: Moderate volume with price move (organic activity)
    if volume_spike_ratio < 2 and price_change_pct < 5:
        risk_score -= 10
    
    # Cap score between 0-100
    risk_score = max(0, min(100, risk_score))
    
    return {
        "risk_score": risk_score,
        "signals": signals,
        "high_risk": risk_score > 70,
        "medium_risk": 40 < risk_score <= 70,
        "low_risk": risk_score <= 40
    }
