# Simple Chat

간단한 AI 채팅 프로그램입니다.

## 기능

- OpenAI API를 활용한 대화형 채팅 인터페이스
- Rich 라이브러리를 사용한 마크다운 및 코드 블록 렌더링
- 다양한 색상의 대화 표시

## 설치 방법

### 1. 가상환경 설정

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 2. 의존성 설치

프로젝트에 필요한 패키지들은 `requirements.txt`에 명시되어 있습니다:


```1:17:requirements.txt
annotated-types==0.7.0
anyio==4.6.2.post1
certifi==2024.8.30
colorama==0.4.6
distro==1.9.0
exceptiongroup==1.2.2
h11==0.14.0
httpcore==1.0.6
httpx==0.27.2
idna==3.10
jiter==0.7.0
markdown-it-py==3.0.0
mdurl==0.1.2
openai==1.54.0
pydantic==2.9.2
pydantic_core==2.23.4
Pygments==2.18.0
```


다음 명령어로 필요한 패키지들을 설치합니다:

```bash
pip install -r requirements.txt
```

주요 의존성:
- openai: OpenAI API 클라이언트
- rich: 터미널 텍스트 스타일링 및 마크다운 렌더링
- httpx: 비동기 HTTP 클라이언트
- pydantic: 데이터 검증

## 실행 방법

```bash
python chat.py
```

## 사용 방법

1. 프로그램 실행 시 환영 메시지가 표시됩니다
2. 대화를 시작하면 사용자 입력과 AI 응답이 다른 색상으로 구분되어 표시됩니다
3. 프로그램 종료는 'quit' 입력

## 주의사항

- OpenAI API 설정이 필요합니다 (`chat.py` 파일의 base_url과 api_key 설정)
- 가상환경 사용을 권장합니다
- Python 3.10 이상 버전 필요

## 가상환경 관련 팁

1. 가상환경 비활성화:
```bash
deactivate
```

2. 현재 설치된 패키지 목록 확인:
```bash
pip freeze
```

3. 새로운 패키지 설치 시:
```bash
pip install 패키지명
pip freeze > requirements.txt  # 의존성 목록 업데이트
```

4. 가상환경 삭제:
```bash
# Windows
rmdir /s /q venv
# macOS/Linux
rm -rf venv
```

## 프로젝트 구조

```
simple-chat/
├── venv/               # 가상환경 디렉토리
├── requirements.txt    # 의존성 목록
├── chat.py            # 메인 프로그램
└── README.md          # 문서
```

## Peter Kwon @ Suresoft Technologies Incs.
