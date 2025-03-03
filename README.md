
# Creator AI Bot Platform (MKBHD Demo)

This is a fully packaged pipeline to fetch creator data, process product mentions, and power a personalized AI recommendation bot using Gemini Pro.

## 📦 Folder Structure
```
creator_ai_bot/
├── README.md                # This file
├── app.py                    # Streamlit UI
├── mkbhd_data.csv            # Pre-collected data (replace with fresh data if needed)
├── mkbhd_product_list.csv    # Pre-extracted products
├── creators/                 
│   └── mkbhd/                 
│       └── config.json        # MKBHD's personalized style config
├── utils/                     
│   ├── data_fetcher.py       # Fetches YouTube/Instagram/Twitter data
│   ├── product_parser.py     # Extracts product mentions from transcripts
│   └── gemini_handler.py     # Handles Gemini Pro API calls
├── .streamlit/
│   └── secrets.toml          # Stores API key for Streamlit Cloud
```

## 🚀 How It Works
1. Run `data_fetcher.py` to grab latest content.
2. Run `product_parser.py` to update `product_list.csv`.
3. Start the bot with `streamlit run app.py`.

## 💡 Customize for Other Creators
- Add new folder under `/creators/` (e.g., `/creators/linustechtips`).
- Fill `config.json` with their greeting, catchphrases, and tone.
- Fetch their data via `data_fetcher.py`.
- Done — you have a new bot.

## 🔑 API Key Setup
Create `.streamlit/secrets.toml` with:
GEMINI_API_KEY="your-api-key-here"

## 🌐 Deploy on Streamlit Cloud
1. Push to GitHub.
2. Connect to Streamlit Cloud.
3. Set your secrets in the Streamlit Cloud dashboard.
4. Your bot is live.
