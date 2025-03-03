import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY is missing!")

genai.configure(api_key=GEMINI_API_KEY)

def ask_mkbhd(query, products, config, use_flash=True):
    product_text = "\n".join([
        f"- {p['product_name']} (${p['price']}): {p['description']}"
        for p in products
    ])

    prompt = f"""
You are {config['name']}, a legendary tech reviewer known for your {config['tone']}.

You often greet people by saying: "{config['greeting']}"
You frequently use phrases like: {', '.join(config['catchphrases'])}

User asked: "{query}"

Here are relevant products:
{product_text}

Answer in your signature style.
"""

    model = genai.GenerativeModel("gemini-1.5-flash" if use_flash else "gemini-1.5-pro")
    return model.generate_content(prompt).text.strip()
