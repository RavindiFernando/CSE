"""
Formatters - Number formatting, color helpers, and display utilities
"""


def format_currency(value: float, prefix: str = "Rs. ") -> str:
    """
    Format a number as currency with commas.
    Example: 1234567.89 → "Rs. 1,234,567.89"
    """
    if isinstance(value, (int, float)):
        return f"{prefix}{value:,.2f}"
    return str(value)


def format_volume(value: int) -> str:
    """
    Format volume with commas and optional millions/thousands suffix.
    Example: 1234567 → "1,234,567" or "1.2M"
    """
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value / 1_000:.1f}K"
    return str(value)


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format percentage with sign and color emoji.
    Example: 5.2 → "+5.20%"
    Example: -2.1 → "-2.10%"
    """
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.{decimals}f}%"


def get_color_for_change(change_pct: float) -> str:
    """
    Get HTML color code for positive (green) or negative (red) change.
    """
    if change_pct > 0:
        return "#00AA44"  # Green
    elif change_pct < 0:
        return "#FF4444"  # Red
    else:
        return "#999999"  # Gray


def get_emoji_for_change(change_pct: float) -> str:
    """
    Get emoji for positive (🟢) or negative (🔴) change.
    """
    if change_pct > 0:
        return "🟢"
    elif change_pct < 0:
        return "🔴"
    else:
        return "⚪"


def format_price_with_change(price: float, change_pct: float) -> str:
    """
    Format price with change indicator.
    Example: "Rs. 125.50 🟢 +5.2%"
    """
    emoji = get_emoji_for_change(change_pct)
    sign = "+" if change_pct > 0 else ""
    return f"Rs. {price:.2f} {emoji} {sign}{change_pct:.2f}%"


def get_verdict_color(verdict: str) -> tuple:
    """
    Get color and emoji for pump detector verdict.
    Returns: (color_hex, emoji, text_color)
    """
    verdicts = {
        "LIKELY PUMP": ("#FF4444", "🔴", "#FFFFFF"),
        "SUSPICIOUS": ("#FF9900", "🟡", "#FFFFFF"),
        "LOOKS LEGIT": ("#00AA44", "🟢", "#FFFFFF"),
    }
    return verdicts.get(verdict, ("#999999", "⚪", "#FFFFFF"))


def format_announcement_date(date_str: str) -> str:
    """
    Format announcement date for display.
    """
    if not date_str:
        return "N/A"
    # Simple formatting - can be enhanced with date parsing
    return date_str[:10] if len(date_str) >= 10 else date_str


def format_market_summary(aspi: float, aspi_change: float, sl20: float, sl20_change: float) -> str:
    """
    Format market summary for display.
    Returns HTML string.
    """
    aspi_emoji = get_emoji_for_change(aspi_change)
    sl20_emoji = get_emoji_for_change(sl20_change)
    
    return f"""
    <div style="display: flex; gap: 30px; font-size: 18px;">
        <div>
            <strong>ASPI</strong><br/>
            {aspi:,.2f} {aspi_emoji} {aspi_change:+.2f}%
        </div>
        <div>
            <strong>S&P SL20</strong><br/>
            {sl20:,.2f} {sl20_emoji} {sl20_change:+.2f}%
        </div>
    </div>
    """


def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Truncate text and add ellipsis if too long.
    """
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text
