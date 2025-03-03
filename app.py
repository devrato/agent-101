import streamlit as st
import pandas as pd
import json
from utils.gemini_handler import ask_mkbhd
from utils.product_parser import load_products

products = load_products()

with open("creators/mkbhd/config.json", "r") as f:
    mkbhd_config = json.load(f)

st.set_page_config(page_title="MKBHD Bot", page_icon="📱", layout="wide")
st.title("🔴 Yo what’s up guys — MKBHD Bot is here!")
st.caption("Ask me anything about tech — powered by Gemini 1.5")

use_flash = st.toggle("Use Fast Mode (Gemini 1.5 Flash)", value=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

query = st.chat_input("Ask MKBHD something...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.spinner(f"MKBHD (via {'Flash' if use_flash else 'Pro'}) is thinking..."):
        response = ask_mkbhd(query, products, mkbhd_config, use_flash=use_flash)

    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)

    matched_products = [
        p for p in products if any(word.lower() in response.lower() for word in p["product_name"].lower().split())
    ]

    if matched_products:
        st.markdown("### 🔗 Products Mentioned:")
        for product in matched_products:
            st.write(f"**{product['product_name']}**")
            st.write(f"💰 Price: {product.get('price', 'N/A')}")
            st.write(f"🔗 [Buy Now]({product.get('url', '#')})")
            st.write(f"📝 {product.get('description', 'No description')}")
            st.divider()
