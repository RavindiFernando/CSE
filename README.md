# 📈 CSE Investor Web App

A free Streamlit web application for Sri Lankan retail investors using the Colombo Stock Exchange (CSE). Detect pump-and-dump schemes and get daily AI-powered market briefings.

## ✨ Features

### 🔍 Pump Detector
Analyze any CSE stock for pump-and-dump patterns:
- **Price & Volume Analysis** — Detects anomalies using 30-day historical data
- **AI Verdict** — Groq AI (Llama 3.3) evaluates risk level: `LIKELY PUMP`, `SUSPICIOUS`, or `LOOKS LEGIT`
- **Red Flags & Green Flags** — Specific concerns and positive indicators
- **Visual Charts** — 30-day price and volume trends
- **Company Announcements** — Recent official CSE announcements

### 📊 Daily Market Briefing
Stay informed about the CSE market:
- **Live Indices** — ASPI and S&P SL20 real-time data
- **Market Leaders** — Top gainers, losers, and most active stocks
- **AI Narrative** — AI-generated briefing explaining what happened and why
- **Recent Announcements** — Latest company news and updates
- **Refresh on Demand** — Get latest data anytime

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Free Groq API Key (2 minutes)
1. Go to https://console.groq.com/keys
2. Sign in (Google or GitHub account works)
3. Click "Create API Key"
4. Copy your key (starts with `gsk_...`)

### 3. Configure Environment
```bash
cp .env.example .env
# Open .env and paste your Groq API key
```

### 4. Run the App
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📁 Project Structure

```
cse-investor-app/
├── app.py                    # Main Streamlit entry point
├── pages/
│   ├── pump_detector.py      # Pump-and-dump analysis feature
│   └── daily_briefing.py     # Daily market briefing feature
├── data/
│   ├── cse_api.py            # CSE API integration
│   ├── yfinance_data.py      # 30-day historical data
│   └── anomaly.py            # Volume spike detection
├── ai/
│   └── groq_client.py        # Groq AI calls
├── utils/
│   └── formatters.py         # Number formatting & colors
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

## 📊 Data Sources

### CSE Direct API
- **Endpoint:** `https://www.cse.lk/api/`
- **Data:** Real-time price, volume, market indices, announcements
- **No API key needed** — Uses public CSE website API

### Yahoo Finance
- **Data:** 30-day historical price and volume
- **Purpose:** Baseline volume calculation for pump detection
- **CSE symbols use `.CM` suffix** — DIAL.N0000 → DIAL.CM

### Groq AI
- **Model:** llama-3.3-70b-versatile (free tier)
- **Free limits:** see https://console.groq.com/settings/limits
- **No credit card needed**

## 📝 Popular CSE Symbols

| Symbol | Company |
|--------|---------|
| DIAL.N0000 | Dialog Axiata |
| LOLC.N0000 | LOLC Holdings |
| COMB.N0000 | Commercial Bank |
| JKH.N0000 | John Keells Holdings |
| HNB.N0000 | Hatton National Bank |
| SAMP.N0000 | Sampath Bank |
| CTC.N0000 | Ceylon Tobacco |
| LION.N0000 | Lion Brewery |
| HEMS.N0000 | Hemas Holdings |
| EAST.N0000 | Eastern Plantations |

## 🎯 How Pump Detection Works

The app looks for these warning signs:

1. **Volume Spike > 3x** without official announcement → HIGH RISK
2. **Price rise > 10%** with volume spike but no news → HIGH RISK
3. **Vague tip message language** ("guaranteed", "insider info") → RISK
4. **Thinly traded stock** (low average volume) → High vulnerability

The AI combines these signals with recent company announcements to give a final verdict.

## 🚨 How the App Uses Data

### Pump Detector Flow
1. User enters stock symbol
2. Fetch live CSE data (current price, volume, announcements)
3. Fetch 30-day historical data from Yahoo Finance
4. Calculate volume spike ratio and price momentum
5. Send to Groq AI with all data
6. Display verdict with red flags, green flags, and AI explanation

### Daily Briefing Flow
1. Fetch today's top gainers, losers, most active stocks
2. Fetch market indices (ASPI, SL20)
3. Fetch recent company announcements
4. Send to Groq AI to generate narrative
5. Display briefing with all data

## ⚙️ Configuration

### Environment Variables
Create a `.env` file (copy from `.env.example`):
```
GROQ_API_KEY=gsk_...your_key_here...
```

### Streamlit Cache Settings
- **Daily Briefing data:** Cached for 5 minutes
- **Historical price data:** Cached for 1 hour
- **AI responses:** Never cached (always fresh analysis)

## 🌐 Deployment

### Deploy to Streamlit Cloud (Free)

1. Push code to public GitHub repo
2. Go to https://share.streamlit.io
3. Connect GitHub repo → select `app.py`
4. Add `GROQ_API_KEY` in Settings → Secrets
5. Deploy — get shareable URL

**Example URL:** `https://cse-pump-detector.streamlit.app`

Share this URL with friends and family — they can use it directly without installing anything!

## 🛡️ Error Handling

| Error | Message | Solution |
|-------|---------|----------|
| CSE API 403 | Market data unavailable | Market may be closed (9:30am-2:30pm weekdays) |
| Invalid symbol | Invalid CSE symbol format | Use format like DIAL.N0000 |
| No historical data | Data not available on Yahoo | App uses today's data only (less accurate) |
| Groq rate limit | AI temporarily unavailable | Wait 1 minute and retry |
| No API key | Groq not configured | Add GROQ_API_KEY to .env |

## ⚠️ Disclaimer

**This tool is for educational purposes only.**

- ❌ Not financial advice
- ❌ Do not use as sole investment decision factor
- ❌ Past patterns ≠ future performance
- ✅ Always do your own research
- ✅ Consult professional financial advisor
- ✅ Invest responsibly

## 🤝 Contributing

Found a bug? Have suggestions?
- Report issues with specific CSE symbols
- Suggest improvements to pump detection logic
- Share feedback about UI/UX

## 📞 Support

For issues:
1. Check if CSE market is open (9:30am-2:30pm Sri Lankan time, weekdays)
2. Verify your Groq API key is valid
3. Check your internet connection
4. Try refreshing the data (Refresh button in app)

## 📜 License

This project is provided as-is for educational purposes.

## 🙏 Acknowledgments

- **CSE:** For public API access
- **Yahoo Finance:** Historical data via yfinance
- **Groq:** Free AI inference tier
- **Streamlit:** Simple web framework

---

**Made with ❤️ for Sri Lankan retail investors**

Happy investing! 📈
