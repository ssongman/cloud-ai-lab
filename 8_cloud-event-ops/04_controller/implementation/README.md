# Controller Application - Implementation

## 개요

Controller Application의 실제 소스 코드가 위치하는 디렉토리입니다.

## 기술 스택

- **언어**: Python 3.11+
- **OpenSearch 클라이언트**: opensearch-py
- **RAG**: LangChain + OpenSearch Vector DB
- **설정**: Pydantic Settings
- **스케줄링**: APScheduler
- **HTTP**: httpx (비동기)
- **테스트**: pytest

## 프로젝트 구조 (예정)

```
implementation/
├── README.md
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── main.py              # 엔트리포인트
│   ├── config.py             # 설정 관리
│   ├── poller/               # 이벤트 폴링
│   ├── detection/            # 탐지 엔진
│   ├── rag/                  # RAG 판단 보조
│   ├── alerting/             # 알림 발송
│   └── models/               # 데이터 모델
├── tests/
├── Dockerfile
└── k8s/
    ├── deployment.yaml
    └── configmap.yaml
```

## 시작하기

> 구현 진행 시 상세 내용이 추가됩니다.





## LLM Open API Key



export OPENAI_API_KEY="your-api-key-here"

export OPENAI_API_KEY="sk-proj-9ruwQXS..."

