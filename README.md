# AI 챗봇 커뮤니티 웹 모의해킹 프로젝트

보안 학습을 위해 취약점을 포함한 커뮤니티 웹사이트를 로컬에서 실행하고, 취약점을 재현한 뒤 패치하는 3인 미니 프로젝트입니다.

> 이 프로젝트는 학습 및 모의해킹 실습용입니다. 서버는 `127.0.0.1`에서만 실행하며 외부에 공개하지 않습니다.

## 기술 스택

- Python 3.11 이상
- Flask 3.0.3
- SQLite
- Ollama 로컬 모델 `exaone3.5:2.4b`
- `requests` 2.32.3

## 프로젝트 구조 (vulnerable 브랜치 기준)

```text
.
├── app.py
├── init_db.py
├── requirements.txt
├── README.md
├── SPEC.md
├── .gitignore
├── .gitattributes
├── templates/
├── static/
└── docs/
    └── evidence/
```

`app.db`와 `venv/`는 각자 컴퓨터에서 생성하며 GitHub에는 올리지 않습니다.

## 브랜치

- `main`: README, SPEC, requirements, 공통 설정 파일 및 문서
- `vulnerable`: 취약점이 포함된 웹사이트 코드
- `patched`: 4주차에 `vulnerable`에서 분기하는 패치 버전

## 실행 방법

저장소를 클론한 뒤 프로젝트 폴더에서 git switch vulnerable을 실행합니다. 아래 가상환경 생성과 DB 초기화는 처음 실행할 때 한 번만 진행합니다.

프로젝트 루트 폴더에서 아래 명령을 실행합니다.

### Windows CMD

```cmd
py -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
python init_db.py
python app.py
```

### macOS 터미널

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python init_db.py
python app.py
```

브라우저에서 [http://127.0.0.1:5001](http://127.0.0.1:5001)에 접속합니다.

````

가상환경을 종료하려면 서버를 실행한 터미널에서 Ctrl+C로 서버를 종료한 뒤, 다음 명령을 입력합니다.

```text
deactivate
````

## 테스트 계정

| 사용자명 | 비밀번호   | 용도           |
| -------- | ---------- | -------------- |
| admin    | admin1234! | 관리자 계정    |
| alice    | alice1234  | 일반 사용자    |
| bob      | bob1234    | 일반 사용자    |
| victim   | victim1234 | IDOR 실습 대상 |

이 계정은 프로젝트의 로컬 실습용 시드 계정입니다.

## 의도된 취약점

취약점 번호와 설명은 [SPEC.md](SPEC.md)를 기준으로 합니다. 취약 코드에는 해당 번호를 나타내는 `# VULN-번호` 주석을 표시합니다.

## 증거 이미지

공격 및 패치 과정의 스크린샷은 `docs/evidence/`에 저장합니다.

파일명 형식:

```text
VULN<번호>-<V 또는 P>-<시나리오순번>_<스샷연번>.png
```

예시:

```text
VULN1-V-01_1.png
```
