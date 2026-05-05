import sqlite3
from datetime import datetime

DB_FILE = "urls.db"

class Database:
    def __init__(self):
        self._create_tables()

    def _connect(self):
        return sqlite3.connect(DB_FILE)

    def _create_tables(self):
        conn = self._connect()
        cursor = conn.cursor()

        # URLs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                short_code   TEXT    UNIQUE NOT NULL,
                original_url TEXT    NOT NULL,
                clicks       INTEGER DEFAULT 0,
                created_at   TEXT    NOT NULL
            )
        """)

        # Click history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS click_logs (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                short_code TEXT NOT NULL,
                clicked_at TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def code_exists(self, short_code):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM urls WHERE short_code = ?", (short_code,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def save_url(self, short_code, original_url):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO urls (short_code, original_url, created_at) VALUES (?, ?, ?)",
            (short_code, original_url, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        conn.close()

    def get_url(self, short_code):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT short_code, original_url, clicks, created_at FROM urls WHERE short_code = ?",
            (short_code,)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "short_code":   row[0],
                "original_url": row[1],
                "clicks":       row[2],
                "created_at":   row[3]
            }
        return None

    def track_click(self, short_code):
        conn = self._connect()
        cursor = conn.cursor()
        # Increment click count
        cursor.execute(
            "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?",
            (short_code,)
        )
        # Log click with timestamp
        cursor.execute(
            "INSERT INTO click_logs (short_code, clicked_at) VALUES (?, ?)",
            (short_code, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        conn.close()

    def get_clicks(self, short_code):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT clicked_at FROM click_logs WHERE short_code = ? ORDER BY clicked_at DESC",
            (short_code,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]

    def get_all_urls(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT short_code, original_url, clicks, created_at FROM urls ORDER BY created_at DESC"
        )
        rows = cursor.fetchall()
        conn.close()
        return [
            {
                "short_code":   row[0],
                "original_url": row[1],
                "clicks":       row[2],
                "created_at":   row[3]
            }
            for row in rows
        ]
