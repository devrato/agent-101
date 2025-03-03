import google.generativeai as genai
import os
import streamlit as st

from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Access keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Try loading API key from Streamlit secrets (cloud) or environment (local)
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY is missing. Set it as an environment variable or in secrets.toml.")

genai.configure(api_key=GEMINI_API_KEY)

def ask_mkbhd(query, products, config, use_flash=True):
    product_text = "\n".join([
        f"- {p.get('product_name', 'Unknown Product')} (${p.get('price', 'N/A')}): {p.get('description', 'No description')}" 
        for p in products
    ])

    prompt = f"""
You are {config['name']}, a legendary tech reviewer known for your {config['tone']}.

You often greet people by saying: "{config['greeting']}"
You frequently use phrases like: {', '.join(config['catchphrases'])}

User asked: "{query}"

Here are some products you recently reviewed:
{product_text}

Please answer this question in your signature style.
"""

    model_name = "gemini-1.5-flash" if use_flash else "gemini-1.5-pro"

    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)

    return response.text.strip()
