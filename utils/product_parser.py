import pandas as pd
import re

# List of known product keywords (this can grow dynamically)
PRODUCT_KEYWORDS = [
    "iPhone", "Galaxy S23", "Pixel 8", "MacBook Pro", "AirPods Pro", "Sony WH-1000XM5",
    "OnePlus 12", "Samsung Fold", "Nothing Phone", "iPad Pro", "Apple Watch Ultra",
    "DJI Pocket", "GoPro", "Razer Blade", "Dell XPS", "Lenovo Legion", "ASUS ROG", "PS5"
]

# Load latest MKBHD data (fetched videos)
def extract_products():
    df = pd.read_csv("mkbhd_data.csv")

    products = {}

    for idx, row in df.iterrows():
        transcript = row.get("transcript", "")
        if not isinstance(transcript, str):
            continue
        
        # Check for product mentions
        for product in PRODUCT_KEYWORDS:
            if re.search(rf"\b{re.escape(product)}\b", transcript, re.IGNORECASE):
                if product not in products:
                    products[product] = {
                        "product_name": product,
                        "url": row["url"],
                        "description": f"Mentioned in: {row['title']}",
                        "price": "N/A (price can be enhanced later)"
                    }

    # Convert to DataFrame and Save
    product_list = list(products.values())
    product_df = pd.DataFrame(product_list)

    product_df.to_csv("mkbhd_product_list.csv", index=False)
    print(f"✅ Extracted {len(product_list)} product mentions — Saved to `mkbhd_product_list.csv`")

if __name__ == "__main__":
    extract_products()
