import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("app.db")

with sqlite3.connect(DB_PATH) as conn:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            email TEXT,
            phone TEXT,
            is_admin INTEGER
        );

        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            content TEXT
        );
    """)

    conn.executemany(
        """
        INSERT OR IGNORE INTO users
            (id, username, password, email, phone, is_admin)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (1, "admin", "admin1234!", "admin@site.com", "010-0000-0001", 1),
            (2, "alice", "alice1234", "alice@site.com", "010-1111-2222", 0),
            (3, "bob", "bob1234", "bob@site.com", "010-3333-4444", 0),
            (4, "victim", "victim1234", "victim@site.com", "010-9999-8888", 0),
        ],
    )

    conn.executemany(
        """
        INSERT OR IGNORE INTO posts (id, user_id, title, content)
        VALUES (?, ?, ?, ?)
        """,
        [
            (1, 1, "공지: 커뮤니티 오픈", "안녕하세요, 관리자입니다."),
            (2, 2, "오늘 점심 추천", "학식 뭐 먹지"),
            (3, 3, "웹해킹 스터디 모집", "같이 하실 분 구해요"),
        ],
    )

print(f"데이터베이스 초기화 완료: {DB_PATH}")