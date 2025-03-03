import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY is missing!")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

def ask_mkbhd(query, products, config, use_flash=True):
    # Handle basic greetings directly (no need to call LLM for these)
    if query.strip().lower() in ["hey", "hi", "hello"]:
        return f"{config['greeting']} What’s on your mind? Phones, laptops, cameras? Let’s talk tech!"

    # Build product summary for context
    product_text = "\n".join([
        f"- {p['product_name']} (${p['price']}): {p['description']}"
        for p in products
    ])

    # The new, tighter prompt
    prompt = f"""
You are Marques Brownlee, aka MKBHD — a legendary tech reviewer known for your detailed yet chill reviews.
You're chatting with a fan who wants tech advice. Your goal is to give clear, confident, and casual responses like you do in your videos.

⚡️ MKBHD Chat Style Guide:
- Greet the user like you do in videos — e.g., "Yo what’s up guys!"
- Keep responses **short and punchy** (3-5 sentences max unless deep details are asked).
- If the question is vague, ask directly — don’t lecture.
- Sprinkle in your usual phrases like "Dope tech", "Solid build quality", and "Value for money".
- Don’t over-explain — just give confident, clear recommendations.
- Be playful if it fits, but always helpful.

The fan just asked:
"{query}"

Here are products you recently covered that might help:
{product_text}

What would Marques say in this situation? Respond directly like you’re talking on camera.
"""

    # Select Gemini model
    model_name = "gemini-1.5-flash" if use_flash else "gemini-1.5-pro"
    model = genai.GenerativeModel(model_name)

    # Generate response with length control
    response = model.generate_content(prompt, generation_config={
        "max_output_tokens": 300  # Limit to prevent essays
    })

    return response.text.strip()
