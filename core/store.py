%%writefile core/store.py
import sqlite3
import json
from datetime import datetime
from typing import Dict, Any

class SQLiteEventStore:
    def __init__(self, db_path: str = "events.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """
        Создание Append-Only таблицы событий согласно спецификации NKS-001.
        """
        query = """
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            source TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            payload TEXT NOT NULL,
            metadata TEXT
        );
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_type ON events(type);")
            conn.commit()

    def save(self, event: Dict[str, Any]) -> None:
        """
        Сохранение события в Append-Only лог.
        """
        required_fields = ["id", "type", "source", "payload"]
        for field in required_fields:
            if field not in event:
                raise ValueError(f"[SQLiteEventStore Error] Missing required event field: {field}")

        event_id = event["id"]
        event_type = event["type"]
        source = event["source"]
        timestamp = event.get("timestamp", datetime.utcnow().isoformat())
        
        payload_str = json.dumps(event["payload"], ensure_ascii=False)
        metadata_str = json.dumps(event.get("metadata", {}), ensure_ascii=False)

        query = "INSERT INTO events (id, type, source, timestamp, payload, metadata) VALUES (?, ?, ?, ?, ?, ?);"
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (event_id, event_type, source, timestamp, payload_str, metadata_str))
                conn.commit()
        except sqlite3.IntegrityError:
            raise IOError(f"[SQLiteEventStore Error] Event with ID {event_id} already exists. Append-Only violation.")

    def get_all_events(self) -> list:
        """
        Выгрузка всех событий в хронологическом порядке для процедуры Replay.
        """
        query = "SELECT id, type, source, timestamp, payload, metadata FROM events ORDER BY timestamp ASC;"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            
        events = []
        for row in rows:
            events.append({
                "id": row[0],
                "type": row[1],
                "source": row[2],
                "timestamp": row[3],
                "payload": json.loads(row[4]),
                "metadata": json.loads(row[5]) if row[5] else {}
            })
        return events