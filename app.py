import secrets
import sqlite3

from flask import Flask, abort, redirect, render_template, request, session, url_for
from db import DB_PATH, get_post

app = Flask(__name__)

# Flask가 세션 쿠키에 서명할 때 사용하는 키
# 서버를 다시 시작하면 새 키가 생성되어 다시 로그인해야 함
app.secret_key = secrets.token_hex(32)


@app.route("/")
def home():
    if "user_id" in session:
        return render_template("login_success.html")
    
    return "AI 커뮤니티 서버가 실행 중입니다."

@app.route("/login", methods=["GET", "POST"])
def login():
    # 주소로 접속했을 때 로그인 화면 표시
    if request.method == "GET":
        return render_template("login.html")

    # 로그인 폼의 name 속성으로 입력값 가져오기
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.row_factory = sqlite3.Row

        # VULN-1: 사용자 입력을 SQL 문자열에 직접 연결
        query = (
            "SELECT id, username, is_admin FROM users "
            f"WHERE username = '{username}' AND password = '{password}'"
        )
        user = conn.execute(query).fetchone()
    finally:
        conn.close()

    # 일치하는 사용자가 없으면 실패 메시지 표시
    if user is None:
        return render_template(
            "login.html",
            error = "아이디 또는 비밀번호가 올바르지 않습니다.",
        )

    # 기존 세션을 비우고 팀 규격의 세 가지 값 저장
    session.clear()
    session["user_id"] = user["id"]
    session["username"] = user["username"]
    session["is_admin"] = user["is_admin"]

    # 로그인에 성공하면 첫 화면으로 이동
    return redirect(url_for("home"))

@app.route("/logout", methods=["GET"])
def logout():
    # 로그인할 때 저장한 세션 정보 모두 제거
    session.clear()

    # 로그아웃 후 로그인 화면으로 이동
    return redirect(url_for("login"))

@app.route("/board", methods=["GET", "POST"])
def board():
    if request.method == "POST":
        # 게시글 작성에는 로그인이 필요함
        if "user_id" not in session:
            return redirect(url_for("login"))

        # 작성 폼에서 제목과 내용 가져오기
        title = request.form.get("title", "")
        content = request.form.get("content", "")

        conn = sqlite3.connect(DB_PATH)
        try:
            # 작성자 ID는 로그인 세션에서 가져옴
            conn.execute(
                "INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)",
                (session["user_id"], title, content),
            )
            conn.commit()  # 추가한 게시글을 DB에 저장
        finally:
            conn.close()

        # 저장 후 목록으로 이동해 새로고침 시 중복 제출 방지
        return redirect(url_for("board"))

    # GET 요청이면 게시글 목록 조회
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.row_factory = sqlite3.Row
        posts = conn.execute(
            "SELECT id, title FROM posts ORDER BY id"
        ).fetchall()
    finally:
        conn.close()

    return render_template("board.html", posts=posts)

@app.route("/board/<int:post_id>", methods=["GET"])
def post_detail(post_id):
    # URL에서 받은 게시글 번호로 DB 조회
    post = get_post(post_id)

    # 존재하지 않는 게시글이면 404 응답
    if post is None:
        abort(404)

    return render_template("post_detail.html", post=post)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)