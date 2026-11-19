import sqlite3
from pathlib import Path

# db.py와 같은 폴더에 있는 app.db의 경로
DB_PATH = Path(__file__).with_name("app.db")


def get_post(post_id):
    conn = sqlite3.connect(DB_PATH)
    try:
        # 조회 결과를 컬럼 이름으로도 읽을 수 있게 설정
        conn.row_factory = sqlite3.Row

        # ? 자리에 게시글 번호를 전달하고, 일치하는 행 하나를 가져옴
        row = conn.execute(
            "SELECT id, user_id, title, content FROM posts WHERE id = ?",
            (post_id,),
        ).fetchone()

        if row is None:
            return None
        return dict(row)
    finally:
        conn.close()