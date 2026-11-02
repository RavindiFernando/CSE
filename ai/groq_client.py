"""
Groq AI Client - Free tier API for analysis and briefing
Model: llama-3.3-70b-versatile (free tier, no credit card needed)
"""

import os
import json
import streamlit as st
from typing import Dict, List
from dotenv import load_dotenv
from groq import Groq, RateLimitError

# Load environment variables
load_dotenv()

MODEL = "llama-3.3-70b-versatile"

# Configure Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


def is_ai_configured() -> bool:
    """Check if Groq API key is configured."""
    return bool(GROQ_API_KEY)


def _complete(prompt: str, json_mode: bool = False) -> str:
    """Send a single-turn prompt to Groq and return the response text."""
    kwargs = {"response_format": {"type": "json_object"}} if json_mode else {}
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        **kwargs,
    )
    return response.choices[0].message.content


def analyze_pump(
    symbol: str,
    company_name: str,
    current_price: float,
    price_change_pct: float,
    today_volume: int,
    avg_30d_volume: float,
    volume_spike_ratio: float,
    recent_announcements: List[str],
    tip_message: str = "",
    has_history: bool = True
) -> Dict:
    """
    Use Groq to analyze if a stock shows signs of pump-and-dump.

    Returns:
        dict with verdict, confidence, explanation, red_flags, green_flags, advice
    """
    if not is_ai_configured():
        st.error(
            "Groq API key not configured. "
            "Please add GROQ_API_KEY to .env file."
        )
        return {
            "verdict": "ERROR",
            "confidence": "N/A",
            "explanation": "AI analysis unavailable - API not configured",
            "red_flags": [],
            "green_flags": [],
            "advice": "Configure GROQ_API_KEY in .env file"
        }

    try:
        history_note = "" if has_history else "\n⚠️ NOTE: 30-day historical data is NOT available for this stock (not listed on Yahoo Finance).\nJudge volume spike based on Today's Volume absolute size and trading context only."

        prompt = f"""You are a CSE (Colombo Stock Exchange) market analyst specialising in detecting pump-and-dump schemes in small-cap Sri Lankan stocks.

Analyse this stock and determine if it shows signs of a coordinated pump-and-dump.

STOCK DATA:
- Symbol: {symbol}
- Company: {company_name}
- Current Price: Rs. {current_price:.2f}
- Today's Change: {price_change_pct:+.2f}%
- Today's Volume: {today_volume:,} shares
- 30-day Average Volume: {avg_30d_volume:,.0f} shares if available, else "Unknown"
- Volume Spike Ratio: {volume_spike_ratio:.1f}x normal volume if available, else "Unknown"
- Recent Official Announcements: {recent_announcements or "None found"}
- Tip Message Received: {tip_message or "None provided"}{history_note}

PUMP-AND-DUMP SIGNALS TO CHECK:
1. Volume spike > 3x normal with no official announcement = HIGH RISK
2. Price rise > 10% with volume spike but no announcement = HIGH RISK
3. Vague or hyped language in tip message ("guaranteed", "inside info", "buy now") = RISK
4. No recent announcements explaining the move = SUSPICIOUS
5. Stock is thinly traded (low avg volume) = more vulnerable to manipulation

Respond ONLY in valid JSON, no other text, no markdown code fences:
{{
  "verdict": "LIKELY PUMP or SUSPICIOUS or LOOKS LEGIT",
  "confidence": "HIGH or MEDIUM or LOW",
  "explanation": "2-3 sentence plain English explanation for a retail investor",
  "red_flags": ["specific concern 1", "specific concern 2"],
  "green_flags": ["reassuring factor 1", "reassuring factor 2"],
  "advice": "One sentence practical advice for the investor"
}}"""

        text = _complete(prompt, json_mode=True).strip()

        result = json.loads(text)
        return result

    except RateLimitError:
        st.warning(
            "AI is rate-limited (Groq free tier). "
            "Wait 1 minute and try again."
        )
        return {
            "verdict": "RATE_LIMITED",
            "confidence": "N/A",
            "explanation": "AI service temporarily unavailable due to rate limits",
            "red_flags": [],
            "green_flags": [],
            "advice": "Please try again in 1 minute"
        }

    except json.JSONDecodeError as e:
        st.error(f"AI response parsing failed: {str(e)}. Please try again.")
        return {
            "verdict": "PARSE_ERROR",
            "confidence": "N/A",
            "explanation": "Failed to parse AI response",
            "red_flags": [],
            "green_flags": [],
            "advice": "Please try again"
        }

    except Exception as e:
        st.error(f"AI analysis failed: {str(e)}")
        return {
            "verdict": "ERROR",
            "confidence": "N/A",
            "explanation": f"AI unavailable: {str(e)}",
            "red_flags": [],
            "green_flags": [],
            "advice": "Please try again later"
        }


def generate_briefing(
    gainers: List[Dict],
    losers: List[Dict],
    most_active: List[Dict],
    market_summary: Dict,
    announcements: List[Dict]
) -> str:
    """
    Generate a daily market briefing narrative using Groq.

    Args:
        gainers: List of top gaining stocks
        losers: List of top losing stocks
        most_active: List of most active stocks
        market_summary: Market indices and summary
        announcements: Recent company announcements

    Returns:
        Plain text briefing narrative
    """
    if not is_ai_configured():
        return (
            "Market Briefing Unavailable\n"
            "Groq API key not configured. Add GROQ_API_KEY to .env file."
        )

    try:
        # Format data for prompt
        gainers_str = ", ".join([
            f"{g.get('name', 'N/A')[:20]} (+{g.get('changePercentage', 0):.1f}%)"
            for g in gainers[:3]
        ])
        losers_str = ", ".join([
            f"{l.get('name', 'N/A')[:20]} ({l.get('changePercentage', 0):.1f}%)"
            for l in losers[:3]
        ])
        active_str = ", ".join([
            f"{a.get('name', 'N/A')[:20]} ({a.get('totalVolume', 0):,} shares)"
            for a in most_active[:3]
        ])
        announcements_str = ", ".join([
            ann.get('subject', 'N/A')[:50]
            for ann in announcements[:5]
        ]) or "None today"

        aspi = market_summary.get('aspi', 'N/A')
        aspi_change = market_summary.get('aspichange', 'N/A')
        sl20 = market_summary.get('sl20', 'N/A')
        sl20_change = market_summary.get('sl20change', 'N/A')

        prompt = f"""You are a friendly CSE market analyst writing a morning briefing for Sri Lankan retail investors.
Write in simple, clear English. Be concise. Avoid jargon.

TODAY'S CSE DATA:
Market: ASPI {aspi} ({aspi_change}%), S&P SL20 {sl20} ({sl20_change}%)

Top Gainers: {gainers_str}
Top Losers: {losers_str}
Most Active: {active_str}
Recent Announcements: {announcements_str}

Write a 3-paragraph briefing:
1. Overall market mood today (1-2 sentences)
2. Notable movers and what might explain the moves
3. One thing investors should watch or keep in mind

Keep it under 150 words. Do not make specific buy/sell recommendations. Neutral, helpful tone."""

        return _complete(prompt)

    except RateLimitError:
        return "AI briefing temporarily unavailable (rate limited). Please try again in 1 minute."

    except Exception as e:
        return f"Failed to generate briefing: {str(e)}"
