"""
Pump Detector Page
Analyzes stocks for pump-and-dump schemes using price, volume, and AI analysis
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data import cse_api, yfinance_data, anomaly
from ai import groq_client
from utils import formatters


def show_pump_detector():
    """Main pump detector page function"""
    st.title("🔍 Pump Detector")
    st.write("Analyze a stock for pump-and-dump patterns using price, volume, and AI analysis.")
    
    # Popular symbols suggestion
    st.subheader("Quick Start")
    popular_symbols = [
        "DIAL.N0000", "LOLC.N0000", "COMB.N0000", "JKH.N0000", "HNB.N0000",
        "SAMP.N0000", "CTC.N0000", "LION.N0000", "HEMS.N0000", "EAST.N0000"
    ]
    
    cols = st.columns(5)
    for i, symbol in enumerate(popular_symbols[:5]):
        if cols[i].button(symbol, key=f"sym1_{i}"):
            st.session_state.selected_symbol = symbol
    
    cols = st.columns(5)
    for i, symbol in enumerate(popular_symbols[5:10]):
        if cols[i].button(symbol, key=f"sym2_{i}"):
            st.session_state.selected_symbol = symbol
    
    st.divider()
    
    # Input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        symbol_input = st.text_input(
            "Enter CSE stock symbol",
            value=st.session_state.get("selected_symbol", ""),
            placeholder="e.g. DIAL.N0000",
            key="symbol_input"
        )
    
    tip_message = st.text_area(
        "Paste the tip message you received (optional)",
        placeholder="e.g., WhatsApp message about a stock...",
        key="tip_message"
    )
    
    # Validate and analyze
    if st.button("🔍 Analyze Stock", type="primary"):
        if not symbol_input:
            st.error("Please enter a stock symbol")
        elif not cse_api.validate_symbol_format(symbol_input.upper()):
            st.error("Invalid CSE symbol format. Use format like: DIAL.N0000")
        else:
            analyze_stock(symbol_input.upper(), tip_message)


def analyze_stock(symbol: str, tip_message: str = ""):
    """Perform complete pump analysis"""
    
    st.session_state.selected_symbol = symbol
    
    with st.spinner("Fetching market data..."):
        # Get company info
        company_info = cse_api.get_company_info(symbol)
        
        if not company_info or not company_info.get("symbol"):
            st.error(
                "Stock not found. CSE market may be closed (trading: 9:30am–2:30pm weekdays) "
                "or the symbol may be invalid. Try again during market hours."
            )
            return
        
        # Extract company data
        company_name = company_info.get("name", "Unknown")
        current_price = float(company_info.get("lastTradedPrice", 0) or 0)
        price_change = float(company_info.get("change", 0) or 0)
        price_change_pct = float(company_info.get("changePercentage", 0) or 0)
        today_volume = int(company_info.get("totalVolume", 0) or 0)
        market_cap = company_info.get("marketCap", "N/A")
        pe_ratio = company_info.get("peRatio", "N/A")
        
        # Get historical data
        history_df = yfinance_data.get_price_volume_history(symbol)
        
        # Calculate anomalies
        volume_spike = anomaly.calculate_volume_spike(history_df, today_volume)
        price_momentum = anomaly.calculate_price_momentum(history_df)
        
        # Get announcements
        announcements = cse_api.get_announcements_for_symbol(symbol)
        announcement_subjects = [a.get("subject", "") for a in announcements]
        
        # Check if we have historical data
        has_history = not history_df.empty and len(history_df) >= 5
        if not has_history:
            st.warning(
                "⚠️ 30-day historical data not available for this stock. "
                "Volume spike detection will be less accurate."
            )

        # Perform pump analysis with AI
        pump_result = None
        if groq_client.is_ai_configured():
            with st.spinner("Running AI analysis..."):
                # Use actual values if available, otherwise use 0 and note in prompt
                avg_30d_volume = volume_spike.get("avg_volume") or 0
                volume_spike_ratio = volume_spike.get("spike_ratio") or 0

                pump_result = groq_client.analyze_pump(
                    symbol=symbol,
                    company_name=company_name,
                    current_price=current_price,
                    price_change_pct=price_change_pct,
                    today_volume=today_volume,
                    avg_30d_volume=float(avg_30d_volume) if avg_30d_volume else 0,
                    volume_spike_ratio=float(volume_spike_ratio) if volume_spike_ratio else 0,
                    recent_announcements=announcement_subjects[:5],
                    tip_message=tip_message,
                    has_history=has_history
                )
        
        # Display results
        display_analysis_results(
            symbol, company_name, company_info,
            volume_spike, price_momentum,
            history_df, pump_result,
            announcements, tip_message
        )


def display_analysis_results(
    symbol: str, company_name: str, company_info: dict,
    volume_spike: dict, price_momentum: dict,
    history_df, pump_result: dict,
    announcements: list, tip_message: str
):
    """Display the analysis results"""
    
    st.divider()
    
    # Verdict Banner
    if pump_result and pump_result.get("verdict") not in ["ERROR", "RATE_LIMITED", "PARSE_ERROR"]:
        verdict = pump_result.get("verdict", "UNKNOWN")
        confidence = pump_result.get("confidence", "N/A")
        
        color, emoji, text_color = formatters.get_verdict_color(verdict)
        
        st.markdown(f"""
        <div style="background:{color};padding:30px;border-radius:10px;text-align:center;margin:20px 0;">
            <h2 style="color:{text_color};margin:0">{emoji} {verdict}</h2>
            <p style="color:{text_color};margin:10px 0;font-size:18px">Confidence: {confidence}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main Info Columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📌 Stock Info")
        st.metric("Price", f"Rs. {company_info.get('lastTradedPrice', 0):.2f}")
        st.metric("Change", f"{company_info.get('changePercentage', 0):+.2f}%")
        if company_info.get("marketCap") and company_info.get("marketCap") != "N/A":
            st.metric("Market Cap", company_info.get("marketCap"))
        if company_info.get("peRatio") and company_info.get("peRatio") != "N/A":
            st.metric("P/E Ratio", company_info.get("peRatio"))
    
    with col2:
        st.subheader("📊 Volume Analysis")
        avg_vol = volume_spike.get("avg_volume", 0)
        today_vol = volume_spike.get("today_volume", 0)
        spike_ratio = volume_spike.get("spike_ratio", 0)
        severity = volume_spike.get("severity", "NORMAL")
        
        st.metric("Today's Volume", formatters.format_volume(today_vol))
        st.metric("30d Avg Volume", formatters.format_volume(avg_vol))
        
        # Volume spike gauge
        if spike_ratio is not None:
            color_map = {
                "EXTREME": "#FF0000",
                "HIGH": "#FF9900",
                "MODERATE": "#FFCC00",
                "NORMAL": "#00AA44",
                "unknown": "#999999"
            }
            color = color_map.get(severity, "#999999")
            st.markdown(f"""
            <div style="padding:10px;background:{color};color:white;border-radius:5px;text-align:center;">
                <strong>Volume Spike: {spike_ratio:.1f}x normal ({severity})</strong>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        st.subheader("📈 Price Momentum")
        if price_momentum:
            st.metric("1-Week Change", f"{price_momentum.get('week_change_pct', 0):+.2f}%")
            st.metric("1-Month Change", f"{price_momentum.get('month_change_pct', 0):+.2f}%")
            st.metric("52-Week High", f"Rs. {company_info.get('fiftyTwoWeekHigh', 'N/A')}")
            st.metric("52-Week Low", f"Rs. {company_info.get('fiftyTwoWeekLow', 'N/A')}")
    
    st.divider()
    
    # Red Flags and Green Flags
    if pump_result and pump_result.get("verdict") not in ["ERROR", "RATE_LIMITED", "PARSE_ERROR"]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🚩 Red Flags")
            red_flags = pump_result.get("red_flags", [])
            if red_flags:
                for flag in red_flags:
                    st.warning(f"• {flag}")
            else:
                st.success("No major red flags detected")
        
        with col2:
            st.subheader("✅ Green Flags")
            green_flags = pump_result.get("green_flags", [])
            if green_flags:
                for flag in green_flags:
                    st.success(f"• {flag}")
            else:
                st.info("Limited positive indicators")
        
        st.divider()
        
        # AI Explanation
        st.subheader("💬 Analysis Explanation")
        explanation = pump_result.get("explanation", "No explanation available")
        st.markdown(f"> {explanation}")
        
        # Advice
        advice = pump_result.get("advice", "")
        if advice:
            st.info(f"💡 {advice}")
    
    st.divider()
    
    # Price and Volume Chart
    if not history_df.empty:
        st.subheader("📈 30-Day Price & Volume Chart")
        
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            row_heights=[0.7, 0.3],
            specs=[[{"secondary_y": False}], [{"secondary_y": False}]]
        )
        
        # Price line
        fig.add_trace(
            go.Scatter(
                x=history_df.index,
                y=history_df["Close"],
                mode="lines",
                name="Price (Rs.)",
                line=dict(color="#0F4C35", width=2)
            ),
            row=1, col=1
        )
        
        # Volume bars
        fig.add_trace(
            go.Bar(
                x=history_df.index,
                y=history_df["Volume"],
                name="Volume",
                marker=dict(color="#B0B0B0"),
                opacity=0.6
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            height=500,
            hovermode="x unified",
            template="plotly_white"
        )
        
        fig.update_yaxes(title_text="Price (Rs.)", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)
        fig.update_xaxes(title_text="Date", row=2, col=1)
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Recent Announcements
    st.subheader("📣 Recent Announcements for this Stock")
    
    if announcements:
        for ann in announcements[:5]:
            subject = ann.get("subject", "N/A")
            date = ann.get("date", "N/A")
            
            st.markdown(f"""
            <div style="padding:15px;background:#f9f9f9;border-left:4px solid #0F4C35;border-radius:5px;margin:10px 0;">
                <strong>{date}</strong><br/>
                {subject}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recent announcements found for this stock")
    
    st.divider()
    
    # Disclaimer
    st.markdown("""
    ⚠️ **DISCLAIMER**
    
    This tool is for **educational purposes only**. It does not constitute financial advice. 
    Always do your own research before making investment decisions. 
    Past volume patterns and price movements do not guarantee future performance.
    
    Invest responsibly and consult a professional financial advisor if needed.
    """)


if __name__ == "__main__":
    show_pump_detector()
