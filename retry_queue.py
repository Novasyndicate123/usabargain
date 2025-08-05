import time
import threading
import logging

class RetryQueue:
    def __init__(self, max_retries=3, retry_delay=300):
        """
        max_retries: Maximum retry attempts per scraper (default 3)
        retry_delay: Delay between retries in seconds (default 5 minutes)
        """
        self.queue = []
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = logging.getLogger("RetryQueue")
        self.lock = threading.Lock()
        self.running = False

    def add(self, scraper_name, func):
        with self.lock:
            self.queue.append({
                "scraper_name": scraper_name,
                "func": func,
                "attempts": 0,
            })
            self.logger.info(f"Added {scraper_name} to retry queue.")

    def process(self):
        self.running = True
        while self.running:
            with self.lock:
                if not self.queue:
                    self.logger.info("Retry queue empty. Sleeping 60 seconds.")
                    time.sleep(60)
                    continue
                item = self.queue.pop(0)
            scraper_name = item["scraper_name"]
            func = item["func"]
            attempts = item["attempts"]
            if attempts >= self.max_retries:
                self.logger.warning(f"{scraper_name} reached max retries. Dropping.")
                continue
            try:
                self.logger.info(f"Retrying {scraper_name} attempt {attempts+1}")
                func()
                self.logger.info(f"{scraper_name} succeeded on retry.")
            except Exception as e:
                self.logger.error(f"{scraper_name} retry failed: {str(e)}")
                item["attempts"] += 1
                with self.lock:
                    self.queue.append(item)
            time.sleep(self.retry_delay)

    def start(self):
        thread = threading.Thread(target=self.process, daemon=True)
        thread.start()
