import subprocess

subprocess.run(["python3", "utils/data_fetcher.py"])
subprocess.run(["python3", "utils/product_parser.py"])
subprocess.run(["streamlit", "run", "app.py"])