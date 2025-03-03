import streamlit as st
import pandas as pd
import json
from utils.gemini_handler import ask_mkbhd
from utils.product_parser import extract_products

products = pd.read_csv("mkbhd_product_list.csv").to_dict(orient="records")

with open("creators/mkbhd/config.json", "r") as f:
    mkbhd_config = json.load(f)

st.set_page_config(page_title="MKBHD Bot", page_icon="📱")
st.title("Yo what’s up guys — MKBHD Bot")

use_flash = st.toggle("Use Fast Mode (Gemini 1.5 Flash)", value=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

query = st.chat_input("Ask MKBHD something...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    response = ask_mkbhd(query, products, mkbhd_config, use_flash=use_flash)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
