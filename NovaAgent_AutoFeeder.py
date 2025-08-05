import os
import sys
import logging
from datetime import datetime
from scraper_hub import run_all_scrapers  # this should be the main interface running all 50 scrapers

# === Logging Setup ===
LOG_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "NovaBargains", "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

log_filename = datetime.now().strftime("feeder_%Y-%m-%d_%H-%M-%S.log")
log_path = os.path.join(LOG_DIR, log_filename)

logging.basicConfig(
    filename=log_path,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def log_and_print(msg, level="info"):
    getattr(logging, level)(msg)
    print(f"[{level.upper()}] {msg}")

# === Main Logic ===
try:
    log_and_print("NovaAgent_AutoFeeder started.")
    run_all_scrapers()
    log_and_print("All scrapers executed successfully.")
except Exception as e:
    log_and_print(f"Error occurred: {str(e)}", level="error")
    sys.exit(1)
