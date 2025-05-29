import sqlite3
import uuid
from datetime import datetime
import os

class SharedMemory:
    def __init__(self):
        self.db_path = "../outputs/memory.db"
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)  # Ensure outputs/ exists
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                thread_id TEXT PRIMARY KEY,
                source TEXT,
                type TEXT,
                timestamp TEXT,
                data TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def save(self, source, type_, data):
        thread_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        data_str = str(data)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO memory (thread_id, source, type, timestamp, data)
            VALUES (?, ?, ?, ?, ?)
        ''', (thread_id, source, type_, timestamp, data_str))
        conn.commit()
        conn.close()
        return thread_id

    def retrieve(self, thread_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM memory WHERE thread_id = ?', (thread_id,))
        result = cursor.fetchone()
        conn.close()
        return result