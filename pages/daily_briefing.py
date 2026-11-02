"""
Daily Market Briefing Page
Shows today's top gainers, losers, most active stocks, and AI-generated narrative
"""

import streamlit as st
from data import cse_api
from ai import groq_client
from utils import formatters


def show_daily_briefing():
    """Main daily briefing page function"""
    st.title("📊 Daily Market Briefing")
    
    # Refresh button
    col1, col2 = st.columns([10, 1])
    with col1:
        st.write("Last updated: today (refresh to get latest data)")
    with col2:
        if st.button("🔄 Refresh", key="refresh_briefing"):
            st.cache_data.clear()
            st.rerun()
    
    st.divider()
    
    # Fetch market data
    with st.spinner("Loading market data..."):
        gainers = cse_api.get_top_gainers()
        losers = cse_api.get_top_losers()
        most_active = cse_api.get_most_active_stocks()
        market_summary = cse_api.get_daily_market_summary()
        announcements = cse_api.get_approved_announcements()
    
    # Market Summary Bar
    if market_summary:
        aspi = market_summary.get("aspi", 0)
        aspi_change = market_summary.get("aspichange", 0)
        sl20 = market_summary.get("sl20", 0)
        sl20_change = market_summary.get("sl20change", 0)
        
        col1, col2 = st.columns(2)
        
        with col1:
            emoji_aspi = formatters.get_emoji_for_change(float(aspi_change))
            st.metric(
                "ASPI",
                f"{aspi:,.2f}",
                f"{aspi_change:+.2f}%"
            )
        
        with col2:
            emoji_sl20 = formatters.get_emoji_for_change(float(sl20_change))
            st.metric(
                "S&P SL20",
                f"{sl20:,.2f}",
                f"{sl20_change:+.2f}%"
            )
    
    st.divider()
    
    # Three columns: Gainers, Losers, Most Active
    col1, col2, col3 = st.columns(3)
    
    # Top Gainers
    with col1:
        st.subheader("🟢 Top Gainers")
        if gainers:
            for stock in gainers[:5]:
                name = formatters.truncate_text(stock.get("name", "N/A"), 25)
                price = stock.get("lastTradedPrice", 0)
                change = stock.get("changePercentage", 0)
                
                st.markdown(f"""
                <div style="padding: 10px; background: #f0f8f0; border-radius: 5px; margin: 5px 0;">
                    <strong>{name}</strong><br/>
                    Rs. {price:.2f} <span style="color: #00AA44;">🟢 +{change:.2f}%</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No data available")
    
    # Top Losers
    with col2:
        st.subheader("🔴 Top Losers")
        if losers:
            for stock in losers[:5]:
                name = formatters.truncate_text(stock.get("name", "N/A"), 25)
                price = stock.get("lastTradedPrice", 0)
                change = stock.get("changePercentage", 0)
                
                st.markdown(f"""
                <div style="padding: 10px; background: #f8f0f0; border-radius: 5px; margin: 5px 0;">
                    <strong>{name}</strong><br/>
                    Rs. {price:.2f} <span style="color: #FF4444;">🔴 {change:.2f}%</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No data available")
    
    # Most Active
    with col3:
        st.subheader("📈 Most Active")
        if most_active:
            for stock in most_active[:5]:
                name = formatters.truncate_text(stock.get("name", "N/A"), 25)
                volume = stock.get("totalVolume", 0)
                volume_str = formatters.format_volume(int(volume))
                
                st.markdown(f"""
                <div style="padding: 10px; background: #f0f0f8; border-radius: 5px; margin: 5px 0;">
                    <strong>{name}</strong><br/>
                    Volume: {volume_str}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No data available")
    
    st.divider()
    
    # AI-Generated Briefing
    st.subheader("📝 AI Market Narrative")
    
    if groq_client.is_ai_configured():
        with st.spinner("Generating AI briefing..."):
            briefing_text = groq_client.generate_briefing(
                gainers[:5],
                losers[:5],
                most_active[:5],
                market_summary,
                announcements
            )
        
        st.markdown(f"""
        <div style="padding: 20px; background: #f9f9f9; border-left: 4px solid #0F4C35; border-radius: 5px;">
            {briefing_text}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning(
            "AI briefing not available. "
            "Please add GROQ_API_KEY to .env file to enable AI analysis."
        )
    
    st.divider()
    
    # Recent Announcements
    st.subheader("📣 Recent Company Announcements")
    
    if announcements:
        with st.expander("View announcements", expanded=True):
            for ann in announcements[:10]:
                subject = ann.get("subject", "N/A")
                symbol = ann.get("symbol", "N/A")
                date = ann.get("date", "N/A")
                
                st.markdown(f"""
                <div style="padding: 10px; background: #f9f9f9; border-radius: 5px; margin: 8px 0;">
                    <strong>{symbol}</strong> - {date}<br/>
                    {subject}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No announcements available")
    
    st.divider()
    
    # Disclaimer
    st.markdown("""
    **Disclaimer:** This tool is for educational purposes only. 
    It does not constitute financial advice. Always do your own research before making investment decisions. 
    Past market data does not guarantee future performance.
    """)


if __name__ == "__main__":
    show_daily_briefing()
