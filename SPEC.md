# 팀 공통 규격

## 1. 프로젝트 개요

- 주제: AI 상담 챗봇이 포함된 커뮤니티 웹사이트의 취약점 진단
- 목적: 학습용 취약 웹사이트 실행 → 취약점 공격 및 재현 → 패치 → 보고서 작성
- 팀 구성: 3명
- 서버 실행 주소: `127.0.0.1` 로컬 전용
- 외부에 웹 서버를 공개하지 않습니다.

## 2. 기술 및 실행 환경

- Python: 3.11
- 웹 프레임워크: Flask 3.0.3
- 데이터베이스: SQLite
- 챗봇: Ollama 로컬 모델
- HTTP 요청 라이브러리: requests 2.32.3
- 가상환경 폴더명: `venv`
- 서버 포트: `5001`

서버 실행 코드는 다음 설정을 사용합니다.

```python
app.run(host="127.0.0.1", port=5001, debug=True)
```

## 3. 패키지

`requirements.txt`:

```text
Flask==3.0.3
requests==2.32.3
```

Ollama 모델: `exaone3.5:2.4b` (팀원 모두 동일 모델 사용)
- 선택 이유: 한국어 응답 품질 (llama3.2:3b는 한국어 응답이 부정확함)

## 4. 데이터베이스

- 종류: SQLite
- 파일명: `app.db`
- 초기화 파일: `init_db.py`

### users 테이블

| 컬럼     | 자료형                            | 설명                  |
| -------- | --------------------------------- | --------------------- |
| id       | INTEGER PRIMARY KEY AUTOINCREMENT | 사용자 ID             |
| username | TEXT                              | 사용자명              |
| password | TEXT                              | 학습용 비밀번호       |
| email    | TEXT                              | 이메일                |
| phone    | TEXT                              | 전화번호              |
| is_admin | INTEGER                           | 관리자 여부: 0 또는 1 |

### posts 테이블

| 컬럼    | 자료형                            | 설명      |
| ------- | --------------------------------- | --------- |
| id      | INTEGER PRIMARY KEY AUTOINCREMENT | 게시글 ID |
| user_id | INTEGER                           | 작성자 ID |
| title   | TEXT                              | 제목      |
| content | TEXT                              | 내용      |

### 시드 사용자

|  id | username | password   | email           | phone         | is_admin |
| --: | -------- | ---------- | --------------- | ------------- | -------: |
|   1 | admin    | admin1234! | admin@site.com  | 010-0000-0001 |        1 |
|   2 | alice    | alice1234  | alice@site.com  | 010-1111-2222 |        0 |
|   3 | bob      | bob1234    | bob@site.com    | 010-3333-4444 |        0 |
|   4 | victim   | victim1234 | victim@site.com | 010-9999-8888 |        0 |

`victim` 계정은 VULN-3 IDOR 실습 대상입니다.

### 시드 게시글

|  id | user_id | title               | content                   |
| --: | ------: | ------------------- | ------------------------- |
|   1 |       1 | 공지: 커뮤니티 오픈 | 안녕하세요, 관리자입니다. |
|   2 |       2 | 오늘 점심 추천      | 학식 뭐 먹지              |
|   3 |       3 | 웹해킹 스터디 모집  | 같이 하실 분 구해요       |

VULN-5 실습용 악성 게시글은 시드에 넣지 않고 공격 시나리오에서 작성합니다.

## 5. 회원가입 범위

초기 구현에서는 회원가입(`/register`)을 넣지 않습니다. 사용자는 시드 계정으로만 생성합니다.

## 6. 취약점 번호

아래 번호를 코드 주석, 공격 시나리오, 증거 이미지, 보고서에서 동일하게 사용합니다.

| 통일 번호 | 취약점                                                 |
| --------- | ------------------------------------------------------ |
| VULN-1    | 로그인 SQL 인젝션                                      |
| VULN-2    | 게시판 Stored XSS                                      |
| VULN-3    | IDOR: URL의 사용자 ID 변경을 통한 타인 마이페이지 접근 |
| VULN-4    | 프롬프트 인젝션을 통한 시스템 프롬프트·비밀 정보 유출  |
| VULN-5    | 게시글 속 악성 지시문을 이용한 간접 프롬프트 인젝션    |
| VULN-6    | 챗봇의 과도한 권한으로 다른 사용자 정보 조회           |
| VULN-7    | 챗봇 응답을 HTML로 출력해 발생하는 XSS                 |

의도적으로 취약하게 작성한 코드에는 관련된 `# VULN-번호` 주석을 표시합니다.

VULN-4 비밀값:

```text
FLAG{pr0mpt_1nj3ction_2026}
```

공격 성공 기준은 챗봇 응답에 위 문자열이 그대로 나타나는 것입니다.

## 7. URL 라우트

| 메서드    | 경로                    | 기능        | 취약점   |
| --------- | ----------------------- | ----------- | -------- |
| GET, POST | `/login`                | 로그인      | VULN-1   |
| GET       | `/logout`               | 로그아웃    | -        |
| GET       | `/board`                | 게시글 목록 | -        |
| GET       | `/board/<int:post_id>`  | 게시글 보기 | VULN-2   |
| POST      | `/board`                | 게시글 작성 | VULN-2   |
| GET       | `/mypage/<int:user_id>` | 마이페이지  | VULN-3   |
| POST      | `/chat`                 | 챗봇 요청   | VULN-4~7 |

Flask 경로 변수는 `<int:post_id>`, `<int:user_id>` 형식으로 작성합니다.

## 8. 챗봇 담당자에게 제공할 함수

### `get_post(post_id)`

게시글이 있으면 다음 형식의 dict를 반환하고, 없으면 `None`을 반환합니다.

```python
{
    "id": int,
    "user_id": int,
    "title": str,
    "content": str
}
```

### `get_user_info(user_id)`

사용자가 있으면 다음 형식의 dict를 반환하고, 없으면 `None`을 반환합니다.

```python
{
    "id": int,
    "username": str,
    "email": str,
    "phone": str,
    "is_admin": int
}
```

권한 확인은 이 함수를 호출하는 라우트 또는 챗봇 기능에서 처리합니다. 취약 버전에서는 해당 확인이 누락된 동작을 재현하고, 패치 버전에서는 세션 기준 권한 검사를 적용합니다.

## 9. 세션 규칙

로그인에 성공하면 다음 값을 세션에 저장합니다.

```python
session["user_id"]
session["username"]
session["is_admin"]
```

패치 버전의 권한 검사는 요청 파라미터가 아니라 로그인 세션을 기준으로 합니다.

## 10. 패치 방향

| 취약점 | 패치 방향                                               |
| ------ | ------------------------------------------------------- |
| VULN-1 | SQL 문자열 연결 대신 파라미터 바인딩 사용               |
| VULN-2 | 게시글 출력 시 템플릿 자동 이스케이프 적용              |
| VULN-3 | 세션 사용자 ID와 요청한 사용자 ID의 권한 확인           |
| VULN-4 | 시스템 프롬프트와 비밀 정보를 사용자 입력·응답에서 보호 |
| VULN-5 | 게시글 내용을 신뢰할 수 없는 데이터로 처리              |
| VULN-6 | 챗봇 기능의 사용자 정보 조회 권한을 세션 기준으로 제한  |
| VULN-7 | 챗봇 응답을 HTML로 직접 실행하지 않도록 안전하게 출력   |

## 11. Git 브랜치 및 커밋 규칙

- `main`: README, SPEC, requirements, `.gitattributes`, `docs/` 등 공통 파일
- `vulnerable`: 취약점이 포함된 구현 코드
- `patched`: 4주차에 `vulnerable`에서 분기
- `.gitignore`에는 `venv/`와 `app.db`를 포함
- `.gitattributes` 내용:

```gitattributes
* text=auto eol=lf
```

커밋 메시지 앞에 담당자 접두어를 붙입니다. 예: `[A]`, `[B]`, `[C]`

## 12. 스크린샷 증거

증거 이미지는 `docs/evidence/`에 저장하고 Git에 포함합니다.

파일명 형식:

```text
VULN<번호>-<V 또는 P>-<시나리오순번>_<스샷연번>.png
```

예시:

```text
VULN1-V-01_1.png
VULN3-P-01_1.png
```

- `V`: vulnerable 버전의 공격 증거
- `P`: patched 버전의 패치 확인 증거

## 13. 작업 방식

- 코드와 실행 방법은 초보자도 따라 할 수 있게 설명합니다.
- 큰 구현은 작은 단계로 나누어 진행합니다.
- 요청되지 않은 기능은 추가하지 않습니다.
- 디자인보다 기능 동작과 취약점 재현·패치에 집중합니다.
