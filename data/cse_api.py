"""
CSE Direct API - Unofficial but publicly accessible API used by cse.lk
Requires browser-like headers to avoid 403 errors.
"""

import requests
import time
import streamlit as st
from typing import Dict, List, Optional

BASE_URL = "https://www.cse.lk/api/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://www.cse.lk",
    "Referer": "https://www.cse.lk/",
    "Content-Type": "application/x-www-form-urlencoded",
}


@st.cache_data(ttl=300)
def get_top_gainers() -> List[Dict]:
    """
    Fetch top gaining stocks today.
    Returns list of stocks with highest percentage gain.
    """
    try:
        response = requests.post(
            f"{BASE_URL}topGainers",
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data.get("reqTopGainerInfo", [])
    except requests.RequestException as e:
        st.error(f"Failed to fetch top gainers: {str(e)}")
        return []


@st.cache_data(ttl=300)
def get_top_losers() -> List[Dict]:
    """
    Fetch top losing stocks today.
    Returns list of stocks with highest percentage loss.
    """
    try:
        response = requests.post(
            f"{BASE_URL}topLooses",
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data.get("reqTopLooserInfo", [])
    except requests.RequestException as e:
        st.error(f"Failed to fetch top losers: {str(e)}")
        return []


@st.cache_data(ttl=300)
def get_most_active_stocks() -> List[Dict]:
    """
    Fetch highest volume traded stocks today.
    Returns list of stocks by total volume traded.
    """
    try:
        response = requests.post(
            f"{BASE_URL}mostActiveTrades",
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data.get("reqMostActiveInfo", [])
    except requests.RequestException as e:
        st.error(f"Failed to fetch most active stocks: {str(e)}")
        return []


@st.cache_data(ttl=300)
def get_all_sectors() -> List[Dict]:
    """
    Fetch all CSE sector performance.
    """
    try:
        response = requests.post(
            f"{BASE_URL}allSectors",
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data.get("reqAllSectorInfo", [])
    except requests.RequestException as e:
        st.error(f"Failed to fetch sector data: {str(e)}")
        return []


@st.cache_data(ttl=300)
def get_daily_market_summary() -> Dict:
    """
    Fetch overall market summary (ASPI, S&P SL20).
    """
    try:
        response = requests.post(
            f"{BASE_URL}dailyMarketSummery",
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data.get("reqDailyMarketSummeryInfo", {})
    except requests.RequestException as e:
        st.error(f"Failed to fetch market summary: {str(e)}")
        return {}


def get_company_info(symbol: str) -> Dict:
    """
    Fetch one company's live data by symbol.
    Uses POST method.
    """
    try:
        response = requests.post(
            f"{BASE_URL}companyInfoSummery",
            data={"symbol": symbol},
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data.get("reqSymbolInfo", {})
    except requests.RequestException as e:
        st.error(f"Failed to fetch company info for {symbol}: {str(e)}")
        return {}


@st.cache_data(ttl=300)
def get_approved_announcements() -> List[Dict]:
    """
    Fetch recent company announcements.
    """
    try:
        response = requests.post(
            f"{BASE_URL}approvedAnnouncement",
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data.get("reqApprovedAnnouncementInfo", [])
    except requests.RequestException as e:
        st.error(f"Failed to fetch announcements: {str(e)}")
        return []


@st.cache_data(ttl=300)
def get_trade_summary() -> List[Dict]:
    """
    Fetch all securities trade summary.
    """
    try:
        response = requests.post(
            f"{BASE_URL}tradeSummary",
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data.get("reqTradeSummaryInfo", [])
    except requests.RequestException as e:
        st.error(f"Failed to fetch trade summary: {str(e)}")
        return []


def get_announcements_for_symbol(symbol: str) -> List[Dict]:
    """
    Filter announcements for a specific symbol.
    """
    all_announcements = get_approved_announcements()
    symbol_base = symbol.split(".")[0] if "." in symbol else symbol
    
    filtered = [
        ann for ann in all_announcements
        if symbol_base.upper() in (ann.get("symbol", "") or "").upper()
    ]
    
    return filtered


def validate_symbol_format(symbol: str) -> bool:
    """
    Validate CSE symbol format (e.g., DIAL.N0000)
    """
    import re
    pattern = r"^[A-Z]+\.[A-Z0-9]+$"
    return bool(re.match(pattern, symbol.upper()))
