import streamlit as st
import pandas as pd
import json
import os

from utils.gemini_handler import ask_mkbhd
from utils.data_fetcher import fetch_latest_videos
from utils.product_parser import extract_products

# Setup page
st.set_page_config(page_title="MKBHD Bot", page_icon="📱")
st.title("Yo what’s up guys — MKBHD Bot")

# Helper function to ensure products are ready
def ensure_products_available():
    if not os.path.exists("mkbhd_data.csv") or not os.path.exists("mkbhd_product_list.csv"):
        st.warning("🔄 Product data missing. Click the button below to fetch the latest data.")
        if st.button("Fetch Latest Data"):
            fetch_latest_videos()
            extract_products()
            st.success("✅ Data fetched and processed! You can start chatting now.")
            st.rerun()
        st.stop()

# Check if product list exists
ensure_products_available()

# Load products (now guaranteed to exist)
products = pd.read_csv("mkbhd_product_list.csv").to_dict(orient="records")

# Load creator config
with open("creators/mkbhd/config.json", "r") as f:
    mkbhd_config = json.load(f)

# UI toggle
use_flash = st.toggle("Use Fast Mode (Gemini 1.5 Flash)", value=True)

# Conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Replay history
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

# Chat input
query = st.chat_input("Ask MKBHD something...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    response = ask_mkbhd(query, products, mkbhd_config, use_flash=use_flash)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
