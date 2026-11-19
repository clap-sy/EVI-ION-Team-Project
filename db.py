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

def get_user_info(user_id):
    # VULN-6: 학습용 취약 버전 — 세션·권한 확인 없이 요청한 사용자 정보를 반환
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.row_factory = sqlite3.Row

        # 전달받은 사용자 ID로 규격에 정해진 다섯 항목 조회
        row = conn.execute(
            """
            SELECT id, username, email, phone, is_admin
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

        # 해당 사용자가 없으면 None 반환
        if row is None:
            return None

        # 조회 결과를 딕셔너리로 반환
        return dict(row)
    finally:
        # 조회가 끝나면 DB 연결 종료
        conn.close()