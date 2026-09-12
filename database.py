import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "news_history.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posted_news (
            id INTEGER PRIMARY KEY,
            original_text TEXT,
            translated_text TEXT,
            media_type TEXT,
            media_url TEXT,
            posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def is_news_posted(news_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM posted_news WHERE id = ?", (news_id,))
    row = cursor.fetchone()
    conn.close()
    return row is not None

def mark_news_posted(news_id: int, original_text: str = "", translated_text: str = "", media_type: str = "text", media_url: str = ""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO posted_news (id, original_text, translated_text, media_type, media_url)
        VALUES (?, ?, ?, ?, ?)
    """, (news_id, original_text, translated_text, media_type, media_url))
    conn.commit()
    conn.close()

def get_max_posted_id() -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM posted_news")
    row = cursor.fetchone()
    conn.close()
    return row[0] if row and row[0] else 0
