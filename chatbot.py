import requests
from flask import Blueprint, redirect, render_template, request, session, url_for

chat_bp = Blueprint("chat", __name__)

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "exaone3.5:2.4b"


def ask_ollama(messages):
    data = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0},
    }
    res = requests.post(OLLAMA_URL, json=data, timeout=120)
    res.raise_for_status()
    return res.json()["message"]["content"]


@chat_bp.route("/chat", methods=["GET", "POST"])
def chat():
    # 챗봇도 게시판처럼 로그인한 사람만 사용
    if "user_id" not in session:
        return redirect(url_for("login"))

    message = ""
    reply = ""
    if request.method == "POST":
        message = request.form.get("message", "")
        reply = ask_ollama([{"role": "user", "content": message}])
    return render_template("chat.html", message=message, reply=reply)