import secrets
import sqlite3

from flask import Flask, redirect, render_template, request, session, url_for
from db import DB_PATH

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

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)