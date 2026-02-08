# System Architecture

## 계층 구조

```
┌─────────────────────────────────────────────┐
│              Cloud Providers                 │
│   Azure (Activity Log, Event Grid)          │
│   AWS   (CloudTrail, EventBridge)           │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│           Ingestion Layer                    │
│   Logstash / FluentBit / Lambda             │
│   이벤트 정규화 · 필터링 · 라우팅            │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│           Storage & Search Layer             │
│   OpenSearch Cluster (Master + Data Nodes)   │
│   Index Lifecycle Management (ILM)           │
└──────────┬───────────────────┬──────────────┘
           │                   │
┌──────────▼──────┐  ┌────────▼──────────────┐
│  Dashboards     │  │  Controller App        │
│  시각화/대시보드  │  │  이벤트 감시           │
│                 │  │  이상징후 탐지          │
│                 │  │  RAG 판단 보조          │
└─────────────────┘  └────────┬──────────────┘
                              │
                   ┌──────────▼──────────────┐
                   │   Alert System           │
                   │   Email / SMS / Slack    │
                   │   Mattermost Webhook     │
                   └──────────────────────────┘
```

## 컴포넌트 상세

### 1. Ingestion Layer
- **Azure**: Event Hub → Logstash OpenSearch Output Plugin
- **AWS**: EventBridge → Lambda → OpenSearch Bulk API
- 공통 이벤트 스키마로 정규화

### 2. OpenSearch Cluster
- Master Node × 3 (고가용성)
- Data Node × 2+ (확장 가능)
- ILM: hot → warm → cold → delete

### 3. Controller Application
- OpenSearch Alerting Plugin 또는 커스텀 폴링 기반
- 탐지 룰 매칭 → RAG 판단 → 알림 발송

### 4. Alert System
- Webhook 기반 알림 (Mattermost, Slack)
- SMTP 이메일 발송
- 에스컬레이션 체계 (P0 → 즉시, P1 → 5분, P2 → 일간 리포트)
