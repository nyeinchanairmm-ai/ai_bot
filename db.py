import sqlite3

DB_NAME = "chat.db"

def get_db_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # return rows as dict-like objects
    return conn

def init_db():
    """Initialize the database and create tables if not exist."""
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


class ChatHistory:
    """Model-like helper for interacting with the messages table."""

    def __init__(self, id, role, content, timestamp):
        self.id = id
        self.role = role
        self.content = content
        self.timestamp = timestamp

    @staticmethod
    def add(role, content):
        """Insert a new message into the database."""
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO messages (role, content) VALUES (?, ?)",
            (role, content)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def all():
        """Fetch all messages ordered by timestamp."""
        conn = get_db_connection()
        rows = conn.execute(
            "SELECT * FROM messages ORDER BY timestamp"
        ).fetchall()
        conn.close()
        return [ChatHistory(row["id"], row["role"], row["content"], row["timestamp"]) for row in rows]

    @staticmethod
    def get_last(n=10):
        """Fetch the last N messages (default 10)."""
        conn = get_db_connection()
        rows = conn.execute(
            "SELECT * FROM messages ORDER BY timestamp DESC LIMIT ?",
            (n,)
        ).fetchall()
        conn.close()
        return [ChatHistory(row["id"], row["role"], row["content"], row["timestamp"]) for row in rows]

    def __repr__(self):
        return f"<ChatHistory id={self.id} role={self.role} content={self.content[:30]}...>"
