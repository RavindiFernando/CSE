"""
CSE Investor Web App - Main Entry Point
Streamlit multi-page app for Colombo Stock Exchange analysis
"""

import streamlit as st
from pages import pump_detector, daily_briefing

# Configure page
st.set_page_config(
    page_title="CSE Investor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    :root {
        --primary-color: #0F4C35;
        --secondary-color: #1e7e34;
    }
    
    .main {
        padding-top: 2rem;
    }
    
    h1 {
        color: #0F4C35;
        border-bottom: 3px solid #0F4C35;
        padding-bottom: 0.5rem;
    }
    
    h2 {
        color: #0F4C35;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "selected_page" not in st.session_state:
    st.session_state.selected_page = "📊 Daily Briefing"
if "selected_symbol" not in st.session_state:
    st.session_state.selected_symbol = ""

# Sidebar Navigation
with st.sidebar:
    st.markdown("# 📈 CSE Investor")
    st.markdown("### Colombo Stock Exchange Analysis Tool")
    st.divider()
    
    st.markdown("""
    **Two key features:**
    1. 🔍 Detect pump-and-dump schemes
    2. 📊 Daily market briefing with AI analysis
    
    Powered by real-time CSE data + Groq AI
    """)
    
    st.divider()
    
    # Page selector
    page = st.radio(
        "📑 Select Feature",
        ["📊 Daily Briefing", "🔍 Pump Detector"],
        index=0
    )
    
    st.session_state.selected_page = page
    
    st.divider()
    
    # About section
    st.markdown("""
    ### ℹ️ About This App
    
    **Free tools for Sri Lankan retail investors**
    
    - **Data:** Live CSE market data + 30-day history
    - **AI:** Llama 3.3 70B via Groq (free tier)
    - **Made with:** Streamlit + Python
    
    ### 📚 Popular Symbols
    - DIAL.N0000 — Dialog Axiata
    - LOLC.N0000 — LOLC Holdings
    - COMB.N0000 — Commercial Bank
    - JKH.N0000 — John Keells Holdings
    - HNB.N0000 — Hatton National Bank
    
    ### ⚠️ Disclaimer
    For educational purposes only. Not financial advice. 
    Always do your own research before investing.
    """)
    
    st.divider()
    st.markdown("**Version:** 1.0 | **Made with ❤️**")


# Main content area
if st.session_state.selected_page == "📊 Daily Briefing":
    daily_briefing.show_daily_briefing()
elif st.session_state.selected_page == "🔍 Pump Detector":
    pump_detector.show_pump_detector()

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666;">
    <p><strong>Disclaimer:</strong> This tool is for educational purposes only. It does not constitute financial advice. 
    Always do your own research before making investment decisions. Past performance does not guarantee future results.</p>
    <p style="font-size: 12px; margin-top: 10px;">
        CSE Investor App | Built for Sri Lankan retail investors | 
        <a href="https://www.cse.lk/" target="_blank">CSE Official</a>
    </p>
</div>
""", unsafe_allow_html=True)
