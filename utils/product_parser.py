import pandas as pd
import re

PRODUCT_KEYWORDS = [
    "iPhone", "Pixel", "Galaxy", "MacBook", "AirPods", "OnePlus", 
    "Sony", "DJI", "Nothing Phone", "Apple Watch", "Razer Blade", "GoPro"
]

def extract_products():
    df = pd.read_csv("mkbhd_data.csv")
    products = []

    for _, row in df.iterrows():
        transcript = row.get("transcript", "")
        for product in PRODUCT_KEYWORDS:
            if product.lower() in transcript.lower():
                products.append({
                    "product_name": product,
                    "url": row["url"],
                    "description": f"Mentioned in: {row['title']}",
                    "price": "N/A"
                })

    pd.DataFrame(products).to_csv("mkbhd_product_list.csv", index=False)
    print("✅ Extracted & saved product list to `mkbhd_product_list.csv`")

if __name__ == "__main__":
    extract_products()
