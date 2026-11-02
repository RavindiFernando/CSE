# How to Run CSE Investor App

## Step 1: Get a Groq API Key (2 minutes)
1. Go to https://console.groq.com/keys
2. Sign in with Google or GitHub (free account)
3. Click **"Create API Key"**
4. Copy your key (starts with `gsk_...`)

## Step 2: Add Key to .env
```bash
# In CSE-project directory
echo "GROQ_API_KEY=gsk_YOUR_KEY_HERE" > .env
```

Or open `.env` in your editor and paste:
```
GROQ_API_KEY=gsk_your_actual_key_here
```

## Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 4: Run the App
```bash
streamlit run app.py
```

The app opens at: **http://localhost:8501**

---

## What to Try First

### Daily Briefing Tab
- Click "Daily Briefing" in the sidebar
- Click the refresh button to see today's top gainers, losers, and market mood

### Pump Detector Tab
- Click "Pump Detector" in the sidebar
- Try one of the popular symbols: **DIAL.N0000** or **LOLC.N0000**
- Click "Analyze Stock"

---

## Troubleshooting

| Problem | Solution |
|---|---|
| "Groq API key not configured" | Check `.env` file has `GROQ_API_KEY=gsk_...` (no spaces) |
| "No module named streamlit" | Run `pip install -r requirements.txt` |
| "Stock not found" | Market may be closed (9:30am–2:30pm weekdays Sri Lankan time). Try again during trading hours. |
| No data showing | CSE API is slow. Wait 10 seconds and refresh. |

---

## Deployment (Optional)

To share with others on Streamlit Cloud:

1. Push to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub repo, select `app.py`
4. Add `GROQ_API_KEY` in Settings → Secrets
5. Done! Share the URL

