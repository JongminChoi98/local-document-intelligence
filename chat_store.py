import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4


DB_PATH = (
    Path(__file__).resolve().parent
    / "storage"
    / "chat_history.db"
)


@contextmanager
def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        conn.execute("PRAGMA foreign_keys = ON")

        with conn:
            yield conn
    finally:
        conn.close()


def init_db():
    with connect() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS chats (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT NOT NULL,
                payload TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id)
                    REFERENCES chats(id)
                    ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_messages_chat
            ON messages(chat_id, id);
        """)


def create_chat() -> str:
    chat_id = uuid4().hex

    with connect() as conn:
        conn.execute(
            "INSERT INTO chats (id, title) VALUES (?, ?)",
            (chat_id, "새 채팅"),
        )

    return chat_id


def list_chats() -> list[dict]:
    with connect() as conn:
        rows = conn.execute("""
            SELECT * FROM chats
            ORDER BY updated_at DESC, rowid DESC
        """).fetchall()

    return [dict(row) for row in rows]


def load_messages(chat_id: str) -> list[dict]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT payload FROM messages
            WHERE chat_id = ?
            ORDER BY id
            """,
            (chat_id,),
        ).fetchall()

    return [json.loads(row["payload"]) for row in rows]


def append_message(chat_id: str, message: dict):
    with connect() as conn:
        if message["role"] == "user":
            title = " ".join(message["content"].split())[:50]

            conn.execute(
                """
                UPDATE chats SET title = ?
                WHERE id = ? AND title = '새 채팅'
                AND NOT EXISTS (
                    SELECT 1 FROM messages WHERE chat_id = ?
                )
                """,
                (title, chat_id, chat_id),
            )

        conn.execute(
            """
            INSERT INTO messages (chat_id, payload)
            VALUES (?, ?)
            """,
            (
                chat_id,
                json.dumps(message, ensure_ascii=False),
            ),
        )

        conn.execute(
            """
            UPDATE chats SET updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (chat_id,),
        )


def rename_chat(chat_id: str, title: str):
    title = title.strip()[:100]

    if not title:
        raise ValueError("Chat title must not be empty.")

    with connect() as conn:
        conn.execute(
            "UPDATE chats SET title = ? WHERE id = ?",
            (title, chat_id),
        )


def delete_chat(chat_id: str):
    with connect() as conn:
        conn.execute(
            "DELETE FROM chats WHERE id = ?",
            (chat_id,),
        )
