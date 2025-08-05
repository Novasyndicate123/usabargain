import time
import sqlite3
import random
from core.context_memory_mesh import ContextMemoryMesh

PULSE_DB = "data/novacortex_state.db"

EVENT_TYPES = [
    "deal_spike",
    "affiliate_revenue",
    "scraper_error",
    "agent_response",
    "user_vote",
    "price_drop",
]

class PulseMonitor:
    def __init__(self, db_path=PULSE_DB):
        self.db_path = db_path
        self.memory_mesh = ContextMemoryMesh(db_path)
        self._init_pulse_table()

    def _init_pulse_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS event_pulse (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT,
                    description TEXT,
                    entropy REAL,
                    timestamp REAL
                )
            ''')
            conn.commit()

    def log_event(self, event_type, description, entropy):
        ts = time.time()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO event_pulse (event_type, description, entropy, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (event_type, description, entropy, ts))
        if entropy > 0.7:
            self.memory_mesh.inject(
                context=f"event_{event_type}",
                value=description,
                importance=entropy
            )
            print(f"[⚡ HIGH-ENTROPY EVENT] → {event_type}: {description}")

    def simulate_event_stream(self):
        while True:
            event = random.choice(EVENT_TYPES)
            description = f"{event} detected at {time.strftime('%X')}"
            entropy = round(random.uniform(0.3, 1.0), 2)
            self.log_event(event, description, entropy)
            time.sleep(5)

if __name__ == "__main__":
    monitor = PulseMonitor()
    monitor.simulate_event_stream()
