import sqlite3
import hashlib
import time

DB_PATH = "data/novacortex_state.db"

def hash_context(context):
    return hashlib.sha256(context.encode()).hexdigest()

class ContextMemoryMesh:
    def __init__(self, db_path=DB_PATH):
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS memory_mesh (
                id TEXT PRIMARY KEY,
                context TEXT,
                value TEXT,
                importance REAL,
                timestamp REAL
            )
        ''')
        self.conn.commit()

    def inject(self, context: str, value: str, importance: float = 0.5):
        uid = hash_context(context + value)
        ts = time.time()
        with self.conn:
            self.conn.execute('''
                INSERT OR REPLACE INTO memory_mesh (id, context, value, importance, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (uid, context, value, importance, ts))

    def query(self, context: str, threshold: float = 0.4):
        c = self.conn.cursor()
        c.execute('''
            SELECT context, value, importance, timestamp
            FROM memory_mesh
            WHERE context LIKE ? AND importance >= ?
            ORDER BY importance DESC, timestamp DESC
            LIMIT 10
        ''', (f"%{context}%", threshold))
        return c.fetchall()

    def list_all(self):
        c = self.conn.cursor()
        c.execute('SELECT context, value, importance, timestamp FROM memory_mesh ORDER BY timestamp DESC')
        return c.fetchall()

if __name__ == "__main__":
    mesh = ContextMemoryMesh()
    mesh.inject("agent_activity", "Agent_3 optimized 12 deals", 0.9)
    mesh.inject("market_trend", "Flash sales rising on electronics", 0.7)

    print("📦 Retrieved Knowledge:")
    for row in mesh.query("agent"):
        print(row)
