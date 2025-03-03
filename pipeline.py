import subprocess
import os

# Always run this from project root (same level as app.py)

def run_command(command):
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        raise Exception(f"❌ Command failed: {command}")

print("🚀 Running Full Pipeline...")

# Step 1 - Fetch latest data (save to root)
run_command("python3 utils/data_fetcher.py")

# Step 2 - Extract products (also works in root)
run_command("python3 utils/product_parser.py")

# Step 3 - Launch Streamlit App
run_command("streamlit run app.py")

print("✅ Pipeline Completed")
