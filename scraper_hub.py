from retry_queue import RetryQueue
import logging

retry_queue = RetryQueue()
retry_queue.start()

import os
import importlib.util

SCRAPER_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "NovaBargains", "scrapers")

def run_all_scrapers():
    for filename in os.listdir(SCRAPER_DIR):
        if filename.endswith(".py") and filename.startswith("scraper_"):
            scraper_path = os.path.join(SCRAPER_DIR, filename)
            spec = importlib.util.spec_from_file_location("module.name", scraper_path)
            scraper_module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(scraper_module)
                if hasattr(scraper_module, "run_scraper"):
                    try:
                        scraper_module.run_scraper()
                    except Exception as e:
                        logging.error(f"{filename} failed: {str(e)}. Adding to retry queue.")
                        retry_queue.add(filename, scraper_module.run_scraper)
            except Exception as e:
                logging.error(f"Failed to load {filename}: {str(e)}")
