import subprocess
import time
import os
from datetime import datetime

SCRIPT_PATH = os.path.expandvars(r"%USERPROFILE%\Desktop\NovaBargains\NovaAgent_AutoFeeder.py")
LOG_FILE = os.path.expandvars(r"%USERPROFILE%\Desktop\NovaBargains\logs\watchdog.log")
RETRY_LIMIT = 3
WAIT_SECONDS = 60 * 10  # 10 minutes between attempts

def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a", encoding="utf-8") as logf:
        logf.write(f"{timestamp} {message}\n")
    print(f"{timestamp} {message}")

def run_autofeeder():
    try:
        result = subprocess.run(
            ["python", SCRIPT_PATH],
            capture_output=True,
            text=True,
            timeout=300  # 5-minute max runtime
        )
        if result.returncode == 0:
            log("✅ AutoFeeder completed successfully.")
        else:
            log(f"⚠️ AutoFeeder exited with error code {result.returncode}")
            log(f"stderr: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        log("⏰ AutoFeeder timed out.")
        return False
    except Exception as e:
        log(f"❌ AutoFeeder crashed: {e}")
        return False
    return True

def watchdog_loop():
    retry_count = 0
    while retry_count < RETRY_LIMIT:
        success = run_autofeeder()
        if success:
            return
        else:
            retry_count += 1
            log(f"🔁 Retrying in {WAIT_SECONDS//60} minutes... ({retry_count}/{RETRY_LIMIT})")
            time.sleep(WAIT_SECONDS)
    log("🚨 Max retries reached. Manual intervention may be required.")

if __name__ == "__main__":
    watchdog_loop()
