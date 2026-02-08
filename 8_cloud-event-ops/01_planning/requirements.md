# Requirements

## 기능 요구사항

### FR-1: OpenSearch 클러스터 구축
- Kubernetes 환경에 OpenSearch 설치
- OpenSearch Dashboards(Kibana 대체) 설치
- 클러스터 고가용성 구성

### FR-2: 클라우드 이벤트 수집
- Azure Activity Log / Event Grid 이벤트 수집
- AWS CloudTrail / EventBridge 이벤트 수집
- 이벤트 정규화 및 인덱싱

### FR-3: 데이터 시각화
- OpenSearch Dashboards를 통한 이벤트 대시보드
- 실시간 모니터링 뷰

### FR-4: Controller Application
- 이벤트 수집 시 실시간 감시
- 이상징후 탐지 룰 엔진
- RAG 기반 판단 보조 시스템

### FR-5: 알림 시스템
- 이메일, SMS, Slack/Mattermost 알림
- 우선순위 기반 라우팅
- 중복 제거 및 억제 정책

### FR-6: 데이터 라이프사이클
- 인덱스 롤오버 정책
- 데이터 보관/삭제 정책

### FR-7: 보안
- 인증/인가 (RBAC)
- TLS/SSL 통신 암호화
- API 키 관리

## 비기능 요구사항

### NFR-1: 성능
- 이벤트 수집 지연 < 5분
- 알림 발송 지연 < 1분 (P0 이벤트)

### NFR-2: 가용성
- OpenSearch 클러스터 99.9% 가용성

### NFR-3: 확장성
- 수평 확장 가능한 아키텍처

### NFR-4: 운영성
- 장애 복구 절차 문서화
- 모니터링 및 로깅
