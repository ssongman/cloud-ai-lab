# Design Document - Controller Application

## 1. 개요

Controller Application은 OpenSearch에 수집된 클라우드 이벤트를 감시하고,
탐지 룰에 따라 알림을 발송하는 이벤트 처리 엔진입니다.

## 2. 아키텍처

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  OpenSearch │────▶│  Controller  │────▶│  Alert      │
│  (이벤트)     │     │  Application │     │  Channels   │
└─────────────┘     └──────┬───────┘     └─────────────┘
                           │
                    ┌──────▼───────┐
                    │  RAG         │
                    │  Knowledge   │
                    └──────────────┘
```

## 3. 핵심 모듈

### 3.1 Event Poller
- OpenSearch 쿼리를 주기적으로 실행
- Cursor 기반으로 마지막 처리 시점 관리
- 설정 가능한 폴링 주기 (기본 30초)

### 3.2 Detection Engine
- 탐지 룰 로딩 (YAML/JSON 기반)
- 이벤트와 룰 매칭
- 매칭 결과에 따라 P0/P1/P2 분류

### 3.3 RAG Advisor (선택적)
- 탐지된 이벤트에 대해 RAG 기반 추가 판단
- 유사 과거 사례 조회
- 대응 플레이북 추천

### 3.4 Alert Router
- 우선순위에 따른 채널 라우팅
- 중복 제거 (Deduplication)
- 쿨다운/억제 (Suppression)
- 에스컬레이션 타이머

### 3.5 Notification Sender
- Mattermost Webhook
- SMTP Email
- SMS Gateway

## 4. 기술 스택

| 항목 | 선택지 | 비고 |
|------|--------|------|
| 언어 | Python 3.11+ | 빠른 프로토타이핑, LLM 라이브러리 풍부 |
| OpenSearch 클라이언트 | opensearch-py | 공식 Python 클라이언트 |
| RAG | LangChain + OpenSearch Vector DB | 벡터 검색 기반 |
| 설정 관리 | Pydantic Settings | 환경변수/파일 기반 |
| 스케줄링 | APScheduler | 폴링 주기 관리 |

## 5. 데이터 모델

### 탐지 룰 스키마
```yaml
rule_id: "azure-vm-deleted"
name: "Azure VM 삭제 감지"
severity: P0
provider: azure
conditions:
  event_type: "Microsoft.Compute/virtualMachines/delete"
  status: "Succeeded"
description: "프로덕션 VM이 삭제되었습니다."
channels: ["mattermost", "email", "sms"]
cooldown_minutes: 30
```

## 6. 배포

- Kubernetes Deployment (replicas: 2)
- ConfigMap: 탐지 룰, 설정
- Secret: OpenSearch 인증정보, Webhook URL
