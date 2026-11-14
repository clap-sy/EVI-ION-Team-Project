from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "AI 커뮤니티 서버가 실행 중입니다."

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)