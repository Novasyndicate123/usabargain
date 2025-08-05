import sqlite3
import threading
import time
from datetime import datetime, timedelta

DB_PATH = 'data/bargains.db'

# Task priority weights (example)
TASK_PRIORITIES = {
    'scraper_feed': 10,
    'ai_scoring': 8,
    'affiliate_injection': 6,
    'seo_sitemap': 5,
    'social_auto': 7,
    'analytics_alert': 9
}

class AgentManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.task_status = {}
        self.lock = threading.Lock()
        self.load_task_status()

    def load_task_status(self):
        # Initialize or load from DB if needed
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS task_status (
                    task_name TEXT PRIMARY KEY,
                    last_run TIMESTAMP,
                    success INTEGER,
                    fail_count INTEGER DEFAULT 0
                )
            ''')
            conn.commit()
            c.execute('SELECT task_name, last_run, success, fail_count FROM task_status')
            rows = c.fetchall()
            self.task_status = {row[0]: {'last_run': row[1], 'success': row[2], 'fail_count': row[3]} for row in rows}

    def update_task_status(self, task_name, success=True):
        with self.lock:
            now = datetime.utcnow().isoformat()
            status = self.task_status.get(task_name, {'fail_count':0})
            if success:
                status['last_run'] = now
                status['success'] = 1
                status['fail_count'] = 0
            else:
                status['fail_count'] = status.get('fail_count', 0) + 1
                status['success'] = 0
            self.task_status[task_name] = status
            # Persist
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute('''
                    INSERT INTO task_status (task_name, last_run, success, fail_count)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(task_name) DO UPDATE SET
                    last_run=excluded.last_run,
                    success=excluded.success,
                    fail_count=excluded.fail_count
                ''', (task_name, status.get('last_run'), status['success'], status['fail_count']))
                conn.commit()

    def get_next_task(self):
        # Prioritize tasks by weight, last run, and failure count
        now = datetime.utcnow()
        candidates = []
        for task, priority in TASK_PRIORITIES.items():
            status = self.task_status.get(task)
            last_run = datetime.fromisoformat(status['last_run']) if status and status['last_run'] else None
            fail_count = status['fail_count'] if status else 0

            # Calculate wait penalty: longer since last run => higher priority
            wait_hours = (now - last_run).total_seconds()/3600 if last_run else float('inf')
            penalty = fail_count * 2  # Penalize failed tasks less aggressively to retry soon

            score = priority + wait_hours - penalty
            candidates.append((score, task))

        candidates.sort(reverse=True)
        if candidates:
            return candidates[0][1]
        return None

    def run_task(self, task_name):
        try:
            print(f"[AgentManager] Running task: {task_name}")
            if task_name == 'scraper_feed':
                from NovaAgent_AutoFeeder import main as feeder_main
                feeder_main()
            elif task_name == 'ai_scoring':
                from modules.ai_scoring import DealScorer
                scorer = DealScorer()
                scorer.update_scores()
            elif task_name == 'affiliate_injection':
                from modules.affiliate_injector import update_deals_with_affiliate_links
                update_deals_with_affiliate_links()
            elif task_name == 'seo_sitemap':
                from modules.seo_sitemap import main as seo_main
                seo_main()
            elif task_name == 'social_auto':
                from modules.social_auto import main as social_main
                social_main()
            elif task_name == 'analytics_alert':
                from modules.analytics_dashboard import send_alert, get_metrics
                total, last_24h, avg = get_metrics()
                if last_24h < 5:
                    send_alert(last_24h)
            else:
                print(f"[AgentManager] Unknown task: {task_name}")
                self.update_task_status(task_name, success=False)
                return

            self.update_task_status(task_name, success=True)
        except Exception as e:
            print(f"[AgentManager] Task {task_name} failed: {e}")
            self.update_task_status(task_name, success=False)

    def scheduler_loop(self, interval_seconds=300):
        while True:
            task = self.get_next_task()
            if task:
                self.run_task(task)
            else:
                print("[AgentManager] No tasks to run.")
            time.sleep(interval_seconds)

def start_agent_manager():
    manager = AgentManager()
    t = threading.Thread(target=manager.scheduler_loop, daemon=True)
    t.start()
    print("[AgentManager] Scheduler started.")
    return manager

if __name__ == "__main__":
    start_agent_manager()
    while True:
        time.sleep(60)  # Keep main thread alive
